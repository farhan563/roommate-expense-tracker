import streamlit as st
import json
import os
import plotly.express as px
import streamlit_authenticator as stauth

# ✅ MUST BE FIRST
st.set_page_config(page_title="Roommate Expense Tracker", page_icon="🧾")

# ------------------- LOGIN CONFIG -------------------
credentials = {
    "usernames": {
        "farhan": {
            "name": "Farhan Akthar",
            "password": "$2b$12$g0W2OgqFUqfgw9HwD.h11eFKT67OWqAp0wD6pj6SNT2TdK9S3zSBS"  # 123
        },
        "ali": {
            "name": "Ali Khan",
            "password": "$2b$12$xMpi61L6D4MV2i/tZ9kwhuSITb6Bjs7lYGxB7pyJ3azxZwjSddyoi"  # 456
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_name="roommate_login",
    key="abcdef",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status is False:
    st.error("❌ Incorrect username or password.")

elif authentication_status is None:
    st.warning("⏳ Please enter your credentials.")

elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"👋 Welcome, {name}!")

    st.title("🧾 Roommate Bill Split & Expense Tracker")
    st.write("Easily track and split expenses with your roommates.")

    # ------------------- LOAD DATA -------------------
    if "expenses" not in st.session_state:
        try:
            if os.path.exists("data/example_data.json") and os.path.getsize("data/example_data.json") > 0:
                with open("data/example_data.json", "r") as f:
                    st.session_state.expenses = json.load(f)
            else:
                st.session_state.expenses = []
        except json.JSONDecodeError:
            st.session_state.expenses = []

    # ------------------- ADD EXPENSE -------------------
    roommates_input = st.text_input("Enter roommate names (comma separated)", "Farhan, Ali, Rehan")
    roommates = [r.strip() for r in roommates_input.split(",") if r.strip()]

    st.subheader("➕ Add Expense")
    payer = st.selectbox("Who paid?", roommates)
    description = st.text_input("What was the expense?")
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
            with open("data/example_data.json", "w") as f:
                json.dump(st.session_state.expenses, f, indent=4)
            st.success(f"✅ Added ₹{amount:.2f} for '{description}' split among {', '.join(split_between)}")
        else:
            st.error("⚠️ Enter a valid amount and select roommates.")

    # ------------------- VIEW EXPENSES -------------------
    st.subheader("📋 All Expenses")
    if st.session_state.expenses:
        for i, expense in enumerate(st.session_state.expenses, 1):
            st.markdown(f"""
            **{i}.** 💸 `{expense['payer']}` paid ₹{expense['amount']} for **{expense['description']}**  
            Split: {', '.join(expense['split_between'])} → ₹{expense['per_person']} each
            """)
    else:
        st.info("No expenses yet.")

    # ------------------- BALANCES -------------------
    st.subheader("⚖️ Balances")
    balances = {name: 0 for name in roommates}
    for expense in st.session_state.expenses:
        payer = expense["payer"]
        for person in expense["split_between"]:
            if person != payer:
                balances[person] -= expense["per_person"]
                balances[payer] += expense["per_person"]

    for person, balance in balances.items():
        if balance > 0:
            st.success(f"{person} should receive ₹{balance:.2f}")
        elif balance < 0:
            st.error(f"{person} owes ₹{abs(balance):.2f}")
        else:
            st.info(f"{person} is settled up.")

    # ------------------- PIE CHART -------------------
    st.subheader("📊 Who Paid Most?")
    total_paid = {name: 0 for name in roommates}
    for expense in st.session_state.expenses:
        total_paid[expense["payer"]] += expense["amount"]

    labels = [name for name in total_paid if total_paid[name] > 0]
    values = [total_paid[name] for name in labels]

    if values:
        fig = px.pie(
            names=labels,
            values=values,
            title="Total Paid by Each Roommate",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No payments to show in chart.")

    # ------------------- RESET -------------------
    st.subheader("🗑️ Reset Expenses")
    if st.button("Reset All"):
        st.session_state.expenses = []
        with open("data/example_data.json", "w") as f:
            json.dump([], f)
        st.success("✅ All expenses cleared.")
