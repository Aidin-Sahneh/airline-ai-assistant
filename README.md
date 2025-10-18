# Airline AI Assistant

An AI-powered customer support assistant for an airline. This project demonstrates the implementation of OpenAI's tool-calling capabilities to enable a large language model to interact with an external SQLite database for retrieving and managing ticket prices. The application is served via a Gradio web interface.

This project was developed as part of the "LLM Engineering" course by Ed Donner on Udemy.

## Key Features

* **OpenAI Tool Integration:** Utilizes the OpenAI API `tools` parameter to connect the LLM to custom Python functions.
* **Database Interaction:** Implements functions for the AI to query and update a SQLite database (e.g., `get_ticket_price` and `set_ticket_price`).
* **Interactive Web Interface:** A clean, responsive chat UI built with Gradio for user interaction.
* **Multi-Step Agentic Logic:** Capable of handling sequential tool calls to fulfill complex user requests (e.g., updating a price and then confirming the new price).

## Technology Stack

* **Language:** Python
* **LLM API:** OpenAI
* **Web Framework:** Gradio
* **Database:** SQLite

## Local Installation and Execution

Follow these steps to run the application on your local machine.

### 1. Prerequisites

* Python 3.8 or newer
* An active OpenAI API Key

### 2. Clone the Repository

```bash
git clone [https://github.com/Aidin-Sahneh/airline-ai-assistant.git](https://github.com/Aidin-Sahneh/airline-ai-assistant.git)
cd airline-ai-assistant