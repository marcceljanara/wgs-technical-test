<?= $this->extend('layouts/admin') ?>

<?= $this->section('content') ?>
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-warning text-dark py-3">
                <h5 class="mb-0 fw-bold"><i class="fa-solid fa-pen-to-square me-2"></i>Edit Product</h5>
            </div>
            <div class="card-body p-4">
                <!-- Errors Alert -->
                <?php if (session()->getFlashdata('errors')) : ?>
                    <div class="alert alert-danger pb-0">
                        <ul>
                            <?php foreach (session()->getFlashdata('errors') as $error) : ?>
                                <li><?= esc($error) ?></li>
                            <?php endforeach; ?>
                        </ul>
                    </div>
                <?php endif; ?>

                <form action="<?= base_url('admin/products/update/' . $product['id']) ?>" method="POST">
                    <?= csrf_field() ?>
                    
                    <div class="mb-3">
                        <label for="title" class="form-label fw-bold">Product Title</label>
                        <input type="text" class="form-control" id="title" name="title" placeholder="e.g., iPhone 14 Pro" value="<?= old('title', $product['title']) ?>" required>
                    </div>

                    <div class="mb-3">
                        <label for="category_id" class="form-label fw-bold">Category</label>
                        <select class="form-select" id="category_id" name="category_id">
                            <option value="">-- Choose Category (Optional) --</option>
                            <?php foreach ($categories as $cat) : ?>
                                <option value="<?= $cat['id'] ?>" <?= old('category_id', $product['category_id']) === $cat['id'] ? 'selected' : '' ?>><?= esc($cat['name']) ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>

                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="price" class="form-label fw-bold">Price (IDR)</label>
                            <div class="input-group">
                                <span class="input-group-text">Rp</span>
                                <input type="number" step="0.01" class="form-control" id="price" name="price" placeholder="e.g. 15000000" value="<?= old('price', $product['price']) ?>" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label for="stock" class="form-label fw-bold">Available Stock</label>
                            <input type="number" class="form-control" id="stock" name="stock" placeholder="e.g. 25" value="<?= old('stock', $product['stock']) ?>" required>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="description" class="form-label fw-bold">Description</label>
                        <textarea class="form-control" id="description" name="description" rows="4" placeholder="Detailed product specifications..."><?= old('description', $product['description']) ?></textarea>
                    </div>

                    <div class="d-flex justify-content-between mt-4">
                        <a href="<?= base_url('admin/products') ?>" class="btn btn-secondary">
                            <i class="fa-solid fa-arrow-left me-1"></i> Cancel
                        </a>
                        <button type="submit" class="btn btn-warning text-dark fw-bold">
                            <i class="fa-solid fa-floppy-disk me-1"></i> Update Product
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
