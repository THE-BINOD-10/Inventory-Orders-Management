# FZTPL Inventory & Orders Backend

Hi, this is my backend project for managing inventory items and orders for FZTPL. I built it using **FastAPI** and **PostgreSQL**, keeping things clean and easy to maintain. It has full CRUD for items, order management with stock checks, simple API key authentication, and some basic tests.

## What I Built

### Items
- I can **create items** with unique names among active items.  
- I can **list items** with search, price filters, and pagination.  
- I can **get a single item**, which shows `low_stock: true` if the quantity is below 5.  
- I can **update items**, making sure the name stays unique.  
- I can **soft delete items** by setting `is_active = false` instead of removing them.  

### Orders
- I can **create orders**, checking that items exist and stock is available. The stock gets updated in a single transaction, and the total amount is calculated automatically.  
- I can **list orders** with filters like `customer_name`, `status`, `from_date`, `to_date` and pagination.  
- I can **get an order by ID** with full item breakdown.  
- I can **cancel an order** (optional) and restore the stock if needed.  

### Authentication
- All endpoints need an API key in the header:  

X-API-KEY: mysecretkey


### Error Handling
- Returns proper JSON responses for validation errors (400), unauthorized/forbidden (401/403), not found (404), stock issues, and fallback for internal errors.  

### Testing
- I added simple tests to check creating items and orders with stock validation.  

---

## How to Set It Up

### Clone the repo
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd fztpl_inventory_backend


Create and activate a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python -m venv venv
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Set up environment variables
Create a .env file in the project root:

DATABASE_URL=postgresql://postgres:binod10@localhost:5432/fztpl_inventory
API_KEY=mysecretkey

Run database migrations

alembic upgrade head

Or use the SQL scripts in /migrations.

Start the server

uvicorn app.main:app --reload

It will run on http://127.0.0.1:8000.

Running Tests

I can run tests easily with:

pytest

API Summary

Items Endpoints

POST /items → Create item

GET /items → List items with filters/pagination

GET /items/{id} → Get single item

PUT /items/{id} → Update item

DELETE /items/{id} → Soft delete item

Orders Endpoints

POST /orders → Create order

GET /orders → List orders

GET /orders/{id} → Get order by ID

POST /orders/{id}/cancel → Cancel order

Auth: X-API-KEY: mysecretkey on all requests

Postman

I included a Postman collection called postman_fztpl_domain_task_collection.json with all the requests I tested.


Author

Binod Parajuli

Task Completed:Yes
