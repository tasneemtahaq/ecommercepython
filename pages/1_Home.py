import streamlit as st
from src.database import Session, Product
from src.cart_manager import CartManager

def show():
    st.title("🏠 Welcome to Our Store")
    st.markdown("### Featured Products")
    
    # Load featured products
    session = Session()
    featured_products = session.query(Product).filter(Product.category == 'leather').limit(3).all()
    
    # Create columns for product cards
    cols = st.columns(3)
    
    for idx, product in enumerate(featured_products):
        with cols[idx]:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            
            # Product Image
            try:
                st.image(f"assets/images/products/{product.image}",
                        use_column_width=True,
                        caption=product.name)
            except FileNotFoundError:
                st.image("assets/images/placeholder.jpg",
                        use_column_width=True,
                        caption="Image coming soon")
            
            # Product Details
            st.subheader(product.name)
            st.markdown(f"**${product.price}**")
            st.caption(product.description[:50] + "...")
            
            # Add to Cart
            if st.button("🛒 Add to Cart", key=f"home_{product.id}"):
                CartManager().add_item(product.id, 1)
                st.success("Added to cart!")
            
            st.markdown("</div>", unsafe_allow_html=True)

    # Featured Categories Section
    st.markdown("---")
    st.markdown("### Shop by Category")
    
    cat_cols = st.columns(3)
    categories = [
        ("🎒 Backpacks", "backpack"),
        ("🧥 Leather Goods", "leather"),
        ("👜 Artificial Bags", "artificial")
    ]
    
    for idx, (title, category) in enumerate(categories):
        with cat_cols[idx]:
            st.markdown(f"<div class='category-card'>", unsafe_allow_html=True)
            st.markdown(f"#### {title}")
            cat_products = session.query(Product).filter_by(category=category).limit(2).all()
            
            for product in cat_products:
                st.image(f"assets/images/products/{product.image}", 
                        width=150,
                        caption=product.name)
                st.write(f"From ${product.price}")
            
            if st.button(f"Shop {title.split()[-1]} ➡️", key=f"cat_{category}"):
                st.session_state.selected_category = category
                st.switch_page("pages/2_Products.py")
            
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()