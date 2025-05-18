import os
from datetime import datetime
from src.database import Session, Product

class ProductManager:
    def __init__(self):
        self.session = Session()
        self.image_dir = "assets/images/products"
        os.makedirs(self.image_dir, exist_ok=True)

    def add_product(self, name, price, category, description, image):
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{image.name}"
        filepath = os.path.join(self.image_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(image.getbuffer())
        
        # Create product record
        new_product = Product(
            name=name,
            price=price,
            category=category,
            description=description,
            image=filename
        )
        
        self.session.add(new_product)
        self.session.commit()
        return new_product

    def get_by_category(self, category):
        return self.session.query(Product).filter_by(category=category).all()