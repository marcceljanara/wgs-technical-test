<?php

namespace App\Models;

use CodeIgniter\Model;

class OrderItemModel extends Model
{
    protected $table            = 'order_items';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = false;
    protected $returnType       = 'array';
    protected $useSoftDeletes   = false;
    protected $protectFields    = true;
    protected $allowedFields    = ['id', 'order_id', 'product_id', 'quantity', 'price_at_purchase'];

    // Callbacks
    protected $allowCallbacks = true;
    protected $beforeInsert   = ['generateUuid'];

    protected function generateUuid(array $data)
    {
        if (empty($data['data']['id'])) {
            helper('uuid');
            $data['data']['id'] = uuid_v4();
        }
        return $data;
    }
}
