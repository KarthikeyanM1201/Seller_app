# 🐔 FarmMarket - Poultry Marketplace

A full-stack Poultry Marketplace built using **Django REST Framework**, **MySQL**, and **Flutter**.

The platform connects **Customers**, **Sellers**, **Delivery Partners**, and **Administrators** in a single marketplace.

---

## 🚀 Features

### 👤 Authentication

- JWT Authentication
- User Registration
- OTP Verification
- Login
- Profile API
- Role-based Authentication

---

### 👥 User Roles

- Customer
- Seller
- Delivery Partner
- Admin

---

### 🛍 Product Management

- Product Categories
- Product CRUD
- Product Images
- Stock Management
- Product Search
- Product Filtering
- Product Ordering

---

### 🛒 Shopping Cart

- Add to Cart
- Update Quantity
- Remove Item
- Clear Cart

---

### 📦 Order Management

- Checkout
- Order History
- Order Details
- Cancel Order

---

### ❤️ Wishlist

- Add to Wishlist
- View Wishlist
- Remove from Wishlist

---

## 🛠 Tech Stack

### Backend

- Python 3.14
- Django 6
- Django REST Framework
- MySQL
- JWT Authentication
- Pillow
- django-filter

### Frontend (Planned)

- Flutter

### Database

- MySQL

---

## 📁 Project Structure

```text
Seller_app/
│
├── backend/
│   ├── accounts/
│   ├── products/
│   ├── orders/
│   ├── wishlist/
│   ├── payments/
│   ├── delivery/
│   ├── notifications/
│   ├── config/
│   └── manage.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/KarthikeyanM1201/Seller_app.git
```

### Move into Project

```bash
cd Seller_app/backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r ../requirements.txt
```

### Configure MySQL

Create a MySQL database:

```text
farmmarket
```

Update the database settings in:

```
backend/config/settings.py
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

---

## 📌 Completed Modules

- Authentication
- User Roles
- Product Module
- Categories
- Shopping Cart
- Orders
- Wishlist

---

## 🚧 Upcoming Modules

- Razorpay Payments
- Delivery Partner Management
- Live Order Tracking
- Notifications
- Flutter Mobile Application
- Admin Dashboard
- Analytics

---

## 👨‍💻 Developer

**Karthikeyan M**

GitHub:
https://github.com/KarthikeyanM1201

---

## 📄 License

This project is developed for learning and portfolio purposes.