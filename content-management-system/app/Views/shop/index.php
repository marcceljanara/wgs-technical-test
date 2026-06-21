<?= $this->extend('layouts/shop') ?>

<?= $this->section('content') ?>
<!-- Hero Header -->
<div class="p-5 mb-4 bg-light rounded-3 border">
    <div class="container-fluid py-2">
        <h1 class="display-5 fw-bold text-dark"><i class="fa-solid fa-cart-arrow-down text-primary me-2"></i>Product Store Simulation</h1>
        <p class="col-md-8 fs-5 text-muted">This page simulates a buyer's experience. Browse products, choose items, and check out without logging in. The system will log transactions, update stock, and track UUID associations automatically.</p>
    </div>
</div>

<div class="row">
    <!-- Category Filter Sidebar -->
    <div class="col-md-3 mb-4">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-dark text-white py-3">
                <h5 class="mb-0 fw-bold"><i class="fa-solid fa-filter me-2"></i>Filter Categories</h5>
            </div>
            <div class="list-group list-group-flush">
                <a href="<?= base_url('shop') ?>" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center <?= empty($selectedCategory) ? 'active bg-primary border-primary' : '' ?>">
                    All Categories
                    <i class="fa-solid fa-angles-right"></i>
                </a>
                <?php foreach ($categories as $cat) : ?>
                    <a href="<?= base_url('shop?category=' . $cat['id']) ?>" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center <?= $selectedCategory === $cat['id'] ? 'active bg-primary border-primary' : '' ?>">
                        <?= esc($cat['name']) ?>
                        <i class="fa-solid fa-angles-right"></i>
                    </a>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <!-- Product Grid Catalog -->
    <div class="col-md-9">
        <div class="row">
            <?php if (count($products) > 0) : ?>
                <?php foreach ($products as $prod) : ?>
                    <div class="col-md-4 mb-4">
                        <div class="card h-100 shadow-sm hover-shadow border">
                            <div class="card-body d-flex flex-column">
                                <span class="badge bg-secondary mb-2 align-self-start text-uppercase">
                                    <?= esc($prod['category_name'] ?? 'General') ?>
                                </span>
                                <h5 class="card-title fw-bold text-dark mb-1"><?= esc($prod['title']) ?></h5>
                                <p class="card-text text-muted flex-grow-1 small mt-2">
                                    <?= esc(substr($prod['description'] ?? '', 0, 100)) ?><?= strlen($prod['description'] ?? '') > 100 ? '...' : '' ?>
                                </p>
                                
                                <div class="mt-3">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <h5 class="text-success fw-bold mb-0">Rp <?= number_format($prod['price'], 2, ',', '.') ?></h5>
                                        <small class="text-muted"><i class="fa-solid fa-boxes-stacked me-1"></i>Stock: <?= $prod['stock'] ?></small>
                                    </div>
                                    <a href="<?= base_url('shop/product/' . $prod['id']) ?>" class="btn btn-primary w-100 fw-bold">
                                        <i class="fa-solid fa-cart-plus me-1"></i> Buy Product
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php else : ?>
                <div class="col-12">
                    <div class="card p-5 text-center shadow-sm">
                        <i class="fa-solid fa-magnifying-glass fs-1 text-muted mb-3"></i>
                        <h4>No Products Available</h4>
                        <p class="text-muted mb-0">There are either no products created, or they are out of stock. Go to <a href="<?= base_url('admin/products') ?>">Admin Dashboard</a> to add products and increase stock.</p>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
