import streamlit as st
from src.database import Session, Order, User
from src.product_manager import ProductManager
from src.utils import load_css
from src.admin_manager import AdminManager

def show():
    load_css()
    
    # Authorization check
    user_info = st.session_state.get('user', {})
    if not user_info.get('is_admin', False):
        st.error("⛔ Admin privileges required")
        st.switch_page("pages/1_Home.py")
        return

    st.title("👑 Admin Dashboard")
    admin_mgr = AdminManager()

    tab1, tab2, tab3 = st.tabs(["Manage Products", "View Orders", "User Management"])

    with tab1:
        st.subheader("Product Management")
        with st.form("product_form"):
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0.0)
            category = st.selectbox("Category", ["leather", "artificial", "backpack"])
            description = st.text_area("Description")
            image = st.file_uploader("Product Image", type=["jpg", "png"])
            
            if st.form_submit_button("Add Product"):
                if image:
                    ProductManager().add_product(name, price, category, description, image)
                    st.success("Product added successfully!")

    with tab2:
        st.subheader("Order Management")
        orders = admin_mgr.get_all_orders()
        for order in orders:
            with st.expander(f"Order #{order.id} - {order.status}"):
                st.write(f"Total: ${order.total}")
                st.write("Products:")
                for item in order.items:
                    st.write(f"- {item.product.name} x{item.quantity}")

    with tab3:
        st.subheader("User Management")
        users = admin_mgr.get_all_users()
        st.dataframe(
            [{"ID": u.id, "Username": u.username, "Email": u.email, "Admin": u.is_admin} 
             for u in users],
            column_config={
                "ID": "ID",
                "Username": "Username",
                "Email": "Email",
                "Admin": st.column_config.CheckboxColumn("Admin Status")
            }
        )
        
        selected_user = st.selectbox("Select User", [u.id for u in users], format_func=lambda x: next(u.username for u in users if u.id == x))
        if st.button("Delete User"):
            if admin_mgr.delete_user(selected_user):
                st.success("User deleted successfully")
                st.rerun()

if __name__ == "__main__":
    show()