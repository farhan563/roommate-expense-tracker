import streamlit as st

st.set_page_config(page_title="RoomMate Split", page_icon="🧾")

st.title("🧾 RoomMate Bill Split & Expense Tracker")
st.write("Track and split expenses with your roommates easily.")

# Enter roommate names
roommates_input = st.text_input("Enter roommate names (comma separated)", "Farhan, Ali, Rehan")
roommates = [name.strip() for name in roommates_input.split(",") if name.strip()]

# Add expense
st.subheader("➕ Add Expense")
payer = st.selectbox("Who paid?", roommates)
description = st.text_input("What for?")
amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
split_between = st.multiselect("Split between", roommates, default=roommates)

if st.button("Add Expense"):
    st.success(f"✅ ₹{amount:.2f} for '{description}' added. Split among {', '.join(split_between)}.")

    # In the next steps, we’ll sto
