<?php

namespace App\Controllers;

use App\Controllers\BaseController;
use App\Models\ProductModel;
use App\Models\CategoryModel;

class ShopController extends BaseController
{
    protected $productModel;
    protected $categoryModel;

    public function __construct()
    {
        $this->productModel = new ProductModel();
        $this->categoryModel = new CategoryModel();
    }

    public function index()
    {
        $categoryId = $this->request->getGet('category');
        
        $query = $this->productModel
            ->select('products.*, categories.name as category_name')
            ->join('categories', 'categories.id = products.category_id', 'left')
            ->where('products.stock >', 0); // only show in-stock products for shopping simulation

        if ($categoryId) {
            $query = $query->where('products.category_id', $categoryId);
        }

        $data['products'] = $query->findAll();
        $data['categories'] = $this->categoryModel->findAll();
        $data['selectedCategory'] = $categoryId;
        $data['title'] = 'Product Shop Catalog';
        
        return view('shop/index', $data);
    }

    public function detail($id)
    {
        $product = $this->productModel
            ->select('products.*, categories.name as category_name')
            ->join('categories', 'categories.id = products.category_id', 'left')
            ->find($id);

        if (!$product) {
            return redirect()->to('shop')->with('error', 'Product not found.');
        }

        $data['product'] = $product;
        $data['title'] = $product['title'] . ' - Buy Now';
        return view('shop/detail', $data);
    }
}
