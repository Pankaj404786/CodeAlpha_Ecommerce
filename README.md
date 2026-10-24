# Simple E-commerce Store (Django)

## Features
- Product listing and product detail pages
- Session-based shopping cart
- User registration, login and logout
- Checkout and order processing
- SQLite database for products, users, orders and order items
- Django admin for managing products and orders

## Requirements
- Python 3.11+
- Visual Studio Code

## Run on Windows (PowerShell)
1. Extract this ZIP and open the `simple_ecommerce_store` folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
4. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use:
   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe manage.py migrate
   .\.venv\Scripts\python.exe manage.py seed_products
   .\.venv\Scripts\python.exe manage.py runserver
   ```
   Then use `.\.venv\Scripts\python.exe` instead of `python` in the commands below.
5. Install Django:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Create database tables:
   ```powershell
   python manage.py migrate
   ```
7. Add sample products:
   ```powershell
   python manage.py seed_products
   ```
8. (Optional) Create admin account:
   ```powershell
   python manage.py createsuperuser
   ```
9. Start the website:
   ```powershell
   python manage.py runserver
   ```
10. Open http://127.0.0.1:8000/ in your browser.
11. Admin page: http://127.0.0.1:8000/admin/

## Notes
- Orders are stored in SQLite. Checkout is a demo order flow and does not collect payment or connect to a payment gateway.
- This Django development server is for local development, not production deployment.
- Product images use remote Unsplash image URLs for demo purposes; an internet connection is needed to display them.
