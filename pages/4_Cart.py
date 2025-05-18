import streamlit as st
from src.cart_manager import CartManager
from src.utils import load_css

def show():
    load_css()
    st.title("🛒 Shopping Cart")
    
    cart_manager = CartManager()
    
    if not cart_manager.cart:  # Now using the property
        st.info("Your cart is empty")
        return
    
    st.markdown("<div class='checkout-form'>", unsafe_allow_html=True)
    
    total = 0
    for item in cart_manager.cart:
        st.markdown("<div class='cart-item'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3,1])
        with col1:
            st.subheader(item['name'])
            st.write(f"Quantity: {item['quantity']}")
        with col2:
            item_total = item['price'] * item['quantity']
            st.markdown(f"**${item_total:.2f}**")
            total += item_total
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(f"### Total: ${total:.2f}")
    
    if st.button("Proceed to Checkout ➡️", use_container_width=True):
        st.switch_page("pages/5_Checkout.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()