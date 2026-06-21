<?php

use CodeIgniter\Router\RouteCollection;

/** @var RouteCollection $routes */
$routes->get('/', 'ShopController::index');
$routes->get('shop', 'ShopController::index');
$routes->get('shop/product/(:any)', 'ShopController::detail/$1');
$routes->post('checkout', 'CheckoutController::process');

// Admin Routes Group
$routes->group('admin', function ($routes) {
    $routes->get('/', 'ProductController::index');

    // Categories CRUD
    $routes->get('categories', 'CategoryController::index');
    $routes->get('categories/create', 'CategoryController::create');
    $routes->post('categories/store', 'CategoryController::store');
    $routes->get('categories/edit/(:any)', 'CategoryController::edit/$1');
    $routes->post('categories/update/(:any)', 'CategoryController::update/$1');
    $routes->get('categories/delete/(:any)', 'CategoryController::delete/$1');

    // Products CRUD
    $routes->get('products', 'ProductController::index');
    $routes->get('products/create', 'ProductController::create');
    $routes->post('products/store', 'ProductController::store');
    $routes->get('products/edit/(:any)', 'ProductController::edit/$1');
    $routes->post('products/update/(:any)', 'ProductController::update/$1');
    $routes->get('products/delete/(:any)', 'ProductController::delete/$1');

    // Orders Management
    $routes->get('orders', 'OrderController::index');
    $routes->get('orders/view/(:any)', 'OrderController::view/$1');
    $routes->post('orders/update-status/(:any)', 'OrderController::updateStatus/$1');
});

