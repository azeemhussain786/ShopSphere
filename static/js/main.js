/**
 * ShopSphere - Interactive Client Logic & Cart Management
 * Handles:
 * 1. Cart Drawer (Open, Close, Backdrop click, Escape key)
 * 2. In-Memory Cart State (Add, Increment, Decrement, Remove, Recalculate Subtotal/Total)
 * 3. Dynamic Toast Notifications
 * 4. Product Search, Category Filtering, and Price/Rating Sorting
 * 5. Demo Checkout Flow (Validation, Modal, Simulated Order Confirmation)
 * 6. Robust Event Delegation for reliable Selenium automation
 */

document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // State
    // ==========================================
    let cart = []; // Array of { id, name, price, quantity, image_url }
    let toastTimer = null;

    // ==========================================
    // DOM Elements
    // ==========================================
    // Nav & Cart Elements
    const navCartBtn = document.getElementById('nav-cart-btn');
    const cartBadge = document.getElementById('cart-count');
    const cartBackdrop = document.getElementById('cart-backdrop');
    const cartDrawer = document.getElementById('cart-drawer');
    const cartCloseBtn = document.getElementById('cart-close-btn');
    const cartItemsTotalBadge = document.getElementById('cart-items-total-badge');
    const cartEmptyState = document.getElementById('cart-empty-state');
    const cartItemsContainer = document.getElementById('cart-items-container');
    const cartDrawerFooter = document.getElementById('cart-drawer-footer');
    const cartSubtotalElem = document.getElementById('cart-subtotal');
    const cartTotalElem = document.getElementById('cart-total');
    const cartCheckoutBtn = document.getElementById('cart-checkout-btn');
    const cartStartShoppingBtn = document.getElementById('cart-start-shopping-btn');

    // Checkout Modal Elements
    const checkoutModalBackdrop = document.getElementById('checkout-modal-backdrop');
    const checkoutModal = document.getElementById('checkout-modal');
    const checkoutModalCloseBtn = document.getElementById('checkout-modal-close-btn');
    const checkoutFormView = document.getElementById('checkout-form-view');
    const checkoutSuccessView = document.getElementById('checkout-success-view');
    const checkoutSummaryTotal = document.getElementById('checkout-summary-total');
    const checkoutSummaryItemsCount = document.getElementById('checkout-summary-items-count');
    const checkoutNameInput = document.getElementById('checkout-name');
    const checkoutAddressInput = document.getElementById('checkout-address');
    const placeOrderBtn = document.getElementById('place-order-btn');
    const orderContinueBtn = document.getElementById('order-continue-btn');
    const confirmedOrderId = document.getElementById('confirmed-order-id');
    const confirmedCustomerName = document.getElementById('confirmed-customer-name');
    const confirmedOrderTotal = document.getElementById('confirmed-order-total');
    const confirmedPaymentMethod = document.getElementById('confirmed-payment-method');

    // Toast Elements
    const toast = document.getElementById('notification-toast');
    const toastMessage = document.getElementById('toast-message');

    // Catalogue, Filter & Search Elements
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const sortSelect = document.getElementById('sort-select');
    const productCountElem = document.getElementById('product-count');
    const filterButtons = document.querySelectorAll('.filter-pill');
    const productsGrid = document.getElementById('products-grid');
    const noProductsMsg = document.getElementById('no-products-msg');

    // ==========================================
    // Toast Notification Utility
    // ==========================================
    function showToast(message) {
        if (!toast || !toastMessage) return;

        if (toastTimer) {
            clearTimeout(toastTimer);
        }

        toastMessage.textContent = message;
        toast.classList.remove('hidden');

        toastTimer = setTimeout(() => {
            toast.classList.add('hidden');
        }, 3000);
    }

    // ==========================================
    // Cart Drawer Controls (Open / Close)
    // ==========================================
    function openCart() {
        if (!cartDrawer || !cartBackdrop) return;
        cartBackdrop.classList.remove('hidden');
        cartDrawer.classList.add('open');
        document.body.classList.add('drawer-open');
        renderCart();
    }

    function closeCart() {
        if (!cartDrawer || !cartBackdrop) return;
        cartBackdrop.classList.add('hidden');
        cartDrawer.classList.remove('open');
        document.body.classList.remove('drawer-open');
    }

    if (navCartBtn) {
        navCartBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openCart();
        });
    }

    if (cartCloseBtn) {
        cartCloseBtn.addEventListener('click', (e) => {
            e.preventDefault();
            closeCart();
        });
    }

    if (cartStartShoppingBtn) {
        cartStartShoppingBtn.addEventListener('click', (e) => {
            e.preventDefault();
            closeCart();
            const catalogueSection = document.getElementById('catalogue');
            if (catalogueSection) {
                catalogueSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    if (cartBackdrop) {
        cartBackdrop.addEventListener('click', () => {
            closeCart();
        });
    }

    // Prevent clicks inside drawer from triggering backdrop close
    if (cartDrawer) {
        cartDrawer.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // Close drawer / modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (checkoutModal && !checkoutModal.classList.contains('hidden')) {
                closeCheckoutModal();
            } else if (cartDrawer && cartDrawer.classList.contains('open')) {
                closeCart();
            }
        }
    });

    // ==========================================
    // Cart State & Calculations
    // ==========================================
    function updateCartBadge() {
        const totalItemsCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        if (cartBadge) {
            cartBadge.textContent = totalItemsCount;
            // Brief visual bump
            cartBadge.style.transform = 'scale(1.25)';
            setTimeout(() => {
                cartBadge.style.transform = 'scale(1)';
            }, 200);
        }
        if (cartItemsTotalBadge) {
            cartItemsTotalBadge.textContent = `${totalItemsCount} item${totalItemsCount === 1 ? '' : 's'}`;
        }
    }

    function renderCart() {
        if (!cartItemsContainer || !cartEmptyState || !cartDrawerFooter) return;

        updateCartBadge();

        if (cart.length === 0) {
            // Display empty state
            cartEmptyState.classList.remove('hidden');
            cartItemsContainer.classList.add('hidden');
            cartDrawerFooter.classList.add('hidden');
            cartItemsContainer.innerHTML = '';
            return;
        }

        // Display populated cart
        cartEmptyState.classList.add('hidden');
        cartItemsContainer.classList.remove('hidden');
        cartDrawerFooter.classList.remove('hidden');

        let subtotal = 0;
        let itemsHtml = '';

        cart.forEach(item => {
            const itemSubtotal = item.price * item.quantity;
            subtotal += itemSubtotal;

            const fallbackSvg = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='68' height='68' fill='%23e2e8f0'><rect width='68' height='68'/><text x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%230284c7' font-family='sans-serif' font-size='10'>Item</text></svg>";

            itemsHtml += `
                <div class="cart-item" id="cart-item-${item.id}" data-testid="cart-item" data-id="${item.id}">
                    <img 
                        src="${item.image_url}" 
                        alt="${item.name}" 
                        class="cart-item-img" 
                        onerror="this.onerror=null; this.src='${fallbackSvg}';"
                    />
                    <div class="cart-item-details">
                        <div class="cart-item-name" id="cart-item-name-${item.id}" data-testid="cart-item-name" title="${item.name}">
                            ${item.name}
                        </div>
                        <div class="cart-item-price" id="cart-item-price-${item.id}" data-testid="cart-item-price">
                            ₹${item.price.toLocaleString('en-IN')} each
                        </div>
                        <div class="cart-item-bottom">
                            <div class="qty-stepper">
                                <button 
                                    class="btn-qty btn-qty-minus" 
                                    id="qty-minus-${item.id}" 
                                    data-testid="qty-minus-btn" 
                                    data-id="${item.id}" 
                                    aria-label="Decrease quantity"
                                >&minus;</button>
                                <span class="qty-display" id="qty-val-${item.id}" data-testid="qty-value">${item.quantity}</span>
                                <button 
                                    class="btn-qty btn-qty-plus" 
                                    id="qty-plus-${item.id}" 
                                    data-testid="qty-plus-btn" 
                                    data-id="${item.id}" 
                                    aria-label="Increase quantity"
                                >&plus;</button>
                            </div>
                            <span class="cart-item-subtotal" id="cart-item-subtotal-${item.id}" data-testid="cart-item-subtotal">
                                ₹${itemSubtotal.toLocaleString('en-IN')}
                            </span>
                        </div>
                    </div>
                    <button 
                        class="btn-remove-item" 
                        id="cart-remove-${item.id}" 
                        data-testid="cart-remove-btn" 
                        data-id="${item.id}" 
                        title="Remove item" 
                        aria-label="Remove ${item.name}"
                    >&times;</button>
                </div>
            `;
        });

        cartItemsContainer.innerHTML = itemsHtml;

        // Recalculate and update subtotal & total
        if (cartSubtotalElem) {
            cartSubtotalElem.textContent = `₹${subtotal.toLocaleString('en-IN')}`;
        }
        if (cartTotalElem) {
            cartTotalElem.textContent = `₹${subtotal.toLocaleString('en-IN')}`;
        }
    }

    function addToCart(product) {
        const existingItem = cart.find(item => item.id === product.id);

        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: product.id,
                name: product.name,
                price: product.price,
                quantity: 1,
                image_url: product.image_url
            });
        }

        updateCartBadge();

        if (cartDrawer && cartDrawer.classList.contains('open')) {
            renderCart();
        }

        showToast(`Added "${product.name}" to cart!`);
    }

    function updateQuantity(productId, delta) {
        const itemIndex = cart.findIndex(item => item.id === productId);
        if (itemIndex === -1) return;

        const item = cart[itemIndex];
        const newQty = item.quantity + delta;

        if (newQty <= 0) {
            const removedName = item.name;
            cart.splice(itemIndex, 1);
            showToast(`Removed "${removedName}" from cart`);
        } else {
            item.quantity = newQty;
        }

        renderCart();
    }

    function removeItem(productId) {
        const itemIndex = cart.findIndex(item => item.id === productId);
        if (itemIndex === -1) return;

        const removedName = cart[itemIndex].name;
        cart.splice(itemIndex, 1);
        showToast(`Removed "${removedName}" from cart`);
        renderCart();
    }

    // ==========================================
    // Event Delegation: Cart Actions (+, -, Remove)
    // ==========================================
    if (cartItemsContainer) {
        cartItemsContainer.addEventListener('click', (e) => {
            const plusBtn = e.target.closest('.btn-qty-plus');
            const minusBtn = e.target.closest('.btn-qty-minus');
            const removeBtn = e.target.closest('.btn-remove-item');

            if (plusBtn) {
                const id = parseInt(plusBtn.getAttribute('data-id'), 10);
                updateQuantity(id, 1);
                return;
            }

            if (minusBtn) {
                const id = parseInt(minusBtn.getAttribute('data-id'), 10);
                updateQuantity(id, -1);
                return;
            }

            if (removeBtn) {
                const id = parseInt(removeBtn.getAttribute('data-id'), 10);
                removeItem(id);
                return;
            }
        });
    }

    // ==========================================
    // Demo Checkout Logic & Modal
    // ==========================================
    function openCheckoutModal() {
        if (!checkoutModal || !checkoutModalBackdrop) return;

        const totalItemsCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        if (checkoutSummaryTotal) {
            checkoutSummaryTotal.textContent = `₹${subtotal.toLocaleString('en-IN')}`;
        }
        if (checkoutSummaryItemsCount) {
            checkoutSummaryItemsCount.textContent = `${totalItemsCount} item${totalItemsCount === 1 ? '' : 's'}`;
        }

        // Show form view, hide success view
        if (checkoutFormView) checkoutFormView.classList.remove('hidden');
        if (checkoutSuccessView) checkoutSuccessView.classList.add('hidden');

        checkoutModalBackdrop.classList.remove('hidden');
        checkoutModal.classList.remove('hidden');
        document.body.classList.add('modal-open');
    }

    function closeCheckoutModal() {
        if (!checkoutModal || !checkoutModalBackdrop) return;
        checkoutModalBackdrop.classList.add('hidden');
        checkoutModal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }

    if (cartCheckoutBtn) {
        cartCheckoutBtn.addEventListener('click', () => {
            // Priority 7: Validate cart before proceeding
            if (cart.length === 0) {
                showToast('Your cart is empty! Add products before checkout.');
                return;
            }
            openCheckoutModal();
        });
    }

    if (checkoutModalCloseBtn) {
        checkoutModalCloseBtn.addEventListener('click', () => {
            closeCheckoutModal();
        });
    }

    if (checkoutModalBackdrop) {
        checkoutModalBackdrop.addEventListener('click', () => {
            closeCheckoutModal();
        });
    }

    if (checkoutModal) {
        checkoutModal.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // Payment method selector highlight
    const paymentRadios = document.querySelectorAll('input[name="payment-method"]');
    paymentRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            document.querySelectorAll('.payment-card').forEach(card => card.classList.remove('selected'));
            radio.closest('.payment-card').classList.add('selected');
        });
    });

    // Place Demo Order Handler
    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', () => {
            const name = (checkoutNameInput ? checkoutNameInput.value.trim() : '') || 'Valued Customer';
            const address = checkoutAddressInput ? checkoutAddressInput.value.trim() : '';

            if (!name) {
                showToast('Please enter your name.');
                if (checkoutNameInput) checkoutNameInput.focus();
                return;
            }

            if (!address) {
                showToast('Please enter your delivery address.');
                if (checkoutAddressInput) checkoutAddressInput.focus();
                return;
            }

            const totalAmount = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
            const orderIdNum = Math.floor(10000 + Math.random() * 90000);
            const orderIdStr = `SP-${orderIdNum}`;

            const selectedPaymentRadio = document.querySelector('input[name="payment-method"]:checked');
            const paymentMode = selectedPaymentRadio && selectedPaymentRadio.value === 'upi' ? 'UPI Simulation' : 'Cash on Delivery';

            // Populate success receipt
            if (confirmedOrderId) confirmedOrderId.textContent = orderIdStr;
            if (confirmedCustomerName) confirmedCustomerName.textContent = name;
            if (confirmedOrderTotal) confirmedOrderTotal.textContent = `₹${totalAmount.toLocaleString('en-IN')}`;
            if (confirmedPaymentMethod) confirmedPaymentMethod.textContent = paymentMode;

            // Clear cart state
            cart = [];
            renderCart();
            closeCart();

            // Transition to success confirmation view
            if (checkoutFormView) checkoutFormView.classList.add('hidden');
            if (checkoutSuccessView) checkoutSuccessView.classList.remove('hidden');

            showToast(`Order ${orderIdStr} placed successfully! (Demo)`);
        });
    }

    if (orderContinueBtn) {
        orderContinueBtn.addEventListener('click', () => {
            closeCheckoutModal();
            const catalogueSection = document.getElementById('catalogue');
            if (catalogueSection) {
                catalogueSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // ==========================================
    // Event Delegation: Add to Cart Buttons
    // ==========================================
    if (productsGrid) {
        productsGrid.addEventListener('click', (e) => {
            const addBtn = e.target.closest('.btn-add-cart');
            if (!addBtn) return;

            const id = parseInt(addBtn.getAttribute('data-product-id'), 10);
            const name = addBtn.getAttribute('data-product-name') || 'Item';
            const price = parseFloat(addBtn.getAttribute('data-product-price')) || 0;
            const imageUrl = addBtn.getAttribute('data-product-image') || '';

            addToCart({
                id: id,
                name: name,
                price: price,
                image_url: imageUrl
            });
        });
    }

    // ==========================================
    // Search, Filter & Sort Logic
    // ==========================================
    function filterAndSortProducts() {
        const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
        const activeCategoryBtn = document.querySelector('.filter-pill.active');
        const selectedCategory = activeCategoryBtn ? activeCategoryBtn.getAttribute('data-category') : 'all';
        const sortValue = sortSelect ? sortSelect.value : 'default';

        const cards = Array.from(productsGrid ? productsGrid.querySelectorAll('.product-card') : []);
        let visibleCards = [];

        // Filter cards
        cards.forEach(card => {
            const titleElem = card.querySelector('.product-title');
            const descElem = card.querySelector('.product-desc');
            const cardCategory = card.getAttribute('data-category') || '';

            const title = titleElem ? titleElem.textContent.toLowerCase() : '';
            const desc = descElem ? descElem.textContent.toLowerCase() : '';

            const matchesQuery = !query || title.includes(query) || desc.includes(query) || cardCategory.toLowerCase().includes(query);
            const matchesCategory = (selectedCategory === 'all') || (cardCategory.toLowerCase() === selectedCategory.toLowerCase());

            if (matchesQuery && matchesCategory) {
                card.classList.remove('hidden');
                visibleCards.push(card);
            } else {
                card.classList.add('hidden');
            }
        });

        // Sort visible cards
        if (productsGrid && visibleCards.length > 0) {
            visibleCards.sort((a, b) => {
                const priceA = parseFloat(a.getAttribute('data-price')) || 0;
                const priceB = parseFloat(b.getAttribute('data-price')) || 0;
                const ratingA = parseFloat(a.getAttribute('data-rating')) || 0;
                const ratingB = parseFloat(b.getAttribute('data-rating')) || 0;
                const idA = parseInt(a.getAttribute('data-id'), 10) || 0;
                const idB = parseInt(b.getAttribute('data-id'), 10) || 0;

                switch (sortValue) {
                    case 'price-low':
                        return priceA - priceB;
                    case 'price-high':
                        return priceB - priceA;
                    case 'rating-high':
                        return ratingB - ratingA;
                    case 'default':
                    default:
                        return idA - idB;
                }
            });

            // Re-append visible cards in sorted order to the grid
            visibleCards.forEach(card => productsGrid.appendChild(card));
        }

        // Update product count label
        if (productCountElem) {
            const catLabel = selectedCategory === 'all' ? '' : ` in "${selectedCategory}"`;
            productCountElem.textContent = `Showing ${visibleCards.length} product${visibleCards.length === 1 ? '' : 's'}${catLabel}`;
        }

        // Toggle 'No products found' banner
        if (noProductsMsg) {
            if (visibleCards.length === 0) {
                noProductsMsg.classList.remove('hidden');
            } else {
                noProductsMsg.classList.add('hidden');
            }
        }
    }

    // Filter Buttons Click Handling
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            filterAndSortProducts();
        });
    });

    // Search Input Handling
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            filterAndSortProducts();
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                filterAndSortProducts();
            }
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            filterAndSortProducts();
        });
    }

    // Sort Dropdown Handling
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            filterAndSortProducts();
        });
    }

    // Initial render
    updateCartBadge();
});
