from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
app=FastAPI() 

# CORS middleware configuration to allow requests from frontend to backend
# This is necessary when the frontend and backend are hosted on different origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

# Create the database tables
database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greeting():
    return "Hello, welcome to the program!"

products=[
     
    Product(id=1, name="Laptop", description="A high-performance laptop", price=499.99, quantity=10),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=199.99, quantity=25),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones", price=99.99, quantity=50),
    Product(id=4, name="Monitor", description="4K UHD Monitor", price=299.99, quantity=15),
    Product(id=5, name="Keyboard", description="Mechanical keyboard", price=49.99, quantity=30)

]

# Dependency to get DB session for all requests
# Function to get a database session
# yield keyword is used to provide a session and ensure it's closed after use
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


# Function to populate the database with initial products
# This function checks if the products table is empty and populates it if necessary
# db.add(database_models.Product(**product.model_dump())) keyword argument unpacking to convert Pydantic model to SQLAlchemy model

def init_db():
    db=session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump())) 
        db.commit()
init_db()


# Dependency injection to get DB session
# db: Session=Depends(get_db) injects a database session into the route handlers
@app.get('/products')
def get_all_products(db: Session=Depends(get_db)):
    database_db=db.query(database_models.Product).all()
    
    return database_db

# db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first() this line queries the database for a product with the specified id


@app.get("/product/{id}")
def get_product_by_id(id: int,db:Session=Depends(get_db)):
    # for product in products:
        db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
        if db_product:
            return db_product
        return {"error": "Product not found"}

#db.commit() is used to save changes to the database after adding a new product
# Always use it after making changes to the database session 


@app.post("/products")
def add_product(product: Product, db:Session =Depends(get_db)):
    db_product=database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    return product  

@app.put("/products/{id}")
def update_product(id: int, product: Product,db:Session=Depends(get_db)):
    # for i in range(len(products)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if(db_product):
        # products[i]=product
        db_product.name=product.name
        db_product.description=product.description      
        db_product.price=product.price
        db_product.quantity=product.quantity    
        db.commit()
        return "Product updated successfully"
    else:
        return {"error": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id: int, db:Session=Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id==id:
    #         del products[i] 
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit() 
        return "Product deleted"
    else:
        return {"error": "Product not found"}
