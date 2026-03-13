# pip install fastapi
# pip install uvicorn
# pip install python-dotenv
# pip install sqlalchemy
# pip install mysql-connector-python
# pip install pymysql

# DEBUGGER COMMAND python -m debugpy --listen 5678 -m uvicorn app.main:app
<!-- {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "python":"${workspaceFolder}/secondpy/Scripts/python.exe",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload"
            ],
            "jinja": true
        },
       
    ]
} -->

<!-- 
# result = db.query(Product, Category)\
        .filter(Product.category_id == Category.id)\  # ✅ match without FK
        .all() -->

<!-- # result = (
        db.query(User.name, Product.name, Product.price)
        .join(Order, User.id == Order.user_id)
        .join(Product, Order.product_id == Product.id)
        .all()
    ) -->
    