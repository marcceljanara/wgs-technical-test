<?= $this->extend('layouts/admin') ?>

<?= $this->section('content') ?>
<div class="card shadow-sm">
    <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
        <h5 class="mb-0 text-primary fw-bold"><i class="fa-solid fa-list me-2"></i>Category List</h5>
        <a href="<?= base_url('admin/categories/create') ?>" class="btn btn-primary btn-sm">
            <i class="fa-solid fa-plus me-1"></i> Add Category
        </a>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover table-striped align-middle">
                <thead class="table-dark">
                    <tr>
                        <th style="width: 10%;">#</th>
                        <th style="width: 40%;">Category Name</th>
                        <th style="width: 30%;">Slug</th>
                        <th style="width: 20%;" class="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (count($categories) > 0) : ?>
                        <?php $no = 1; foreach ($categories as $cat) : ?>
                            <tr>
                                <td><?= $no++ ?></td>
                                <td class="fw-bold"><?= esc($cat['name']) ?></td>
                                <td><span class="badge bg-light text-dark text-lowercase border"><?= esc($cat['slug']) ?></span></td>
                                <td class="text-center">
                                    <a href="<?= base_url('admin/categories/edit/' . $cat['id']) ?>" class="btn btn-sm btn-outline-warning me-1" title="Edit">
                                        <i class="fa-solid fa-pen-to-square"></i> Edit
                                    </a>
                                    <a href="<?= base_url('admin/categories/delete/' . $cat['id']) ?>" class="btn btn-sm btn-outline-danger" onclick="return confirm('Are you sure you want to delete this category? All products under this category will have their category cleared.');" title="Delete">
                                        <i class="fa-solid fa-trash"></i> Delete
                                    </a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    <?php else : ?>
                        <tr>
                            <td colspan="4" class="text-center text-muted py-4">No categories found. Click "Add Category" to create one.</td>
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
