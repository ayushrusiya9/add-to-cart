# cart_demo (Django Beginner Friendly Cart)

This project demonstrates a **session-based Add to Cart** system without JS or helpers.

## Features
- Simple Product model (name, price)
- Session stores cart items (`{product_id: quantity}`)
- Navbar button shows live cart count (initial 0)
- Add products and see count increase
- View Cart page with items and total

## Setup
1. Create virtual env and install Django:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install django
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create products in admin or shell.

4. Run server:
   ```bash
   python manage.py runserver
   ```

5. Open `http://127.0.0.1:8000/`

