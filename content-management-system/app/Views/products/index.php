<?= $this->extend('layouts/admin') ?>

<?= $this->section('content') ?>
<div class="card shadow-sm">
    <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
        <h5 class="mb-0 text-primary fw-bold"><i class="fa-solid fa-box me-2"></i>Product Inventory</h5>
        <a href="<?= base_url('admin/products/create') ?>" class="btn btn-primary btn-sm">
            <i class="fa-solid fa-plus me-1"></i> Add Product
        </a>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover table-striped align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Product Title</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Stock</th>
                        <th>Created At</th>
                        <th class="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (count($products) > 0) : ?>
                        <?php $no = 1; foreach ($products as $prod) : ?>
                            <tr>
                                <td><?= $no++ ?></td>
                                <td>
                                    <div class="fw-bold text-dark"><?= esc($prod['title']) ?></div>
                                    <small class="text-muted"><?= esc(substr($prod['description'] ?? '', 0, 50)) ?><?= strlen($prod['description'] ?? '') > 50 ? '...' : '' ?></small>
                                </td>
                                <td>
                                    <?php if ($prod['category_name']) : ?>
                                        <span class="badge bg-info text-dark"><?= esc($prod['category_name']) ?></span>
                                    <?php else : ?>
                                        <span class="badge bg-light text-muted border">Uncategorized</span>
                                    <?php endif; ?>
                                </td>
                                <td class="fw-bold text-success">Rp <?= number_format($prod['price'], 2, ',', '.') ?></td>
                                <td>
                                    <?php if ($prod['stock'] > 10) : ?>
                                        <span class="badge bg-success"><?= $prod['stock'] ?> pcs</span>
                                    <?php elseif ($prod['stock'] > 0) : ?>
                                        <span class="badge bg-warning text-dark"><?= $prod['stock'] ?> pcs (Low)</span>
                                    <?php else : ?>
                                        <span class="badge bg-danger">Out of Stock</span>
                                    <?php endif; ?>
                                </td>
                                <td><small class="text-muted"><?= date('d M Y H:i', strtotime($prod['created_at'])) ?></small></td>
                                <td class="text-center">
                                    <a href="<?= base_url('admin/products/edit/' . $prod['id']) ?>" class="btn btn-sm btn-outline-warning me-1" title="Edit">
                                        <i class="fa-solid fa-pen-to-square"></i> Edit
                                    </a>
                                    <a href="<?= base_url('admin/products/delete/' . $prod['id']) ?>" class="btn btn-sm btn-outline-danger" onclick="return confirm('Are you sure you want to delete this product? All transaction history for this product will remain, but the product item link will be cleared.');" title="Delete">
                                        <i class="fa-solid fa-trash"></i> Delete
                                    </a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    <?php else : ?>
                        <tr>
                            <td colspan="7" class="text-center text-muted py-4">No products found. Click "Add Product" to populate inventory.</td>
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
