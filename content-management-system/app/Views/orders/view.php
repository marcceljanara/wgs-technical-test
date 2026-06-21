<?= $this->extend('layouts/admin') ?>

<?= $this->section('content') ?>
<div class="row">
    <!-- Left Column - Order Items -->
    <div class="col-lg-8 mb-4">
        <div class="card shadow-sm mb-4">
            <div class="card-header bg-white py-3">
                <h5 class="mb-0 text-primary fw-bold"><i class="fa-solid fa-list me-2"></i>Ordered Items</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>Product</th>
                                <th class="text-end">Price at Purchase</th>
                                <th class="text-center">Qty</th>
                                <th class="text-end">Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($items as $item) : ?>
                                <tr>
                                    <td>
                                        <div class="fw-bold">
                                            <?= $item['product_title'] ? esc($item['product_title']) : '<span class="text-muted">Deleted Product</span>' ?>
                                        </div>
                                    </td>
                                    <td class="text-end">Rp <?= number_format($item['price_at_purchase'], 2, ',', '.') ?></td>
                                    <td class="text-center"><?= $item['quantity'] ?></td>
                                    <td class="text-end fw-bold">Rp <?= number_format($item['price_at_purchase'] * $item['quantity'], 2, ',', '.') ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                        <tfoot>
                            <tr class="table-light border-top">
                                <td colspan="3" class="text-end fw-bold">Total Amount:</td>
                                <td class="text-end fw-bold text-success fs-5">Rp <?= number_format($order['total_amount'], 2, ',', '.') ?></td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </div>

        <a href="<?= base_url('admin/orders') ?>" class="btn btn-secondary">
            <i class="fa-solid fa-arrow-left me-1"></i> Back to Orders
        </a>
    </div>

    <!-- Right Column - Customer Info & Status Change -->
    <div class="col-lg-4">
        <!-- Customer Info Card -->
        <div class="card shadow-sm mb-4">
            <div class="card-header bg-dark text-white py-3">
                <h5 class="mb-0 fw-bold"><i class="fa-solid fa-user me-2"></i>Customer Info</h5>
            </div>
            <div class="card-body">
                <p class="mb-1 text-muted">Customer Name:</p>
                <h6 class="fw-bold mb-3"><?= esc($order['customer_name']) ?></h6>
                
                <p class="mb-1 text-muted">Customer Email:</p>
                <h6 class="fw-bold mb-3"><a href="mailto:<?= esc($order['customer_email']) ?>"><?= esc($order['customer_email']) ?></a></h6>

                <p class="mb-1 text-muted">Order Date:</p>
                <h6 class="fw-bold mb-3"><?= date('d F Y H:i:s', strtotime($order['created_at'])) ?></h6>

                <p class="mb-1 text-muted">Order ID (UUID):</p>
                <code class="text-break fs-7"><?= esc($order['id']) ?></code>
            </div>
        </div>

        <!-- Status Editor Card -->
        <div class="card shadow-sm">
            <div class="card-header bg-white py-3">
                <h5 class="mb-0 text-primary fw-bold"><i class="fa-solid fa-pen-fancy me-2"></i>Update Order Status</h5>
            </div>
            <div class="card-body">
                <form action="<?= base_url('admin/orders/update-status/' . $order['id']) ?>" method="POST">
                    <?= csrf_field() ?>
                    <div class="mb-3">
                        <label for="status" class="form-label text-muted">Current Status:</label>
                        <select class="form-select form-select-lg fw-bold 
                            <?= $order['status'] === 'PENDING' ? 'text-warning bg-light-warning' : '' ?>
                            <?= $order['status'] === 'PAID' ? 'text-success bg-light-success' : '' ?>
                            <?= $order['status'] === 'CANCELLED' ? 'text-danger bg-light-danger' : '' ?>" 
                            id="status" name="status">
                            <option value="PENDING" <?= $order['status'] === 'PENDING' ? 'selected' : '' ?>>PENDING</option>
                            <option value="PAID" <?= $order['status'] === 'PAID' ? 'selected' : '' ?>>PAID</option>
                            <option value="CANCELLED" <?= $order['status'] === 'CANCELLED' ? 'selected' : '' ?>>CANCELLED</option>
                        </select>
                    </div>

                    <button type="submit" class="btn btn-primary w-100 fw-bold py-2">
                        <i class="fa-solid fa-circle-check me-1"></i> Update Status
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
<?= $this->endSection() ?>
