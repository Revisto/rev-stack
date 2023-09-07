import os
from dotenv import load_dotenv
load_dotenv()

class RabbitMQConfig:
    host = os.getenv("RABBITMQ_HOST")
    port = os.getenv("RABBITMQ_PORT")
    username = os.getenv("RABBITMQ_USERNAME")
    password = os.getenv("RABBITMQ_PASSWORD")