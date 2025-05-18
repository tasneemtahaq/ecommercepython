import streamlit as st
from src.database import Session, Order, User
from src.product_manager import ProductManager
from src.utils import load_css
from src.admin_manager import AdminManager

def show():
    load_css()
    
    # Authorization check with proper session management
    if 'user' not in st.session_state or not st.session_state.user.get('is_admin', False):
        st.error("⛔ Admin privileges required")
        st.switch_page("pages/1_Home.py")
        return

    st.title("👑 Admin Dashboard")
    admin_mgr = AdminManager()

    tab1, tab2, tab3 = st.tabs(["Manage Products", "View Orders", "User Management"])

    with tab1:
        st.subheader("Product Management")
        with st.form("product_form", clear_on_submit=True):
            name = st.text_input("Product Name", key="prod_name")
            price = st.number_input("Price", min_value=0.0, step=0.01, key="prod_price")
            category = st.selectbox("Category", ["leather", "artificial", "backpack"], key="prod_category")
            description = st.text_area("Description", key="prod_desc")
            image = st.file_uploader("Product Image", type=["jpg", "png"], key="prod_image")
            
            if st.form_submit_button("Add Product"):
                if all([name, price, category, description, image]):
                    try:
                        ProductManager().add_product(name, price, category, description, image)
                        st.success("Product added successfully!")
                    except Exception as e:
                        st.error(f"Error adding product: {str(e)}")
                else:
                    st.warning("Please fill all required fields")

    with tab2:
        st.subheader("Order Management")
        try:
            orders = admin_mgr.get_all_orders()
            if not orders:
                st.info("No orders found.")
            else:
                for order in orders:
                    with st.expander(f"Order #{order.id} - {order.status}"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.metric("Total", f"${order.total:.2f}")
                            st.write(f"**Status:** {order.status}")
                            st.write(f"**User:** {order.user.email}")
                        
                        with col2:
                            st.write("**Items:**")
                            for item in order.items:
                                cols = st.columns([2, 1, 1])
                                cols[0].write(f"**{item.product.name}**")
                                cols[1].write(f"Qty: {item.quantity}")
                                cols[2].write(f"${item.product.price:.2f} each")
        except Exception as e:
            st.error(f"Error loading orders: {str(e)}")

    with tab3:
        st.subheader("User Management")
        try:
            users = admin_mgr.get_all_users()
            if not users:
                st.info("No users found")
                return
                
            df_users = st.dataframe(
                [{"ID": u.id, "Username": u.username, "Email": u.email, "Admin": u.is_admin} 
                 for u in users],
                column_config={
                    "ID": st.column_config.NumberColumn("User ID"),
                    "Username": "Username",
                    "Email": st.column_config.TextColumn("Email", width="large"),
                    "Admin": st.column_config.CheckboxColumn("Admin Status", disabled=True)
                },
                use_container_width=True
            )
            
            selected_user = st.selectbox(
                "Select User", 
                options=[u.id for u in users],
                format_func=lambda x: next(u.username for u in users if u.id == x),
                key="user_select"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete User", type="primary"):
                    if admin_mgr.delete_user(selected_user):
                        st.success("User deleted successfully")
                        st.rerun()
            with col2:
                if st.button("Grant Admin Privileges"):
                    if admin_mgr.promote_to_admin(selected_user):
                        st.success("Admin privileges granted")
                        st.rerun()
        except Exception as e:
            st.error(f"Error managing users: {str(e)}")

if __name__ == "__main__":
    show()