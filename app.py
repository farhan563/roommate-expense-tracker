import streamlit as st
import json
import os
import plotly.express as px

st.set_page_config(page_title="RoomMate Split", page_icon="🧾")

st.title("🧾 RoomMate Bill Split & Expense Tracker")
st.write("Track and split expenses with your roommates easily.")

# --- Load expenses from file if exists ---
if "expenses" not in st.session_state:
    try:
        if os.path.exists("data/example_data.json") and os.path.getsize("data/example_data.json") > 0:
            with open("data/example_data.json", "r") as f:
                st.session_state.expenses = json.load(f)
        else:
            st.session_state.expenses = []
    except json.JSONDecodeError:
        st.session_state.expenses = []

# --- Roommate input ---
roommates_input = st.text_input("Enter roommate names (comma separated)", "Farhan, Ali, Rehan")
roommates = [name.strip() for name in roommates_input.split(",") if name.strip()]

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

        # Save to file
        with open("data/example_data.json", "w") as f:
            json.dump(st.session_state.expenses, f, indent=4)

        st.success(f"✅ ₹{amount:.2f} for '{description}' added. Split among {', '.join(split_between)}")
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

for expense in st.session_state.expenses:
    payer = expense["payer"]
    split_between = expense["split_between"]
    per_person = expense["per_person"]

    for person in split_between:
        if person != payer:
            balances[person] -= per_person
            balances[payer] += per_person

for name, balance in balances.items():
    if balance > 0:
        st.success(f"✅ {name} will receive ₹{balance:.2f}")
    elif balance < 0:
        st.error(f"❌ {name} owes ₹{abs(balance):.2f}")
    else:
        st.info(f"➖ {name} is settled up.")

# --- Pie Chart of Total Contributions ---
st.subheader("📊 Total Contributions (Who Paid How Much?)")

total_paid = {name: 0 for name in roommates}
for expense in st.session_state.expenses:
    total_paid[expense["payer"]] += expense["amount"]

labels = []
values = []
for person, total in total_paid.items():
    if total > 0:
        labels.append(person)
        values.append(total)

if values:
    fig = px.pie(
        names=labels,
        values=values,
        title="Roommate Payment Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No payments yet to show in chart.")

# --- Reset expenses ---
st.subheader("🔁 Reset All Expenses")
if st.button("Reset All Data"):
    st.session_state.expenses = []
    with open("data/example_data.json", "w") as f:
        json.dump([], f)
    st.success("✅ All expenses have been reset.")
