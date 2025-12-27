document.addEventListener('DOMContentLoaded', function() {
    // Enhanced Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || '0s';
                entry.target.style.animationDelay = delay;
                entry.target.style.transitionDelay = delay;
                entry.target.classList.add('animate-in');
                
                // Counter animation for stats
                if (entry.target.classList.contains('counter-stat')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.animate-on-scroll, .animate-fade-up, .animate-slide-in').forEach(el => {
        observer.observe(el);
    });

    // Counter animation
    function animateCounter(element) {
        const target = parseInt(element.dataset.target);
        const numberElement = element.querySelector('.stat-number');
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            numberElement.textContent = Math.floor(current).toLocaleString();
        }, 16);
    }

    // Parallax effect for hero and other elements
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        
        // Hero background parallax
        const heroBackground = document.querySelector('.hero-animated-bg');
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
        
        // Parallax elements
        document.querySelectorAll('.parallax-element').forEach(element => {
            const speed = parseFloat(element.dataset.speed) || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
        
        ticking = false;
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    });

    // Product filtering and sorting
    const filterButtons = document.querySelectorAll('.filter-btn');
    const sortSelect = document.getElementById('sortSelect');
    const productGrid = document.getElementById('productGrid');
    
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Update active state
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Filter products
                const filter = this.dataset.filter;
                filterProducts(filter);
            });
        });
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            sortProducts(this.value);
        });
    }
    
    function filterProducts(filter) {
        const products = document.querySelectorAll('.catalog-item');
        
        products.forEach(product => {
            const category = product.dataset.category;
            
            if (filter === 'all' || category === filter) {
                product.style.display = 'block';
                product.style.animation = 'fadeIn 0.5s ease forwards';
            } else {
                product.style.display = 'none';
            }
        });
    }
    
    function sortProducts(sortBy) {
        const products = Array.from(document.querySelectorAll('.catalog-item'));
        const container = document.getElementById('productGrid');
        
        products.sort((a, b) => {
            switch (sortBy) {
                case 'price-low':
                    return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
                case 'price-high':
                    return parseFloat(b.dataset.price) - parseFloat(a.dataset.price);
                case 'name':
                    return a.dataset.name.localeCompare(b.dataset.name);
                case 'newest':
                default:
                    return 0; // Keep original order
            }
        });
        
        // Re-append sorted products
        products.forEach(product => container.appendChild(product));
    }

    // View toggle (grid/list)
    const viewButtons = document.querySelectorAll('.view-btn');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            viewButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const view = this.dataset.view;
            toggleView(view);
        });
    });
    
    function toggleView(view) {
        const grid = document.getElementById('productGrid');
        if (grid) {
            grid.className = view === 'list' ? 'catalog-list' : 'catalog-grid';
        }
    }

    // Enhanced add to cart functionality
    const addToCartForms = document.querySelectorAll('.product-form-editorial, .add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            formData.append('product_id', form.dataset.productId);
            
            // Check if size is selected
            const sizeSelected = form.querySelector('input[name=\"size\"]:checked');
            if (!sizeSelected) {
                showNotification('Please select a size', 'error');
                shakeElement(form.querySelector('.size-grid, .size-options'));
                return;
            }
            
            // Button loading state
            const button = form.querySelector('.add-to-cart-editorial, .add-to-cart-btn');
            setButtonLoading(button, true);
            
            fetch('/add-to-cart/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Added to cart!', 'success');
                    setButtonSuccess(button);
                    updateCartCount();
                } else {
                    showNotification('Error adding to cart', 'error');
                    setButtonLoading(button, false);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error adding to cart', 'error');
                setButtonLoading(button, false);
            });
        });
    });

    // Product detail page interactions
    
    // Image gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('mainImage');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            this.classList.add('active');
            
            if (mainImage) {
                const newSrc = this.dataset.image;
                mainImage.style.opacity = '0';
                setTimeout(() => {
                    mainImage.src = newSrc;
                    mainImage.style.opacity = '1';
                }, 200);
            }
        });
    });
    
    // Quantity controls
    const decreaseBtn = document.getElementById('decreaseQty');
    const increaseBtn = document.getElementById('increaseQty');
    const quantityInput = document.getElementById('quantityInput');
    
    if (decreaseBtn && increaseBtn && quantityInput) {
        decreaseBtn.addEventListener('click', () => {
            const current = parseInt(quantityInput.value);
            if (current > 1) {
                quantityInput.value = current - 1;
                animateQuantityChange(quantityInput);
            }
        });
        
        increaseBtn.addEventListener('click', () => {
            const current = parseInt(quantityInput.value);
            const max = parseInt(quantityInput.max);
            if (current < max) {
                quantityInput.value = current + 1;
                animateQuantityChange(quantityInput);
            }
        });
    }
    
    function animateQuantityChange(input) {
        input.style.transform = 'scale(1.1)';
        setTimeout(() => {
            input.style.transform = 'scale(1)';
        }, 150);
    }

    // Size selection with motion feedback
    document.querySelectorAll('.size-label').forEach(label => {
        label.addEventListener('click', function() {
            // Remove active class from siblings
            const parent = this.closest('.size-grid, .size-options');
            parent.querySelectorAll('.size-label').forEach(sibling => {
                sibling.classList.remove('active');
            });
            
            // Add active class and animation
            this.classList.add('active');
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Cart page functionality
    
    // Quantity controls in cart
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const isIncrease = this.classList.contains('increase-btn');
            const input = document.querySelector(`input[data-item-id="${itemId}"]`);
            
            if (input) {
                const current = parseInt(input.value);
                const max = parseInt(input.max);
                let newValue = current;
                
                if (isIncrease && current < max) {
                    newValue = current + 1;
                } else if (!isIncrease && current > 1) {
                    newValue = current - 1;
                }
                
                if (newValue !== current) {
                    input.value = newValue;
                    updateCartItem(itemId, newValue);
                }
            }
        });
    });
    
    // Direct quantity input changes
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const newValue = parseInt(this.value);
            updateCartItem(itemId, newValue);
        });
    });
    
    // Remove item buttons
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            showRemoveConfirmation(itemId);
        });
    });
    
    function updateCartItem(itemId, quantity) {
        showLoadingOverlay(true);
        
        // Simulate API call - replace with actual endpoint
        setTimeout(() => {
            // Update the total for this item
            const totalElement = document.querySelector(`[data-item-id="${itemId}"].total-amount`);
            if (totalElement) {
                const price = parseFloat(totalElement.dataset.price);
                const newTotal = (price * quantity).toFixed(2);
                totalElement.textContent = `$${newTotal}`;
                
                // Animate the change
                totalElement.style.transform = 'scale(1.1)';
                totalElement.style.color = '#4CAF50';
                setTimeout(() => {
                    totalElement.style.transform = 'scale(1)';
                    totalElement.style.color = '#ffffff';
                }, 300);
            }
            
            updateCartTotals();
            showLoadingOverlay(false);
        }, 500);
    }
    
    function showRemoveConfirmation(itemId) {
        const modal = document.getElementById('removeModal');
        if (modal) {
            modal.style.display = 'block';
            
            const confirmBtn = document.getElementById('confirmRemove');
            const cancelBtn = document.getElementById('cancelRemove');
            
            confirmBtn.onclick = () => {
                removeCartItem(itemId);
                modal.style.display = 'none';
            };
            
            cancelBtn.onclick = () => {
                modal.style.display = 'none';
            };
        }
    }
    
    function removeCartItem(itemId) {
        const item = document.querySelector(`[data-item-id="${itemId}"].cart-item`);
        if (item) {
            item.style.animation = 'slideOut 0.5s ease forwards';
            setTimeout(() => {
                item.remove();
                updateCartTotals();
                showNotification('Item removed from cart', 'success');
            }, 500);
        }
    }
    
    function updateCartTotals() {
        // Calculate new totals - this would typically be done server-side
        let subtotal = 0;
        document.querySelectorAll('.total-amount').forEach(total => {
            subtotal += parseFloat(total.textContent.replace('$', ''));
        });
        
        const subtotalElement = document.getElementById('subtotalAmount');
        const totalElement = document.getElementById('totalAmount');
        
        if (subtotalElement) {
            subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        }
        if (totalElement) {
            totalElement.textContent = `$${subtotal.toFixed(2)}`;
        }
    }

    // Promo code functionality
    const promoBtn = document.getElementById('applyPromoBtn');
    const promoInput = document.getElementById('promoCodeInput');
    const promoMessage = document.getElementById('promoMessage');
    
    if (promoBtn && promoInput) {
        promoBtn.addEventListener('click', function() {
            const code = promoInput.value.trim().toUpperCase();
            
            if (!code) {
                showPromoMessage('Please enter a promo code', 'error');
                return;
            }
            
            // Simulate promo code validation
            const validCodes = ['CLAWS10', 'STREET15', 'NEWDROP20'];
            
            if (validCodes.includes(code)) {
                showPromoMessage('Promo code applied successfully!', 'success');
                // Apply discount logic here
            } else {
                showPromoMessage('Invalid promo code', 'error');
            }
        });
    }
    
    function showPromoMessage(message, type) {
        if (promoMessage) {
            promoMessage.textContent = message;
            promoMessage.className = `promo-message ${type}`;
            promoMessage.style.display = 'block';
            
            setTimeout(() => {
                promoMessage.style.display = 'none';
            }, 3000);
        }
    }

    // Checkout page functionality
    
    // Payment method toggle
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    const cardDetails = document.getElementById('cardDetails');
    
    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            if (cardDetails) {
                cardDetails.style.display = this.value === 'card' ? 'block' : 'none';
            }
        });
    });
    
    // Shipping method change
    const shippingMethods = document.querySelectorAll('input[name="shipping_method"]');
    const checkoutShipping = document.getElementById('checkoutShipping');
    const checkoutTotal = document.getElementById('checkoutTotal');
    
    shippingMethods.forEach(method => {
        method.addEventListener('change', function() {
            const shippingCost = this.value === 'standard' ? 0 : 
                                this.value === 'express' ? 15 : 35;
            
            if (checkoutShipping) {
                checkoutShipping.textContent = shippingCost === 0 ? 'FREE' : `$${shippingCost}.00`;
            }
            
            // Update total (this would be calculated server-side in reality)
            updateCheckoutTotal();
        });
    });
    
    function updateCheckoutTotal() {
        // This is a simplified calculation - real implementation would be server-side
        const subtotal = parseFloat(document.getElementById('checkoutSubtotal')?.textContent.replace('$', '') || '0');
        const shipping = document.getElementById('checkoutShipping')?.textContent === 'FREE' ? 0 : 
                        parseFloat(document.getElementById('checkoutShipping')?.textContent.replace('$', '') || '0');
        const tax = parseFloat(document.getElementById('checkoutTax')?.textContent.replace('$', '') || '0');
        
        const total = subtotal + shipping + tax;
        
        if (checkoutTotal) {
            checkoutTotal.textContent = `$${total.toFixed(2)}`;
        }
    }
    
    // Checkout form submission
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show processing modal
            const processingModal = document.getElementById('processingModal');
            if (processingModal) {
                processingModal.style.display = 'block';
            }
            
            // Simulate payment processing
            setTimeout(() => {
                if (processingModal) {
                    processingModal.style.display = 'none';
                }
                showNotification('Order placed successfully!', 'success');
                // Redirect to success page
            }, 3000);
        });
    }

    // Modal functionality
    
    // Size guide modal
    const sizeGuideBtn = document.getElementById('sizeGuideBtn');
    const sizeGuideModal = document.getElementById('sizeGuideModal');
    
    if (sizeGuideBtn && sizeGuideModal) {
        sizeGuideBtn.addEventListener('click', function(e) {
            e.preventDefault();
            sizeGuideModal.style.display = 'block';
        });
    }
    
    // Share modal
    const shareBtn = document.getElementById('shareBtn');
    const shareModal = document.getElementById('shareModal');
    
    if (shareBtn && shareModal) {
        shareBtn.addEventListener('click', function() {
            shareModal.style.display = 'block';
        });
    }
    
    // Copy link functionality
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(window.location.href).then(() => {
                showNotification('Link copied to clipboard!', 'success');
            });
        });
    }
    
    // Close modals
    document.querySelectorAll('.modal-close, .modal-overlay').forEach(element => {
        element.addEventListener('click', function() {
            const modal = this.closest('.quick-add-modal, .size-guide-modal, .share-modal, .remove-modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Quick add functionality
    document.querySelectorAll('.quick-add-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const productId = this.dataset.productId;
            showQuickAddModal(productId);
        });
    });
    
    function showQuickAddModal(productId) {
        const modal = document.getElementById('quickAddModal');
        if (modal) {
            // Populate modal with product data (would fetch from server in real app)
            modal.style.display = 'block';
            document.getElementById('modalProductId').value = productId;
        }
    }

    // Utility functions
    
    function setButtonLoading(button, loading) {
        if (loading) {
            button.dataset.originalText = button.textContent;
            button.textContent = 'ADDING...';
            button.style.background = '#666';
            button.disabled = true;
        } else {
            button.textContent = button.dataset.originalText;
            button.style.background = '#ffffff';
            button.disabled = false;
        }
    }
    
    function setButtonSuccess(button) {
        button.style.background = '#4CAF50';
        button.textContent = 'ADDED!';
        
        setTimeout(() => {
            button.style.background = '#ffffff';
            button.textContent = button.dataset.originalText;
            button.disabled = false;
        }, 2000);
    }
    
    function shakeElement(element) {
        if (element) {
            element.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                element.style.animation = '';
            }, 500);
        }
    }
    
    function showLoadingOverlay(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        }
    }
    
    // Enhanced notification system
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'success' ? '✓' : '⚠'}</span>
                <span class="notification-text">${message}</span>
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 120px;
            right: 30px;
            background: ${type === 'success' ? '#ffffff' : '#ff4444'};
            color: ${type === 'success' ? '#0d0d0d' : '#fff'};
            padding: 20px 25px;
            font-weight: 700;
            z-index: 10000;
            transform: translateX(120%) scale(0.8);
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0) scale(1)';
        }, 100);
        
        // Remove after 4 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(120%) scale(0.8)';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 400);
        }, 4000);
    }
    
    function updateCartCount() {
        // This would typically fetch the cart count from the server
        console.log('Cart updated');
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Enhanced hover effects for catalog items
    document.querySelectorAll('.catalog-item, .magazine-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Load more functionality
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            const btnText = this.querySelector('.btn-text');
            const btnLoader = this.querySelector('.btn-loader');
            
            btnText.style.display = 'none';
            btnLoader.style.display = 'block';
            
            // Simulate loading more products
            setTimeout(() => {
                btnText.style.display = 'block';
                btnLoader.style.display = 'none';
                showNotification('More products loaded!', 'success');
            }, 2000);
        });
    }
    
    // Staggered animation for grid items
    const gridItems = document.querySelectorAll('.catalog-item, .magazine-item');
    gridItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideOut {
            from { opacity: 1; transform: translateX(0); }
            to { opacity: 0; transform: translateX(-100%); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .notification-icon {
            font-size: 18px;
            font-weight: bold;
        }
        
        .promo-message {
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .promo-message.success {
            background: rgba(76, 175, 80, 0.2);
            color: #4CAF50;
            border: 1px solid rgba(76, 175, 80, 0.3);
        }
        
        .promo-message.error {
            background: rgba(244, 67, 54, 0.2);
            color: #F44336;
            border: 1px solid rgba(244, 67, 54, 0.3);
        }
    `;
    document.head.appendChild(style);
});