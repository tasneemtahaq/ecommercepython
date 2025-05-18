import stripe
from config import Config
import streamlit as st

class PaymentProcessor:
    @staticmethod
    def create_payment_intent(amount):
        try:
            # Validate amount
            if not isinstance(amount, (int, float)) or amount <= 0:
                raise ValueError("Invalid payment amount")

            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency="usd",
                payment_method_types=["card"],
                metadata={
                    "user_id": st.session_state.get("user", {}).get("id", "guest"),
                    "cart_total": str(amount)
                }
            )
            
            # Debug logging
            st.write("Payment Intent Created:", intent.id)
            
            return intent
        except Exception as e:
            st.error(f"Payment Error: {str(e)}")
            raise