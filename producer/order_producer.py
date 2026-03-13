import json
import time
import random
from datetime import datetime, timezone  
from kafka import KafkaProducer

# Connect to Kafka running on localhost
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Create a single order with random values
def generate_order():
    return {
        "order_id": random.randint(1000, 9999),
        "customer_id": random.randint(1, 100),
        "product_id": random.randint(1, 50),
        "amount": round(random.uniform(10, 200), 2),
        "created_at": datetime.now(timezone.utc).isoformat()  
    }

# Run the producer continuously until stopped
if __name__ == "__main__":
    print("Starting Kafka producer...")
    print("Press Ctrl+C to stop\n")
    count = 0
    
    while True:
        order = generate_order()
        producer.send("orders", order)
        count += 1
        print(f"[{count}] Sent: {order}")
        time.sleep(2)
   