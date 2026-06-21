<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? 'Admin Panel' ?> - CMS</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <!-- Alternatively use standard bootstrap cdn if path is incorrect -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <!-- FontAwesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .sidebar {
            min-height: 100vh;
            background-color: #343a40;
            color: #fff;
        }
        .sidebar a {
            color: #c2c7d0;
            text-decoration: none;
            display: block;
            padding: 10px 15px;
            border-radius: 4px;
            margin-bottom: 5px;
        }
        .sidebar a:hover, .sidebar a.active {
            color: #fff;
            background-color: rgba(255,255,255,0.1);
        }
        .main-content {
            padding: 20px;
        }
        .navbar-brand {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 sidebar py-3">
                <h4 class="text-center mb-4 text-white"><i class="fa-solid fa-gauge-high me-2"></i>CMS Admin</h4>
                <hr class="bg-secondary">
                <nav class="nav flex-column">
                    <a href="<?= base_url('admin/products') ?>" class="<?= (url_is('admin/products*') || url_is('admin')) ? 'active' : '' ?>">
                        <i class="fa-solid fa-box me-2"></i> Products
                    </a>
                    <a href="<?= base_url('admin/categories') ?>" class="<?= url_is('admin/categories*') ? 'active' : '' ?>">
                        <i class="fa-solid fa-list me-2"></i> Categories
                    </a>
                    <a href="<?= base_url('admin/orders') ?>" class="<?= url_is('admin/orders*') ? 'active' : '' ?>">
                        <i class="fa-solid fa-cart-shopping me-2"></i> Orders
                    </a>
                    <hr class="bg-secondary">
                    <a href="<?= base_url('shop') ?>" target="_blank">
                        <i class="fa-solid fa-globe me-2"></i> View Shop
                    </a>
                </nav>
            </div>

            <!-- Main Content Area -->
            <div class="col-md-9 col-lg-10 main-content">
                <!-- Top Header -->
                <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                    <h1 class="h2"><?= $title ?? 'Dashboard' ?></h1>
                    <div>
                        <span class="badge bg-secondary p-2"><i class="fa-solid fa-user me-1"></i> Admin User</span>
                    </div>
                </div>

                <!-- Alert Messages -->
                <?php if (session()->getFlashdata('success')) : ?>
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        <i class="fa-solid fa-circle-check me-2"></i><?= session()->getFlashdata('success') ?>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                <?php endif; ?>

                <?php if (session()->getFlashdata('error')) : ?>
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <i class="fa-solid fa-circle-xmark me-2"></i><?= session()->getFlashdata('error') ?>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                <?php endif; ?>

                <!-- Page Content -->
                <?= $this->renderSection('content') ?>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 Bundle JS with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
