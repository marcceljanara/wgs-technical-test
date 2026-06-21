<?php

namespace App\Models;

use CodeIgniter\Model;

class OrderModel extends Model
{
    protected $table            = 'orders';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = false;
    protected $returnType       = 'array';
    protected $useSoftDeletes   = false;
    protected $protectFields    = true;
    protected $allowedFields    = ['id', 'customer_name', 'customer_email', 'total_amount', 'status', 'created_at'];

    // Callbacks
    protected $allowCallbacks = true;
    protected $beforeInsert   = ['prepareData'];

    protected function prepareData(array $data)
    {
        if (empty($data['data']['id'])) {
            helper('uuid');
            $data['data']['id'] = uuid_v4();
        }
        $data['data']['created_at'] = date('Y-m-d H:i:s');
        return $data;
    }
}
