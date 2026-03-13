import json
import psycopg2
from kafka import KafkaConsumer

# Kafka consumer
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="streaming_db",
    user="airflow",
    password="airflow"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS staging_orders (
        id SERIAL PRIMARY KEY,
        order_id INTEGER,
        customer_id INTEGER,
        product_id INTEGER,
        amount DECIMAL(10,2),
        created_at TIMESTAMP,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()
print("Table 'staging_orders' is ready")

# Process messages
for message in consumer:
    order = message.value
    
    cursor.execute("""
        INSERT INTO staging_orders (order_id, customer_id, product_id, amount, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        order["order_id"],
        order["customer_id"],
        order["product_id"],
        order["amount"],
        order["created_at"]
    ))
    
    conn.commit()
    print(f"Inserted: order_id={order['order_id']}, amount={order['amount']}")