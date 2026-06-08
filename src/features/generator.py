import random
import time
import json
import logging
from datetime import datetime
from kafka import KafkaProducer
from src.features.transaction import Transaction, TransactionType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCATIONS = [
    "Karachi", "Lahore", "Islamabad",
    "Peshawar", "Quetta", "Multan"
]

USERS = [f"user_{i}" for i in range(1, 51)]


def create_fake_transaction(fraud: bool = False) -> Transaction:
    user_id = random.choice(USERS)

    if fraud:
        amount = random.uniform(50000, 500000)
    else:
        amount = random.uniform(100, 50000)

    return Transaction(
        user_id=user_id,
        amount=round(amount, 2),
        transaction_type=random.choice(list(TransactionType)),
        location=random.choice(LOCATIONS),
        is_fraud=fraud
    )


def start_generator(bootstrap_servers: str, topic: str):
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    logger.info(f"Generator started → topic: {topic}")

    while True:
        is_fraud = random.random() < 0.02
        transaction = create_fake_transaction(fraud=is_fraud)

        producer.send(
            topic,
            value=transaction.model_dump(mode='json')
        )

        logger.info(
            f"Sent → user: {transaction.user_id} | "
            f"amount: {transaction.amount} | "
            f"fraud: {transaction.is_fraud}"
        )

        time.sleep(0.1)


if __name__ == "__main__":
    start_generator(
        bootstrap_servers="localhost:9092",
        topic="transactions"
    )
