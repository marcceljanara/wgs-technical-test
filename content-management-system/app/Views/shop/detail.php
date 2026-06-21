<?= $this->extend('layouts/shop') ?>

<?= $this->section('content') ?>
<div class="row">
    <!-- Left Column: Product Info -->
    <div class="col-md-6 mb-4">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-dark text-white py-3">
                <h5 class="mb-0 fw-bold"><i class="fa-solid fa-circle-info me-2"></i>Product Details</h5>
            </div>
            <div class="card-body p-4">
                <span class="badge bg-secondary mb-3 text-uppercase"><?= esc($product['category_name'] ?? 'General') ?></span>
                <h2 class="fw-bold text-dark mb-3"><?= esc($product['title']) ?></h2>
                <h3 class="text-success fw-bold mb-4">Rp <?= number_format($product['price'], 2, ',', '.') ?></h3>
                
                <hr>
                
                <h5 class="fw-bold text-muted mt-3 mb-2">Description</h5>
                <p class="text-dark fs-6" style="white-space: pre-wrap;"><?= esc($product['description'] ?: 'No description provided for this product.') ?></p>
                
                <hr>
                
                <div class="d-flex align-items-center mt-3">
                    <span class="text-muted me-3">Stock Available:</span>
                    <strong class="fs-5 text-primary"><i class="fa-solid fa-boxes-stacked me-1"></i><?= $product['stock'] ?> units</strong>
                </div>
            </div>
        </div>
    </div>

    <!-- Right Column: Purchase Form -->
    <div class="col-md-6 mb-4">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-primary text-white py-3">
                <h5 class="mb-0 fw-bold"><i class="fa-solid fa-credit-card me-2"></i>Simulate Checkout</h5>
            </div>
            <div class="card-body p-4">
                <!-- Validation & Error Alerts -->
                <?php if (session()->getFlashdata('errors')) : ?>
                    <div class="alert alert-danger pb-0">
                        <ul>
                            <?php foreach (session()->getFlashdata('errors') as $error) : ?>
                                <li><?= esc($error) ?></li>
                            <?php endforeach; ?>
                        </ul>
                    </div>
                <?php endif; ?>

                <form action="<?= base_url('checkout') ?>" method="POST" id="checkout-form">
                    <?= csrf_field() ?>
                    <input type="hidden" name="product_id" value="<?= $product['id'] ?>">

                    <div class="mb-3">
                        <label for="customer_name" class="form-label fw-bold">Your Name</label>
                        <input type="text" class="form-control" id="customer_name" name="customer_name" placeholder="e.g. John Doe" value="<?= old('customer_name') ?>" required>
                    </div>

                    <div class="mb-3">
                        <label for="customer_email" class="form-label fw-bold">Your Email</label>
                        <input type="email" class="form-control" id="customer_email" name="customer_email" placeholder="e.g. john.doe@example.com" value="<?= old('customer_email') ?>" required>
                    </div>

                    <div class="mb-3">
                        <label for="quantity" class="form-label fw-bold">Quantity (Units)</label>
                        <input type="number" class="form-control" id="quantity" name="quantity" min="1" max="<?= $product['stock'] ?>" value="<?= old('quantity', 1) ?>" required>
                        <div class="form-text text-muted">Maximum order limit is the remaining stock (<?= $product['stock'] ?>).</div>
                    </div>

                    <!-- Dynamic Subtotal Calculator -->
                    <div class="bg-light p-3 rounded mb-4 border">
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="text-muted fw-bold">Simulated Total Amount:</span>
                            <span class="fs-4 fw-bold text-success" id="subtotal-display">Rp <?= number_format($product['price'], 2, ',', '.') ?></span>
                        </div>
                    </div>

                    <div class="d-flex justify-content-between">
                        <a href="<?= base_url('shop') ?>" class="btn btn-secondary">
                            <i class="fa-solid fa-arrow-left me-1"></i> Back to Shop
                        </a>
                        <button type="submit" class="btn btn-success fw-bold">
                            <i class="fa-solid fa-basket-shopping me-1"></i> Complete Purchase
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const quantityInput = document.getElementById('quantity');
        const subtotalDisplay = document.getElementById('subtotal-display');
        const price = <?= $product['price'] ?>;

        function updateSubtotal() {
            let qty = parseInt(quantityInput.value);
            if (isNaN(qty) || qty < 1) {
                qty = 1;
            }
            const total = price * qty;
            
            // Format to Indonesian Rupiah representation
            const formattedTotal = new Intl.NumberFormat('id-ID', {
                style: 'currency',
                currency: 'IDR',
                minimumFractionDigits: 2
            }).format(total);

            subtotalDisplay.textContent = formattedTotal;
        }

        quantityInput.addEventListener('input', updateSubtotal);
        quantityInput.addEventListener('change', updateSubtotal);
    });
</script>
<?= $this->endSection() ?>
