<?php

namespace App\Controllers;

use App\Controllers\BaseController;
use App\Models\OrderModel;
use App\Models\OrderItemModel;

class OrderController extends BaseController
{
    protected $orderModel;
    protected $orderItemModel;

    public function __construct()
    {
        $this->orderModel = new OrderModel();
        $this->orderItemModel = new OrderItemModel();
    }

    public function index()
    {
        $data['orders'] = $this->orderModel->orderBy('created_at', 'DESC')->findAll();
        $data['title'] = 'Manage Orders';
        return view('orders/index', $data);
    }

    public function view($id)
    {
        $order = $this->orderModel->find($id);
        if (!$order) {
            return redirect()->to('admin/orders')->with('error', 'Order not found.');
        }

        // Get items for this order joined with product title
        $items = $this->orderItemModel
            ->select('order_items.*, products.title as product_title')
            ->join('products', 'products.id = order_items.product_id', 'left')
            ->where('order_items.order_id', $id)
            ->findAll();

        $data['order'] = $order;
        $data['items'] = $items;
        $data['title'] = 'Order Details - #' . substr($order['id'], 0, 8);
        return view('orders/view', $data);
    }

    public function updateStatus($id)
    {
        $order = $this->orderModel->find($id);
        if (!$order) {
            return redirect()->to('admin/orders')->with('error', 'Order not found.');
        }

        $status = $this->request->getPost('status');
        $validStatuses = ['PENDING', 'PAID', 'CANCELLED'];

        if (!in_array($status, $validStatuses)) {
            return redirect()->back()->with('error', 'Invalid status selected.');
        }

        $this->orderModel->update($id, ['status' => $status]);

        return redirect()->to('admin/orders/view/' . $id)->with('success', 'Order status updated successfully.');
    }
}
