# src/admin_manager.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from src.database import Session, User, Product, Order, OrderItem
from config import Config

class AdminManager:
    def __init__(self):
        self.session = Session()
        
    # User Management
    def get_all_users(self):
        """Get all registered users"""
        try:
            return self.session.query(User).all()
        except SQLAlchemyError as e:
            print(f"Error fetching users: {str(e)}")
            return []

    def delete_user(self, user_id: int):
        """Delete a user by ID"""
        try:
            user = self.session.query(User).get(user_id)
            if user:
                self.session.delete(user)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting user: {str(e)}")
            return False

    def promote_to_admin(self, user_id: int):
        """Grant admin privileges to a user"""
        try:
            user = self.session.query(User).get(user_id)
            if user and user.username != Config.ADMIN_USERNAME:
                user.is_admin = True
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error promoting user: {str(e)}")
            return False

    # Product Management
    def create_product(self, product_data: dict):
        """Create new product"""
        try:
            new_product = Product(**product_data)
            self.session.add(new_product)
            self.session.commit()
            return new_product
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error creating product: {str(e)}")
            return None

    def update_product(self, product_id: int, update_data: dict):
        """Update existing product"""
        try:
            product = self.session.query(Product).get(product_id)
            if product:
                for key, value in update_data.items():
                    setattr(product, key, value)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating product: {str(e)}")
            return False

    # Order Management
def get_all_orders(self):
    """Get all orders with related information"""
    try:
        return self.session.query(Order)\
            .options(
                joinedload(Order.items).joinedload(OrderItem.product)  # Correct loading path
            )\
            .all()
    except SQLAlchemyError as e:
        print(f"Error fetching orders: {str(e)}")
        return []

    def update_order_status(self, order_id: int, new_status: str):
        """Update order status"""
        try:
            order = self.session.query(Order).get(order_id)
            if order:
                order.status = new_status
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating order status: {str(e)}")
            return False

    # Analytics
    def get_sales_report(self):
        """Generate sales report"""
        try:
            return self.session.query(
                Product.name,
                Product.category,
                Product.price,
                OrderItem.quantity,
                Order.status
            ).join(OrderItem.product).join(OrderItem.order).all()
        except SQLAlchemyError as e:
            print(f"Error generating report: {str(e)}")
            return []