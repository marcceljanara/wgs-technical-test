<?= $this->extend('layouts/admin') ?>

<?= $this->section('content') ?>
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-primary text-white py-3">
                <h5 class="mb-0 fw-bold"><i class="fa-solid fa-plus me-2"></i>Create New Category</h5>
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

                <form action="<?= base_url('admin/categories/store') ?>" method="POST">
                    <?= csrf_field() ?>
                    <div class="mb-3">
                        <label for="name" class="form-label fw-bold">Category Name</label>
                        <input type="text" class="form-control" id="name" name="name" placeholder="e.g., Electronics, Fashion" value="<?= old('name') ?>" required>
                    </div>

                    <div class="d-flex justify-content-between mt-4">
                        <a href="<?= base_url('admin/categories') ?>" class="btn btn-secondary">
                            <i class="fa-solid fa-arrow-left me-1"></i> Cancel
                        </a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fa-solid fa-floppy-disk me-1"></i> Save Category
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
