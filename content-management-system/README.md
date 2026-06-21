# Simple CMS Purchase Simulation

A basic Content Management System (CMS) built with PHP CodeIgniter 4 that simulates a product purchasing process. This project implements fundamental CRUD operations and a transactional workflow without authentication or authorization.

## Features
- **Admin Panel (CRUD):**
  - Manage Categories (Create, Read, Update, Delete)
  - Manage Products (Create, Read, Update, Delete) with stock tracking and UUIDv4 identifiers.
  - View Orders and Order Items.
- **Shop / Frontend:**
  - Browse available products.
  - Add products to cart and checkout (Simulated Purchase).
  - Automatically deducts stock upon successful purchase.
- **Database Architecture:**
  - Designed using CodeIgniter 4 Migrations.
  - Includes a provided `database.sql` dump for easy import.
  - Employs UUIDv4 as primary keys for security and uniqueness (generated automatically via Model callbacks).

## Technical Stack
- **Framework:** PHP CodeIgniter 4 (MVC Architecture)
- **Database:** MySQL / MariaDB
- **UI:** Bootstrap 5 (Responsive Layouts)
- **Requirements:** PHP 8.2 or higher

## PHP Extension Requirements
Ensure the following extensions are enabled in your `php.ini`:
- `openssl`
- `zip`
- `intl`
- `mbstring`
- `fileinfo`
- `mysqli`
- `pdo_mysql`

## Installation and Setup

### 1. Clone or Extract the Project
Make sure you are in the project root directory: `content-management-system`.

### 2. Install Dependencies
This project uses Composer to manage dependencies. You can run `composer install` using the included `composer.phar` or your globally installed composer:
```bash
php composer.phar install
# OR
composer install
```

### 3. Database Setup
You have two options to set up the database:

**Option A: Using the SQL Dump (Recommended for quick start)**
1. Create a new MySQL database named `ci4_cms`.
2. Import the provided `database.sql` file located in the project root into this database.

**Option B: Using Migrations**
1. Create a new MySQL database named `ci4_cms`.
2. Open the `.env` file in the project root.
3. Ensure the database connection settings are correct:
   ```env
   database.default.hostname = localhost
   database.default.database = ci4_cms
   database.default.username = root
   database.default.password = 
   database.default.DBDriver = MySQLi
   ```
4. Run the database migrations using the CodeIgniter Spark CLI:
   ```bash
   php spark migrate
   ```

### 4. Configuration
1. Rename `env` to `.env` (if not already done).
2. Set the environment to development to display errors during testing:
   ```env
   CI_ENVIRONMENT = development
   ```
3. Set the base URL:
   ```env
   app.baseURL = 'http://localhost:8080/'
   ```

## Running the Application

Due to some CLI environments experiencing issues with `php spark serve` (specifically related to the `mbstring` extension detection), it is highly recommended to run the application using PHP's built-in development server with the `public` directory as the document root:

```bash
php -S localhost:8080 -t public
```

If your `php.ini` extensions are not loaded globally, you can explicitly load them:
```bash
php -d extension=openssl -d extension=zip -d extension=intl -d extension=mbstring -d extension=fileinfo -d extension=mysqli -d extension=pdo_mysql -d extension_dir="<PATH_TO_YOUR_PHP_EXT_DIR>" -S localhost:8080 -t public
```

*(Note: Replace `<PATH_TO_YOUR_PHP_EXT_DIR>` with the absolute path to your PHP extensions directory, e.g., `C:\php\ext`)*

Alternatively, you can try using the Spark server:
```bash
php spark serve
```

## Usage and Routes

Once the server is running, you can access the application in your browser:

### Shop Area (Purchase Simulation)
- **Catalog:** `http://localhost:8080/`
- **Checkout Process:** Select a product, enter quantity, and proceed to checkout. The system will automatically update the product stock and generate an order record.

### Admin Area (CRUD Management)
- **Categories:** `http://localhost:8080/admin/categories`
- **Products:** `http://localhost:8080/admin/products`
- **Orders:** `http://localhost:8080/admin/orders`

## Project Structure Overview
- `app/Controllers/`: Contains the logic for `Admin` operations and `Shop` checkout processes.
- `app/Models/`: Defines the database interaction logic, including custom `beforeInsert` callbacks for automatic UUIDv4 generation.
- `app/Views/`: Contains the Bootstrap 5 templates structured into `admin`, `shop`, and `layouts` directories.
- `app/Database/Migrations/`: Migration scripts for creating `categories`, `products`, `orders`, and `order_items` tables.
