import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
import uuid
import sqlite3

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None
def init_db():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        customer_name TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        description TEXT NOT NULL,
        topic TEXT,
        urgency TEXT,
        status TEXT DEFAULT 'Open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    conn.commit()
    conn.close()
init_db()


st.set_page_config(
    page_title="Support Ticket Triage Copilot",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 Support Ticket Triage Copilot")
st.write("Classify support tickets and prepare helpful replies.")

st.divider()

st.subheader("📩 Submit a Support Ticket")

customer_name = st.text_input("Customer Name")
customer_email = st.text_input("Email Address")
ticket = st.text_area(
"Describe your problem:",
placeholder="Example: I was charged twice and need a refund.",
height=150
)
if st.button("🎫 Submit Ticket"):
    if not customer_name.strip() or not customer_email.strip() or not ticket.strip():
        st.warning("Please fill in all fields.")
    else:
        ticket_id = "TKT-" + uuid.uuid4().hex[:8].upper()

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            ticket_id, customer_name, customer_email, description, status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, customer_name, customer_email, ticket, "Open"))

    conn.commit()
    conn.close()

    st.success("Ticket submitted and saved successfully!")
    st.write("**Ticket ID:**", ticket_id)
    st.write("**Customer:**", customer_name)
    st.write("**Status:** Open")

    st.info("Save your Ticket ID so you can track your ticket later.")



def classify_ticket(message):
    text = message.lower()

    # Identify topic
    if any(word in text for word in [
        "refund", "payment", "charged", "billing", "invoice", "subscription"
    ]):
        topic = "Billing"

    elif any(word in text for word in [
        "login", "log in", "password", "account", "sign in"
    ]):
        topic = "Account"

    elif any(word in text for word in [
        "error", "crash", "bug", "not working", "technical"
    ]):
        topic = "Technical"

    else:
        topic = "General"

    # Identify urgency
    if any(word in text for word in [
        "urgent", "immediately", "critical", "right now",
        "locked out", "can't access", "cannot log in",
        "cannot login", "cannot access", "charged twice"
    ]):
        urgency = "High"

    elif any(word in text for word in [
        "soon", "asap", "quickly", "important"
    ]):
        urgency = "Medium"

    else:
        urgency = "Low"

    return topic, urgency

def analyze_ticket_with_gemma(message):
    if client is None:
        return None

    prompt = f"""
    You are a professional customer support ticket triage assistant.

Analyze the following customer support ticket:
{message}

Return exactly these three fields:

Topic: Choose one of Billing, Account, Technical, General.
Urgency: Choose one of High, Medium, Low.
Reply: Write a short, professional, empathetic response to the customer.

Rules:

* Never promise that a refund, payment reversal, or other action has already been approved or will happen immediately.
* Do not claim that an issue has been resolved when it has not.
* Ask only for information relevant to investigating the issue, such as an order number or transaction reference.
* Never ask for passwords, full card numbers, or other sensitive authentication details.
* Keep the reply clear, helpful, and concise.

    """

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt
    )

    return response.text



def draft_reply(topic):
    replies = {
        "Billing": (
            "Hello! We're sorry for the inconvenience with your payment. "
            "Our support team can review the charge. Please share your "
            "transaction reference, without sharing any card details, "
            "so we can help investigate."
        ),
        "Account": (
            "Hello! We're sorry you're having trouble with your account. "
            "Please tell us what happens when you try to sign in. "
            "Never share your password with support."
        ),
        "Technical": (
            "Hello! We're sorry you're experiencing this technical issue. "
            "Please share the error message and the steps that led to it "
            "so our team can investigate."
        ),
        "General": (
            "Hello! Thank you for contacting support. "
            "Could you share a little more detail about your concern "
            "so we can help you?"
        )
    }

    return replies[topic]


if st.button("🔍 Analyze Ticket", use_container_width=True):
    if not ticket.strip():
        st.warning("Please enter a support ticket first.")

    elif client is None:
        st.error("API key nahi mili. Apni .env file check karo.")

    else:
        try:
            with st.spinner("Gemma is analyzing your ticket..."):
                result = analyze_ticket_with_gemma(ticket)

            st.subheader("🤖 Gemma Analysis")
            st.markdown(result)

            import re

            topic_match = re.search(
                r"Topic:\s*(Billing|Account|Technical|General)",
                result,
                re.IGNORECASE
            )

            urgency_match = re.search(
                r"Urgency:\s*(High|Medium|Low)",
                result,
                re.IGNORECASE
            )

            if topic_match and urgency_match:
                topic = topic_match.group(1).capitalize()
                urgency = urgency_match.group(1).capitalize()

                conn = sqlite3.connect("tickets.db")
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE tickets
                    SET topic = ?, urgency = ?
                    WHERE description = ?
                """, (topic, urgency, ticket))

                conn.commit()
                conn.close()

                st.success("Ticket analysis saved to the database!")

            else:
                st.warning(
                    "Gemma ka response show ho gaya, lekin Topic "
                    "aur Urgency extract nahi ho sake. Please check the output."
                )

        except Exception as e:
            st.error(f"Gemma analysis failed: {e}")




st.divider()
st.header("🔎 Track Your Ticket")

search_ticket_id = st.text_input(
"Enter your Ticket ID:",
placeholder="Example: TKT-D865167D"
)

if st.button("🔍 Track Ticket"):
    if search_ticket_id.strip():
        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ticket_id, customer_name, description, topic, urgency, status, created_at FROM tickets WHERE ticket_id = ?",
            (search_ticket_id.strip().upper(),)
    )

    ticket_record = cursor.fetchone()
    conn.close()

    if ticket_record:
        st.success("Ticket found!")

        st.write("**Ticket ID:**", ticket_record[0])
        st.write("**Customer:**", ticket_record[1])
        st.write("**Problem:**", ticket_record[2])
        st.write("**Topic:**", ticket_record[3] or "Not analyzed yet")
        st.write("**Urgency:**", ticket_record[4] or "Not analyzed yet")
        st.write("**Status:**", ticket_record[5])
        st.write("**Created At:**", ticket_record[6])
    else:
        st.warning("Ticket not found. Please check your Ticket ID.")
else:
    st.warning("Please enter your Ticket ID.")

st.divider()

st.header("📊 Model Evaluation")


sample_tickets = [
    {"ticket": "I was charged twice and need a refund immediately.", "actual_topic": "Billing", "actual_urgency": "High"},
    {"ticket": "I forgot my password and cannot log in.", "actual_topic": "Account", "actual_urgency": "High"},
    {"ticket": "The application crashes whenever I open it.", "actual_topic": "Technical", "actual_urgency": "Low"},
    {"ticket": "I have a question about your services.", "actual_topic": "General", "actual_urgency": "Low"},
    {"ticket": "My invoice has an incorrect payment amount.", "actual_topic": "Billing", "actual_urgency": "Low"},
    {"ticket": "I cannot access my account because I am locked out.", "actual_topic": "Account", "actual_urgency": "High"},
    {"ticket": "The website has a bug and is not working.", "actual_topic": "Technical", "actual_urgency": "Low"},
    {"ticket": "Please resolve this urgent billing issue immediately.", "actual_topic": "Billing", "actual_urgency": "High"},
    {"ticket": "My subscription payment failed.", "actual_topic": "Billing", "actual_urgency": "Low"},
    {"ticket": "I need a refund for my last purchase.", "actual_topic": "Billing", "actual_urgency": "Low"},
    {"ticket": "I was charged twice for my order.", "actual_topic": "Billing", "actual_urgency": "High"},
    {"ticket": "Please send me a copy of my invoice.", "actual_topic": "Billing", "actual_urgency": "Low"},
    {"ticket": "My account password reset is not working.", "actual_topic": "Account", "actual_urgency": "Low"},
    {"ticket": "I cannot sign in and need access right now.", "actual_topic": "Account", "actual_urgency": "High"},
    {"ticket": "How can I update my account details?", "actual_topic": "Account", "actual_urgency": "Low"},
    {"ticket": "My account is locked and this is urgent.", "actual_topic": "Account", "actual_urgency": "High"},
    {"ticket": "The app shows an error when I save changes.", "actual_topic": "Technical", "actual_urgency": "Low"},
    {"ticket": "The website crashes every time I open it.", "actual_topic": "Technical", "actual_urgency": "Low"},
    {"ticket": "Critical: the application is not working right now.", "actual_topic": "Technical", "actual_urgency": "High"},
    {"ticket": "A bug prevents me from completing my task.", "actual_topic": "Technical", "actual_urgency": "Low"},
    {"ticket": "Can you tell me your business hours?", "actual_topic": "General", "actual_urgency": "Low"},
    {"ticket": "I have a general question about your services.", "actual_topic": "General", "actual_urgency": "Low"},
    {"ticket": "Please help me understand how your service works.", "actual_topic": "General", "actual_urgency": "Low"},
    {"ticket": "I need assistance with a question immediately.", "actual_topic": "General", "actual_urgency": "High"},
    {"ticket": "My subscription renewal payment was declined.", "actual_topic": "Billing", "actual_urgency": "Low"},
    {"ticket": "I cannot access my account and need help ASAP.", "actual_topic": "Account", "actual_urgency": "High"},
    {"ticket": "The software displays an unexpected error.", "actual_topic": "Technical", "actual_urgency": "Low"},
    {"ticket": "Please investigate this critical payment problem.", "actual_topic": "Billing", "actual_urgency": "High"},
    {"ticket": "I need help changing my account password.", "actual_topic": "Account", "actual_urgency": "Low"},
    {"ticket": "The application has a critical bug and is crashing.", "actual_topic": "Technical", "actual_urgency": "High"},
]

if st.button("Run Evaluation"):
    results = []

    for sample in sample_tickets:
        predicted_topic, predicted_urgency = classify_ticket(
            sample["ticket"]
        )

        results.append({
            "Ticket": sample["ticket"],
            "Actual Topic": sample["actual_topic"],
            "Predicted Topic": predicted_topic,
            "Actual Urgency": sample["actual_urgency"],
            "Predicted Urgency": predicted_urgency,
            "Topic Correct": (
                predicted_topic == sample["actual_topic"]
            ),
            "Urgency Correct": (
                predicted_urgency == sample["actual_urgency"]
            )
        })

    df = pd.DataFrame(results)

    topic_accuracy = df["Topic Correct"].mean() * 100
    urgency_accuracy = df["Urgency Correct"].mean() * 100

    col1, col2 = st.columns(2)

    col1.metric("Topic Accuracy", f"{topic_accuracy:.1f}%")
    col2.metric("Urgency Accuracy", f"{urgency_accuracy:.1f}%")

    st.dataframe(df, use_container_width=True)

    manual_minutes = 5
    assisted_minutes = 2
    saved = manual_minutes - assisted_minutes

    st.metric(
        "Estimated Time Saved per Ticket",
        f"{saved} minutes"
    )

    st.caption(
        "Time saved is an illustrative estimate, not a measured result. "
        "Accuracy is calculated against the sample labels."
    )