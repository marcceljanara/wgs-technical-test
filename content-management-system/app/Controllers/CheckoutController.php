<?php

namespace App\Controllers;

use App\Controllers\BaseController;
use App\Models\ProductModel;
use App\Models\OrderModel;
use App\Models\OrderItemModel;
use CodeIgniter\Database\Exceptions\DatabaseException;

class CheckoutController extends BaseController
{
    protected $productModel;
    protected $orderModel;
    protected $orderItemModel;

    public function __construct()
    {
        $this->productModel = new ProductModel();
        $this->orderModel = new OrderModel();
        $this->orderItemModel = new OrderItemModel();
    }

    public function process()
    {
        $rules = [
            'customer_name'  => 'required|min_length[3]|max_length[100]',
            'customer_email' => 'required|valid_email|max_length[100]',
            'product_id'     => 'required',
            'quantity'       => 'required|integer|greater_than[0]'
        ];

        if (!$this->validate($rules)) {
            return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
        }

        $productId = $this->request->getPost('product_id');
        $quantity = (int) $this->request->getPost('quantity');

        // Check if product exists and has enough stock
        $product = $this->productModel->find($productId);
        if (!$product) {
            return redirect()->back()->withInput()->with('error', 'Product not found.');
        }

        if ($product['stock'] < $quantity) {
            return redirect()->back()->withInput()->with('error', 'Sorry, not enough stock available. Remaining stock: ' . $product['stock']);
        }

        $totalAmount = $product['price'] * $quantity;
        $db = \Config\Database::connect();

        try {
            $db->transException(true)->transStart();

            // Insert into orders
            $orderData = [
                'customer_name'  => $this->request->getPost('customer_name'),
                'customer_email' => $this->request->getPost('customer_email'),
                'total_amount'   => $totalAmount,
                'status'         => 'PENDING'
            ];
            $this->orderModel->insert($orderData);
            
            // Get the generated order ID (CodeIgniter model insert returns false on failure or generated insert ID, but since UUID is generated in model callback, we can get it from the insert operation or get the insert ID. In CodeIgniter 4, we can retrieve the last inserted ID. Let's see: $this->orderModel->getInsertID() or we can pass custom ID from controller or fetch from DB. Actually, to be extremely reliable, we can generate the UUID here in controller or grab it).
            // Wait! To ensure we have the correct order ID, let's generate it here in the Controller and pass it, so we don't have to rely on getInsertID() which might fail or be empty for UUID columns.
            // Yes! Generating it in controller and passing it is 100% reliable!
            helper('uuid');
            $orderId = uuid_v4();
            $orderData['id'] = $orderId;
            
            // Reinsert with explicit ID (this skips uuid callback generation if already present in $data)
            $this->orderModel->insert($orderData);

            // Insert into order_items
            $orderItemData = [
                'order_id'          => $orderId,
                'product_id'        => $productId,
                'quantity'          => $quantity,
                'price_at_purchase' => $product['price']
            ];
            $this->orderItemModel->insert($orderItemData);

            // Decrement product stock
            $newStock = $product['stock'] - $quantity;
            $this->productModel->update($productId, ['stock' => $newStock]);

            $db->transComplete();

            return redirect()->to('shop')->with('success', 'Thank you! Your purchase of ' . $quantity . 'x ' . $product['title'] . ' has been recorded (Status: PENDING). Order ID: ' . substr($orderId, 0, 8));

        } catch (\Exception $e) {
            return redirect()->back()->withInput()->with('error', 'An error occurred during transaction: ' . $e->getMessage());
        }
    }
}
