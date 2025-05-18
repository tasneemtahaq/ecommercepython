import streamlit as st
from src.database import Session, Product
from src.cart_manager import CartManager
from src.utils import load_css

def show():
    load_css()
    st.title("🛍️ Our Products")
    
    # Category filter
    categories = ["leather", "artificial", "backpack"]
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Get products
    session = Session()
    if selected_category == "All":
        products = session.query(Product).all()
    else:
        products = session.query(Product).filter_by(category=selected_category).all()
    
    # Display grid
    cols = st.columns(3)
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            # Clickable product card
            with st.container():
                # Create clickable area using columns
                col_img, _ = st.columns([4, 1])
                with col_img:
                    # Clickable image and title
                    if st.button(
                        key=f"product_{product.id}",
                        label="",
                        help=f"Click to view {product.name}",
                    ):
                        st.session_state.selected_product = product.id
                        st.switch_page("pages/3_Product_Detail.py")
                    
                    st.image(
                        f"assets/images/products/{product.image}",
                        use_column_width=True,
                        caption=product.name
                    )
                    st.subheader(product.name)
                
                # Product details and add to cart
                st.markdown(f"**${product.price:.2f}**")
                st.caption(product.description[:80] + "...")
                
                # Add to cart form
                with st.form(key=f"cart_{product.id}"):
                    quantity = st.number_input(
                        "Qty", 
                        min_value=1, 
                        value=1,
                        key=f"qty_{product.id}"
                    )
                    if st.form_submit_button("Add to Cart 🛒", use_container_width=True):
                        cart = CartManager()
                        if cart.add_item(product.id, quantity):
                            st.success("Added to cart!")
                        else:
                            st.error("Failed to add item")

if __name__ == "__main__":
    show()