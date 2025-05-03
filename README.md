# Mental Health Chatbot App

This is a Quart-based web application. Follow the steps below to set up the virtual environment and start the app locally. Requires Python 3.8.10.

You'll need an API key for IBM Watson Natural Language Understanding v1 for chatbot.py and
sentiment_analysis.py

## Setup Instructions

### 1️⃣ Create and Activate a Virtual Environment

**On Windows:**

```sh
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```sh
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies

Once the virtual environment is activated, install the required packages:

```sh
pip install -r requirements.txt
```

### 3️⃣ Start the Application

Run the following command to start the Quart server:

```sh
quart run
```

By default, the app will be available at:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

### 4️⃣ Troubleshooting

If you encounter missing NLTK data errors, run:

```python
import nltk
nltk.download('punkt_tab')
```

---

Let me know if you need any modifications! 🚀
