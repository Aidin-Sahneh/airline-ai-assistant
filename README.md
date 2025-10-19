Airline AI Assistant
====================

An AI-powered customer support assistant for an airline. This project demonstrates the implementation of OpenAI's tool-calling capabilities to enable a large language model to interact with an external SQLite database for retrieving and managing ticket prices. The application is served via a Gradio web interface.

![Airline AI Assistant Demo](demo.gif)

Key Features
------------

-   **OpenAI Tool Integration:** Utilizes the OpenAI API `tools` parameter to connect the LLM to custom Python functions.

-   **Database Interaction:** Implements functions for the AI to query and update a SQLite database (e.g., `get_ticket_price` and `set_ticket_price`).

-   **Interactive Web Interface:** A clean, responsive chat UI built with Gradio for user interaction.

-   **Multi-Step Agentic Logic:** Capable of handling sequential tool calls to fulfill complex user requests (e.g., updating a price and then confirming the new price).

Technology Stack
----------------

-   **Language:** Python

-   **LLM API:** OpenAI

-   **Web Framework:** Gradio

-   **Database:** SQLite

Local Installation and Execution
--------------------------------

Follow these steps to run the application on your local machine.

### 1\. Prerequisites

-   Python 3.8 or newer

-   An active OpenAI API Key

### 2\. Clone the Repository

```
git clone https://github.com/Aidin-Sahneh/airline-ai-assistant.git
cd airline-ai-assistant

```

### 3\. Set Up the Python Environment

Create and activate a virtual environment:

```
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate

```

### 4\. Install Dependencies

Install the required packages from `requirements.txt`:

```
pip install -r requirements.txt

```

### 5\. Configure API Key

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=sk-YourActualOpenAIKeyHere

```

### 6\. Initialize the Database

Run the database setup script one time to create the `prices.db` file and populate it with initial data:

```
python setup_database.py

```

### 7\. Run the Application

Launch the Gradio web server:

```
python app.py

```

The application will be accessible at the local URL provided in the terminal (e.g., `http://127.0.0.1:7860`).

Usage
-----

Once the application is running, you can interact with the assistant via the Gradio interface.

**Example prompts:**

-   "What is the price for a ticket to Tokyo?"

-   "Set the price for Berlin to 550."

-   "What is the price for Berlin now?"
