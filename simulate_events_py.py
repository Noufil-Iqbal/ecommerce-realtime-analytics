# -*- coding: utf-8 -*-


import boto3
import json
import random
import time
from datetime import datetime, timedelta

# Configure this with your AWS credentials
kinesis = boto3.client(
    'kinesis',
    region_name='eu-north-1',
    aws_access_key_id='YOUR_ACCESS_KEY_HERE',      
    aws_secret_access_key='YOUR_SECRET_KEY_HERE'   
)

STREAM_NAME = 'ecommerce-events-stream'

PRODUCTS = [
    {'id': 'P001', 'name': 'Wireless Headphones', 'price': 79.99},
    {'id': 'P002', 'name': 'Running Shoes', 'price': 124.99},
    {'id': 'P003', 'name': 'Coffee Maker', 'price': 49.99},
    {'id': 'P004', 'name': 'Yoga Mat', 'price': 34.99},
    {'id': 'P005', 'name': 'Laptop Stand', 'price': 29.99},
]

def generate_event():
    """Generate a realistic e-commerce event"""
    session_start = datetime.utcnow() - timedelta(seconds=random.randint(10, 300))
    event_time = datetime.utcnow()
    product = random.choice(PRODUCTS)

    # 70% chance of add_to_cart, 30% chance of purchase
    # This creates a natural abandonment rate of ~70%
    event_type = random.choices(
        ['add_to_cart', 'purchase'],
        weights=[70, 30]
    )[0]

    return {
        'event_id': f"evt_{random.randint(100000, 999999)}",
        'event_type': event_type,
        'event_time': event_time.isoformat(),
        'user_id': f"user_{random.randint(1000, 9999)}",   # Will be anonymised by Lambda
        'session_id': f"sess_{random.randint(10000, 99999)}",
        'session_start': session_start.isoformat(),
        'product_id': product['id'],
        'product_name': product['name'],
        'product_price': product['price'],
        'quantity': random.randint(1, 3),
        'page': random.choice(['homepage', 'product_page', 'search', 'recommendations']),
        'device': random.choice(['mobile', 'desktop', 'tablet']),
        'country': random.choice(['US', 'UK', 'CA', 'AU', 'PK', 'IN'])
    }

def send_events(events_per_second=5, duration_seconds=60):
    """Send events to Kinesis for a specified duration"""
    print(f"🚀 Starting event simulation...")
    print(f"   Sending ~{events_per_second} events/second for {duration_seconds} seconds")
    print(f"   Total expected: ~{events_per_second * duration_seconds} events\n")

    total_sent = 0
    start_time = time.time()

    while time.time() - start_time < duration_seconds:
        batch = []

        for _ in range(events_per_second):
            event = generate_event()
            batch.append({
                'Data': json.dumps(event).encode('utf-8'),
                'PartitionKey': event['session_id']  # Groups events by session
            })

        # Send batch to Kinesis
        response = kinesis.put_records(
            Records=batch,
            StreamName=STREAM_NAME
        )

        failed = response.get('FailedRecordCount', 0)
        sent = len(batch) - failed
        total_sent += sent

        print(f"✅ Sent {sent} events | Total: {total_sent} | Failed: {failed}")
        time.sleep(1)

    print(f"\n🎉 Simulation complete! Total events sent: {total_sent}")

if __name__ == '__main__':
    send_events(events_per_second=5, duration_seconds=120)
