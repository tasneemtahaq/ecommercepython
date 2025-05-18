import streamlit as st
from src.database import Session, Product
from src.cart_manager import CartManager
from src.utils import load_css

def show():
    load_css()
    
    if 'selected_product' not in st.session_state:
        st.error("No product selected")
        st.switch_page("pages/2_Products.py")
        return

    session = Session()
    product = session.query(Product).get(st.session_state.selected_product)
    
    st.title(product.name)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.image(f"assets/images/products/{product.image}", 
                use_column_width=True,
                caption=product.name)
    
    with col2:
        st.markdown(f"**Price:** ${product.price:.2f}")
        st.markdown(f"**Category:** {product.category.capitalize()}")
        st.markdown("---")
        st.markdown("**Description:**")
        st.write(product.description)
        
        quantity = st.number_input("Quantity", 
                                 min_value=1, 
                                 value=1,
                                 key=f"qty_{product.id}")
        
        if st.button("Add to Cart 🛒", use_container_width=True):
            cart = CartManager()
            if cart.add_item(product.id, quantity):
                st.success(f"Added {quantity} {product.name} to cart!")
            else:
                st.error("Failed to add item to cart")
        
        if st.button("← Back to Products", use_container_width=True):
            del st.session_state.selected_product
            st.switch_page("pages/2_Products.py")

if __name__ == "__main__":
    show()