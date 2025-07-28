import streamlit as st

st.set_page_config(page_title="RoomMate Split", page_icon="🧾")

st.title("🧾 RoomMate Bill Split & Expense Tracker")
st.write("Track and split expenses with your roommates easily.")

# --- Roommate input ---
roommates_input = st.text_input("Enter roommate names (comma separated)", "Farhan, Ali, Rehan")
roommates = [name.strip() for name in roommates_input.split(",") if name.strip()]

# --- Session state to store expenses ---
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# --- Add expense ---
st.subheader("➕ Add Expense")
payer = st.selectbox("Who paid?", roommates)
description = st.text_input("What for?")
amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
split_between = st.multiselect("Split between", roommates, default=roommates)

if st.button("Add Expense"):
    if amount > 0 and split_between:
        per_person = round(amount / len(split_between), 2)
        st.session_state.expenses.append({
            "payer": payer,
            "description": description,
            "amount": amount,
            "split_between": split_between,
            "per_person": per_person
        })
        st.success(f"Added ₹{amount:.2f} for '{description}' split among {', '.join(split_between)}")
    else:
        st.error("Please enter a valid amount and select people to split with.")

# --- Show all expenses ---
st.subheader("📋 All Expenses")
if st.session_state.expenses:
    for i, expense in enumerate(st.session_state.expenses, 1):
        st.write(f"{i}. 💸 {expense['payer']} paid ₹{expense['amount']:.2f} for **{expense['description']}**")
        st.write(f"  Split between: {', '.join(expense['split_between'])} → ₹{expense['per_person']} each")
else:
    st.info("No expenses added yet.")

# --- Calculate balances ---
st.subheader("⚖️ Final Balances")
balances = {name: 0 for name in roommates}

# Add/subtract balances based on expenses
for expense in st.session_state.expenses:
    payer = expense["payer"]
    split_between = expense["split_between"]
    per_person = expense["per_person"]
    amount = expense["amount"]

    for person in split_between:
        if person != payer:
            balances[person] -= per_person
            balances[payer] += per_person

# Display balances
for name, balance in balances.items():
    if balance > 0:
        st.success(f"✅ {name} will receive ₹{balance:.2f}")
    elif balance < 0:
        st.error(f"❌ {name} owes ₹{abs(balance):.2f}")
    else:
        st.info(f"➖ {name} is settled up.")
