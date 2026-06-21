<?php

namespace App\Controllers;

use App\Controllers\BaseController;
use App\Models\ProductModel;
use App\Models\CategoryModel;

class ProductController extends BaseController
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
        // Join with categories to show category name
        $data['products'] = $this->productModel
            ->select('products.*, categories.name as category_name')
            ->join('categories', 'categories.id = products.category_id', 'left')
            ->findAll();
        $data['title'] = 'Manage Products';
        return view('products/index', $data);
    }

    public function create()
    {
        $data['categories'] = $this->categoryModel->findAll();
        $data['title'] = 'Create Product';
        return view('products/create', $data);
    }

    public function store()
    {
        $rules = [
            'category_id' => 'permit_empty',
            'title'       => 'required|min_length[3]|max_length[255]',
            'description' => 'permit_empty',
            'price'       => 'required|numeric|greater_than_equal_to[0]',
            'stock'       => 'required|integer|greater_than_equal_to[0]',
        ];

        if (!$this->validate($rules)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }

        $categoryId = $this->request->getPost('category_id');
        if ($categoryId === '') {
            $categoryId = null;
        }

        $this->productModel->insert([
            'category_id' => $categoryId,
            'title'       => $this->request->getPost('title'),
            'description' => $this->request->getPost('description'),
            'price'       => $this->request->getPost('price'),
            'stock'       => $this->request->getPost('stock'),
        ]);

        return redirect()->to('admin/products')->with('success', 'Product created successfully.');
    }

    public function edit($id)
    {
        $product = $this->productModel->find($id);
        if (!$product) {
            return redirect()->to('admin/products')->with('error', 'Product not found.');
        }

        $data['product'] = $product;
        $data['categories'] = $this->categoryModel->findAll();
        $data['title'] = 'Edit Product';
        return view('products/edit', $data);
    }

    public function update($id)
    {
        $product = $this->productModel->find($id);
        if (!$product) {
            return redirect()->to('admin/products')->with('error', 'Product not found.');
        }

        $rules = [
            'category_id' => 'permit_empty',
            'title'       => 'required|min_length[3]|max_length[255]',
            'description' => 'permit_empty',
            'price'       => 'required|numeric|greater_than_equal_to[0]',
            'stock'       => 'required|integer|greater_than_equal_to[0]',
        ];

        if (!$this->validate($rules)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }

        $categoryId = $this->request->getPost('category_id');
        if ($categoryId === '') {
            $categoryId = null;
        }

        $this->productModel->update($id, [
            'category_id' => $categoryId,
            'title'       => $this->request->getPost('title'),
            'description' => $this->request->getPost('description'),
            'price'       => $this->request->getPost('price'),
            'stock'       => $this->request->getPost('stock'),
        ]);

        return redirect()->to('admin/products')->with('success', 'Product updated successfully.');
    }

    public function delete($id)
    {
        $product = $this->productModel->find($id);
        if (!$product) {
            return redirect()->to('admin/products')->with('error', 'Product not found.');
        }

        $this->productModel->delete($id);
        return redirect()->to('admin/products')->with('success', 'Product deleted successfully.');
    }
}
