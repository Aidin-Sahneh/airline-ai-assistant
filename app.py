# Save this as app.py
import os
import json
import sqlite3
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# --- 1. Initialization ---
load_dotenv(override=True)
openai = OpenAI() # API key is read from .env automatically
MODEL = "gpt-4o-mini" # Using a more modern model, but gpt-4.1-mini is also fine
DB_FILE = "prices.db"

# --- 2. System Message ---
system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

# --- 3. Tool Implementations (Python Functions) ---
# These are the actual Python functions the LLM can ask us to run.

def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
        result = cursor.fetchone()
        if result:
            return f"The ticket price to {city} is ${result[0]}."
        else:
            return f"No price data available for {city}."

def set_ticket_price(city, price):
    print(f"DATABASE TOOL CALLED: Setting price for {city} to ${price}", flush=True)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO prices (city, price) VALUES (?, ?) '
            'ON CONFLICT(city) DO UPDATE SET price = ?',
            (city.lower(), price, price)
        )
        conn.commit()
    return f"The ticket price for {city} has been updated to ${price}."

# --- 4. Tool Definitions (JSON Schema) ---
# This is how we describe our Python functions to the LLM.

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_price",
            "description": "Get the price of a return ticket to the destination city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination_city": {
                        "type": "string",
                        "description": "The city that the customer wants to travel to",
                    },
                },
                "required": ["destination_city"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_ticket_price",
            "description": "Set or update the price of a ticket for a specific city. This is an admin-only action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The destination city.",
                    },
                    "price": {
                        "type": "number",
                        "description": "The new price for the ticket."
                    }
                },
                "required": ["city", "price"],
                "additionalProperties": False
            }
        }
    }
]

# Map tool names to their actual Python functions
available_tools = {
    "get_ticket_price": get_ticket_price,
    "set_ticket_price": set_ticket_price,
}

# --- 5. Tool Handling Logic ---

def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_tools.get(function_name)
        
        if not function_to_call:
            print(f"Error: Model tried to call unknown function '{function_name}'")
            continue

        try:
            arguments = json.loads(tool_call.function.arguments)
            
            # Use **arguments to pass them as keyword arguments
            function_response = function_to_call(**arguments)
            
            responses.append({
                "role": "tool",
                "content": function_response,
                "tool_call_id": tool_call.id
            })
        except json.JSONDecodeError:
            print(f"Error: Could not decode arguments for {function_name}")
        except TypeError as e:
            print(f"Error: Incorrect arguments for {function_name}: {e}")

    return responses

# --- 6. Main Chat Function ---
# This is the final version from your notebook, using a 'while' loop
# to handle multiple sequential tool calls.

def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    
    response = openai.chat.completions.create(
        model=MODEL, 
        messages=messages, 
        tools=tools
    )

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_responses = handle_tool_calls(message)
        
        messages.append(message)
        messages.extend(tool_responses)
        
        response = openai.chat.completions.create(
            model=MODEL, 
            messages=messages, 
            tools=tools
        )
    
    return response.choices[0].message.content

# --- 7. Launch Gradio Interface ---
gr.ChatInterface(fn=chat, title="FlightAI Assistant", type="messages").launch()