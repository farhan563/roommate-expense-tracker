from streamlit_authenticator.utilities.hasher import Hasher

# ✅ Step 1: Create Hasher object
hasher = Hasher()

# ✅ Step 2: Hash passwords one by one
plain_passwords = ["123", "456"]

# ✅ Step 3: Store hashed output
hashed_passwords = [hasher.hash(pw) for pw in plain_passwords]

# ✅ Step 4: Print them
for i, hashed in enumerate(hashed_passwords, start=1):
    print(f"Hashed password {i}: {hashed}")
