<?php

namespace App\Database\Migrations;

use CodeIgniter\Database\Migration;

class CreateOrderItemsTable extends Migration
{
    public function up()
    {
        $this->forge->addField([
            'id' => [
                'type'       => 'VARCHAR',
                'constraint' => 36,
            ],
            'order_id' => [
                'type'       => 'VARCHAR',
                'constraint' => 36,
            ],
            'product_id' => [
                'type'       => 'VARCHAR',
                'constraint' => 36,
                'null'       => true,
            ],
            'quantity' => [
                'type' => 'INT',
            ],
            'price_at_purchase' => [
                'type'       => 'DECIMAL',
                'constraint' => '12,2',
            ],
        ]);
        $this->forge->addKey('id', true);
        $this->forge->addForeignKey('order_id', 'orders', 'id', 'CASCADE', 'CASCADE');
        $this->forge->addForeignKey('product_id', 'products', 'id', 'SET NULL', 'CASCADE');
        $this->forge->createTable('order_items');
    }

    public function down()
    {
        $this->forge->dropTable('order_items');
    }
}
