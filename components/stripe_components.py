stripe_form = """
<script src="https://js.stripe.com/v3/"></script>
<div id="payment-element"></div>
<button id="submit">Pay Now</button>
<div id="error-message"></div>

<script>
const stripe = Stripe('{public_key}');
const elements = stripe.elements({{
    clientSecret: '{client_secret}',
    appearance: {{
        theme: 'stripe',
        variables: {{
            colorPrimary: '#4a90e2',
            colorBackground: '#ffffff'
        }}
    }}
}});

const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

document.getElementById('submit').addEventListener('click', async (e) => {{
    e.preventDefault();
    const {{ error }} = await stripe.confirmPayment({{
        elements,
        confirmParams: {{
            return_url: window.location.href
        }}
    }});

    if (error) {{
        document.getElementById('error-message').textContent = error.message;
    }}
}});
</script>
"""