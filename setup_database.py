# Save this as setup_database.py
import sqlite3

DB_FILE = "prices.db"
TABLE_NAME = "prices"

# This is the function we'll also use in the main app
def set_ticket_price(city, price):
    print(f"DATABASE: Setting price for {city} to ${price}")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'INSERT INTO {TABLE_NAME} (city, price) VALUES (?, ?) '
            'ON CONFLICT(city) DO UPDATE SET price = ?',
            (city.lower(), price, price)
        )
        conn.commit()

def main():
    # 1. Create the table
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} (city TEXT PRIMARY KEY, price REAL)'
        )
        conn.commit()
        print(f"Table '{TABLE_NAME}' created successfully in '{DB_FILE}'.")

    # 2. Populate with initial data
    ticket_prices = {"london": 799, "paris": 899, "tokyo": 1420, "sydney": 2999}
    for city, price in ticket_prices.items():
        set_ticket_price(city, price)
    
    print("Database populated with initial data.")

if __name__ == "__main__":
    main()