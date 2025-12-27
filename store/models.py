from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

def validate_image_size(image):
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError('Image size cannot exceed 5MB')

def validate_not_empty(value):
    if not value.strip():
        raise ValidationError('This field cannot be empty')

def validate_description_length(value):
    if len(value.strip()) < 10:
        raise ValidationError('Description must be at least 10 characters')

class Category(models.Model):
    name = models.CharField(max_length=100, validators=[validate_not_empty])
    slug = models.SlugField(unique=True, max_length=100)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.name.strip():
            raise ValidationError('Category name cannot be empty')

class Product(models.Model):
    SIZES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), 
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')
    ]
    
    name = models.CharField(max_length=200, validators=[validate_not_empty])
    slug = models.SlugField(unique=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.TextField(validators=[validate_description_length])
    image = models.ImageField(upload_to='products/', blank=True, null=True, validators=[validate_image_size])
    image_url = models.URLField(blank=True, null=True, help_text="Unsplash image URL")
    available_sizes = models.JSONField(default=list)
    stock = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(9999)])
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.name.strip():
            raise ValidationError('Product name cannot be empty')
        if len(self.description.strip()) < 10:
            raise ValidationError('Description must be at least 10 characters')
        if self.price <= 0:
            raise ValidationError('Price must be greater than 0')
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if not self.user and not self.session_key:
            raise ValidationError('Cart must have either user or session_key')
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=3, choices=Product.SIZES)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(99)])
    
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be at least 1')
        if self.quantity > self.product.stock:
            raise ValidationError('Quantity cannot exceed available stock')
    
    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total_price(self):
        return self.quantity * self.price