from src.database import Session, Product, Order, OrderItem
import streamlit as st

class CartManager:
    def __init__(self):
        self.session = Session()
        if 'cart' not in st.session_state:
            st.session_state.cart = []

    @property
    def cart(self):
        return st.session_state.cart

    def add_item(self, product_id, quantity):
        try:
            product = self.session.query(Product).get(product_id)
            if product:
                # Check if item already exists in cart
                for item in st.session_state.cart:
                    if item['product_id'] == product_id:
                        item['quantity'] += quantity
                        return True
                
                # Add new item
                st.session_state.cart.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "quantity": quantity,
                    "image": product.image
                })
                return True
            return False
        except Exception as e:
            st.error(f"Error adding to cart: {str(e)}")
            return False

    def get_cart_total(self):
        return sum(item['price'] * item['quantity'] for item in st.session_state.cart)

    def clear_cart(self):
        st.session_state.cart = []