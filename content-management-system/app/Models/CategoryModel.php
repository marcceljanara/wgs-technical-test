<?php

namespace App\Models;

use CodeIgniter\Model;

class CategoryModel extends Model
{
    protected $table            = 'categories';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = false;
    protected $returnType       = 'array';
    protected $useSoftDeletes   = false;
    protected $protectFields    = true;
    protected $allowedFields    = ['id', 'name', 'slug'];

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
