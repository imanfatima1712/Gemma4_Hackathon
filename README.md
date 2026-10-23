# 🎫 Support Ticket Triage Copilot

### AI-Powered Customer Support using Google's Gemma

An AI-powered customer support application built with **Python, Streamlit, Google's Gemma model, and SQLite**. The application helps analyze customer complaints, suggest responses, manage support tickets, and interpret screenshots of reported issues using multimodal AI.

---

## 📌 Project Overview

Customer support teams often receive a large number of complaints that require manual review, categorization, and responses.

**Support Ticket Triage Copilot** explores how generative AI can assist with this process by analyzing written complaints and screenshots, suggesting appropriate responses, and organizing ticket information.

The project demonstrates how Google's Gemma model can be integrated into a practical application to support customer service workflows.

## ✨ Features

### 1. 📩 Support Ticket Submission

* Collects the customer's name, email address, and problem description.
* Generates a unique Ticket ID.
* Stores ticket information in an SQLite database.

### 2. 🤖 AI-Powered Ticket Analysis

* Uses Google's Gemma model to analyze written complaints.
* Generates a suggested topic and urgency level.
* Drafts a short, professional, and empathetic customer response.

**Supported topics:**

* Billing
* Account
* Technical
* General

**Urgency levels:**

* High
* Medium
* Low

### 3. 🖼️ Visual Ticket Analysis

* Accepts uploaded PNG, JPG, and JPEG images.
* Allows users to describe the reported problem in text.
* Sends the image and text prompt to the configured Gemma model.
* Generates an explanation of visible content, a possible issue category, and suggested troubleshooting steps.

For example, a user can upload a screenshot showing a login error and ask the application to help interpret it.

This feature demonstrates multimodal AI by combining image and text inputs.

### 4. 🔎 Ticket Tracking

* Retrieves a ticket using its unique Ticket ID.
* Displays saved ticket details.
* Shows the ticket status, creation time, and any saved topic and urgency information.

### 5. 📊 Model Evaluation

* Includes a sample dataset of 30 support tickets.
* Compares rule-based topic and urgency predictions against predefined sample labels.
* Calculates topic and urgency accuracy.
* Displays the evaluation results in a table.
* Shows an illustrative estimate of potential time saved per ticket.

**Note:** The evaluation uses a small, predefined sample dataset and a rule-based classification function. Its accuracy figures do not represent guaranteed real-world performance or a comprehensive benchmark of Gemma itself. The estimated time saved is illustrative, not measured.

---

## 🛠️ Technology Stack

| Technology         | Purpose                                             |
| ------------------ | --------------------------------------------------- |
| Python             | Application logic                                   |
| Streamlit          | Interactive web interface                           |
| Google Gemma       | AI-based complaint analysis and response generation |
| Google GenAI SDK   | Communication with the configured AI model          |
| SQLite             | Local support-ticket database                       |
| Pandas             | Evaluation tables and data handling                 |
| Python `re` module | Extracting topic and urgency from model responses   |
| python-dotenv      | Loading environment variables                       |

---

## ⚙️ How It Works

1. The user submits a support ticket.
2. The application generates a unique Ticket ID.
3. Ticket information is stored in SQLite.
4. The user can request AI analysis of the written complaint.
5. Gemma generates a topic, urgency level, and suggested response.
6. The application attempts to extract the topic and urgency and save them to the ticket record.
7. The user can retrieve ticket details using the Ticket ID.
8. For visual analysis, the user uploads an image and provides a text description.
9. The application sends both inputs to the configured model and displays its response.
10. The evaluation section measures the rule-based classifier against predefined sample labels.

---

## 📋 Requirements

Before running the application, make sure you have:

* Python installed.
* Git installed.
* A Google Gemini API key that supports access to the configured model.
* An internet connection for API-based AI requests.

The configured model name in the current application is `gemma-4-31b-it`. Model availability, API access, and image-input support depend on the service configuration.

---

## 🚀 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/imanfatima1712/Gemma4_Hackathon.git
```

### Step 2: Open the Project Folder

```bash
cd Gemma4_Hackathon
```

### Step 3: Create a Virtual Environment (Recommended)

**Windows:**

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies

Install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

The required packages are:

```text
streamlit
pandas
python-dotenv
google-genai
```

### Step 5: Configure the API Key

Create a file named `.env` in the project root directory.

Add the following line:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own valid API key.

**Security:** Never commit your actual API key to GitHub. Keep `.env` out of version control.

### Step 6: Run the Application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local address where you can open the application in your browser.

---

## 📂 Project Structure

```text
Gemma4_Hackathon/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .env                # Local API key (not committed)
├── .gitignore          # Files excluded from Git
└── tickets.db          # Local SQLite database, created at runtime
```

The exact files present may vary depending on your local setup.

---

## 🧪 Testing the Application

### Test 1: Billing Complaint

Example:

> I was charged twice and need a refund immediately.

Expected behavior:

* The AI should analyze the complaint.
* It should suggest a relevant category and urgency.
* It should draft an appropriate response without promising an unapproved refund.

### Test 2: Account Access

Example:

> I cannot log in to my account because I receive an invalid password error.

Expected behavior:

* The AI should identify the likely authentication issue.
* It should suggest relevant troubleshooting steps.

### Test 3: Visual Analysis

1. Open the Visual Ticket Analysis section.
2. Upload a relevant error screenshot.
3. Describe the issue in the text field.
4. Click **Analyze Image with Gemma**.
5. Review the generated explanation and suggestions.

Do not upload screenshots containing passwords, API keys, financial information, or other sensitive data.

### Test 4: Ticket Tracking

1. Submit a ticket.
2. Copy its Ticket ID.
3. Enter the ID in the tracking section.
4. Check the retrieved ticket information.

### Test 5: Model Evaluation

Open the Model Evaluation section and click **Run Evaluation** to view the sample results.

---

## 🔐 Privacy and Security

* Store API credentials in environment variables.
* Never publish API keys or passwords.
* Use synthetic or appropriately redacted screenshots for public demonstrations.
* The current prototype stores ticket information locally in SQLite.
* A production deployment would require stronger authentication, access controls, data protection, and appropriate handling of customer information.

---

## ⚠️ Current Limitations

* AI-generated classifications and suggestions may be incorrect.
* AI analysis depends on API availability and valid credentials.
* The evaluation dataset is small and predefined.
* The rule-based evaluation function is separate from the Gemma-based analysis.
* Visual-analysis results are displayed but are not currently saved with the ticket.
* The current prototype has basic ticket-management functionality and should not be treated as a complete production support system.

---

## 🔮 Future Improvements

* Add customer and administrator authentication.
* Improve ticket status management.
* Save AI analysis and visual-analysis results with each ticket.
* Expand and improve the evaluation dataset.
* Test performance across more varied complaints and screenshots.
* Add stronger error handling and input validation.
* Improve data protection and production deployment security.
* Explore additional analytics for support-ticket trends.

---

## 🎯 Project Goal

The goal of Support Ticket Triage Copilot is to explore how generative and multimodal AI can assist customer support workflows through complaint analysis, suggested responses, ticket organization, and screenshot interpretation.

This project was developed as a practical exploration of AI integration and application development using Google's Gemma model.

---

## 👩‍💻 Author

**Iman Fatima**
Computer Science Student
University of Agriculture Faisalabad

GitHub: [imanfatima1712](https://github.com/imanfatima1712)

---

## 📄 License

A license has not yet been specified for this repository. Add a `LICENSE` file if you intend to distribute the project under a particular open-source license.
