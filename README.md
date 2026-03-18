# Real-Time E-Commerce Analytics Pipeline 🛒📊

A real-time data streaming pipeline built on AWS to track e-commerce 
user behaviour and calculate cart abandonment rates.

## Architecture
```
Python Script → Kinesis Streams → Lambda → Kinesis Firehose → S3 → Athena
```

## Tech Stack
- **AWS Kinesis Data Streams** — Real-time event ingestion
- **AWS Lambda (Python)** — Stream transformation & user anonymisation
- **AWS Kinesis Firehose** — Batch delivery to S3
- **Amazon S3** — Cost-effective data lake storage
- **Amazon Athena** — Serverless SQL querying

## Key Results
- ✅ Processed 600+ real-time events through the pipeline
- ✅ Highest abandonment rate: 90.48% on Desktop
- ✅ Lowest abandonment rate: 65% on Mobile devices
- ✅ Pipeline latency: under 60 seconds from event to S3

## How To Run
1. Clone this repository
2. Set up AWS services (Kinesis, Lambda, Firehose, S3, Athena)
3. Replace credentials in simulate_events_py.py with your own AWS keys
4. Install dependencies: `pip3 install boto3`
5. Run: `python3 simulate_events_py.py`
6. Query results in Athena using athena_queries.sql
