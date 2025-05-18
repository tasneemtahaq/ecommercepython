from config import Config

print("Stripe Keys Verification:")
print("Public Key:", "✅ Found" if Config.STRIPE_PUBLIC_KEY else "❌ Missing")
print("Secret Key:", "✅ Found" if Config.STRIPE_SECRET_KEY else "❌ Missing")
print("\nKey Prefixes:")
print(f"Public: {Config.STRIPE_PUBLIC_KEY[:12]}...")
print(f"Secret: {Config.STRIPE_SECRET_KEY[:12]}...")