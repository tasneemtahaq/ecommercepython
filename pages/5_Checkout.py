import streamlit as st
import stripe
from src.cart_manager import CartManager
from src.payment_gateway import PaymentProcessor
from src.utils import load_css
from components import stripe_components
from config import Config

def show():
    load_css()
    st.title("💳 Checkout")
    
    cart_manager = CartManager()
    
    # Validate cart first
    if not cart_manager.cart:
        st.error("Your cart is empty!")
        st.stop()

    # Shipping Details
    with st.form("shipping_details"):
        st.subheader("Shipping Information")
        name = st.text_input("Full Name", key="ship_name")
        address = st.text_area("Shipping Address", key="ship_addr")
        email = st.text_input("Email", key="ship_email")
        
        if st.form_submit_button("Save Details"):
            st.session_state.shipping = {
                "name": name,
                "address": address,
                "email": email
            }
            st.success("Shipping details saved!")

    if 'shipping' in st.session_state:
        try:
            total = cart_manager.get_cart_total()
            intent = PaymentProcessor.create_payment_intent(total)
            
            # Get Stripe form template
            payment_form = stripe_components.stripe_form.format(
                public_key=Config.STRIPE_PUBLIC_KEY,
                client_secret=intent.client_secret
            )
            
            # Render using Streamlit's component system
            st.components.v1.html(payment_form, height=400)
            
        except Exception as e:
            st.error(f"Payment Error: {str(e)}")


if __name__ == "__main__":
    show()