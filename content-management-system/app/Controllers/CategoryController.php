<?php

namespace App\Controllers;

use App\Controllers\BaseController;
use App\Models\CategoryModel;

class CategoryController extends BaseController
{
    protected $categoryModel;

    public function __construct()
    {
        $this->categoryModel = new CategoryModel();
    }

    public function index()
    {
        $data['categories'] = $this->categoryModel->findAll();
        $data['title'] = 'Manage Categories';
        return view('categories/index', $data);
    }

    public function create()
    {
        $data['title'] = 'Create Category';
        return view('categories/create', $data);
    }

    public function store()
    {
        $rules = [
            'name' => 'required|min_length[3]|max_length[100]'
        ];

        if (!$this->validate($rules)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }

        $name = $this->request->getPost('name');
        helper('text'); // load text helper for url_title
        $slug = url_title($name, '-', true);

        // Check if slug is unique
        $existing = $this->categoryModel->where('slug', $slug)->first();
        if ($existing) {
            $slug = $slug . '-' . time();
        }

        $this->categoryModel->insert([
            'name' => $name,
            'slug' => $slug
        ]);

        return redirect()->to('admin/categories')->with('success', 'Category created successfully.');
    }

    public function edit($id)
    {
        $category = $this->categoryModel->find($id);
        if (!$category) {
            return redirect()->to('admin/categories')->with('error', 'Category not found.');
        }

        $data['category'] = $category;
        $data['title'] = 'Edit Category';
        return view('categories/edit', $data);
    }

    public function update($id)
    {
        $category = $this->categoryModel->find($id);
        if (!$category) {
            return redirect()->to('admin/categories')->with('error', 'Category not found.');
        }

        $rules = [
            'name' => 'required|min_length[3]|max_length[100]'
        ];

        if (!$this->validate($rules)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }

        $name = $this->request->getPost('name');
        helper('text');
        $slug = url_title($name, '-', true);

        // Check if slug is unique (excluding current)
        $existing = $this->categoryModel->where('slug', $slug)->where('id !=', $id)->first();
        if ($existing) {
            $slug = $slug . '-' . time();
        }

        $this->categoryModel->update($id, [
            'name' => $name,
            'slug' => $slug
        ]);

        return redirect()->to('admin/categories')->with('success', 'Category updated successfully.');
    }

    public function delete($id)
    {
        $category = $this->categoryModel->find($id);
        if (!$category) {
            return redirect()->to('admin/categories')->with('error', 'Category not found.');
        }

        $this->categoryModel->delete($id);
        return redirect()->to('admin/categories')->with('success', 'Category deleted successfully.');
    }
}
