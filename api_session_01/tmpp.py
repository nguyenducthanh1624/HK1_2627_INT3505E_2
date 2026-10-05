import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the existing database
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    orderId INTEGER PRIMARY KEY AUTOINCREMENT,
    customerId INTEGER NOT NULL,
    status TEXT NOT NULL,
    total REAL NOT NULL
    
)
''')

# Reference data for generating realistic orders
statuses = ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
streets = ["Maple St", "Oak Ave", "Pine Rd", "Cedar Blvd", "Elm St", "Main St"]
cities = ["Springfield", "Riverside", "Franklin", "Clinton", "Fairview"]

new_orders = []
now = datetime.now()

# Generate 20 random orders
for _ in range(20):
    customer_id = random.randint(1000, 9999)
    status = random.choice(statuses)
    
    
    
    # Generate a random price between $10 and $500
    total = round(random.uniform(10.0, 500.0), 2)
    
    # Construct a realistic looking address
    
    
    new_orders.append((customer_id, status,  total))

# Insert the batch of 20 orders
cursor.executemany('''
INSERT INTO orders (customerId, status, total)
VALUES (?, ?, ?)
''', new_orders)

conn.commit()

# Verify the total count in the table
cursor.execute("SELECT COUNT(*) FROM orders")
total_count = cursor.fetchone()[0]

print(f"Successfully inserted {cursor.rowcount} new orders.")
print(f"Total orders now in the database: {total_count}")

conn.close()