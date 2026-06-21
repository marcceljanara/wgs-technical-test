<?= $this->extend('layouts/admin') ?>

<?= $this->section('content') ?>
<div class="card shadow-sm">
    <div class="card-header bg-white py-3">
        <h5 class="mb-0 text-primary fw-bold"><i class="fa-solid fa-cart-shopping me-2"></i>Incoming Orders</h5>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover table-striped align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Email</th>
                        <th>Total Amount</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th class="text-center">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (count($orders) > 0) : ?>
                        <?php foreach ($orders as $ord) : ?>
                            <tr>
                                <td class="fw-bold">#<?= esc(substr($ord['id'], 0, 8)) ?></td>
                                <td><?= esc($ord['customer_name']) ?></td>
                                <td><?= esc($ord['customer_email']) ?></td>
                                <td class="fw-bold text-dark">Rp <?= number_format($ord['total_amount'], 2, ',', '.') ?></td>
                                <td>
                                    <?php if ($ord['status'] === 'PENDING') : ?>
                                        <span class="badge bg-warning text-dark"><i class="fa-regular fa-clock me-1"></i>PENDING</span>
                                    <?php elseif ($ord['status'] === 'PAID') : ?>
                                        <span class="badge bg-success"><i class="fa-solid fa-circle-check me-1"></i>PAID</span>
                                    <?php else : ?>
                                        <span class="badge bg-danger"><i class="fa-solid fa-circle-xmark me-1"></i>CANCELLED</span>
                                    <?php endif; ?>
                                </td>
                                <td><small class="text-muted"><?= date('d M Y H:i', strtotime($ord['created_at'])) ?></small></td>
                                <td class="text-center">
                                    <a href="<?= base_url('admin/orders/view/' . $ord['id']) ?>" class="btn btn-sm btn-outline-primary" title="View Details">
                                        <i class="fa-solid fa-eye me-1"></i> View
                                    </a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    <?php else : ?>
                        <tr>
                            <td colspan="7" class="text-center text-muted py-4">No orders received yet. Perform simulated purchase in Shop catalog.</td>
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
