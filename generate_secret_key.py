import secrets

# Generate a secure random secret key for JWT
secret_key = secrets.token_hex(32)

print("=" * 60)
print("🔐 SECRET KEY GENERATOR")
print("=" * 60)
print("\nYour secure SECRET_KEY for production:")
print("\n" + secret_key)
print("\n" + "=" * 60)
print("\n📋 Copy this key and use it in:")
print("   1. Render.com environment variables")
print("   2. Your production .env file")
print("\n⚠️  IMPORTANT: Keep this secret! Don't share it publicly.")
print("=" * 60)
