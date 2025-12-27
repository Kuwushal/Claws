// Product Filtering and Sorting
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const sortSelect = document.getElementById('sortSelect');
    const productGrid = document.getElementById('productGrid');
    
    if (!productGrid) return;
    
    const products = Array.from(productGrid.querySelectorAll('.card'));

    // Filter functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            try {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.dataset.filter;
                if (!filter) return;
                
                products.forEach(product => {
                    const category = product.dataset.category;
                    
                    if (filter === 'all' || (category && category.includes(filter))) {
                        product.style.display = 'block';
                    } else {
                        product.style.display = 'none';
                    }
                });
            } catch (error) {
                console.error('Filter error:', error);
            }
        });
    });

    // Sort functionality
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            try {
                const sortValue = this.value;
                if (!sortValue) return;
                
                const sortedProducts = [...products].sort((a, b) => {
                    switch (sortValue) {
                        case 'price-low':
                            const priceA = parseFloat(a.dataset.price) || 0;
                            const priceB = parseFloat(b.dataset.price) || 0;
                            return priceA - priceB;
                        case 'price-high':
                            const priceA2 = parseFloat(a.dataset.price) || 0;
                            const priceB2 = parseFloat(b.dataset.price) || 0;
                            return priceB2 - priceA2;
                        case 'name':
                            const nameA = (a.dataset.name || '').toLowerCase();
                            const nameB = (b.dataset.name || '').toLowerCase();
                            return nameA.localeCompare(nameB);
                        default:
                            return 0;
                    }
                });
                
                sortedProducts.forEach(product => productGrid.appendChild(product));
            } catch (error) {
                console.error('Sort error:', error);
            }
        });
    }
});