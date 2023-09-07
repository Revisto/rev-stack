
import pika

from config import RabbitMQConfig


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()


class RabbitMQSender:
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
   
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None


    def connect(self, queue="stackoverflow-questions"):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host,
                                               port=self.port,
                                               credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=True)

    def send_message(self, exchange, routing_key, message):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=message)
        print("Sent message: %r" % message)

    def disconnect(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


# sender = RabbitMQSender(host=RabbitMQConfig.host, port=RabbitMQConfig.port, username=RabbitMQConfig.username, password=RabbitMQConfig.password)
# sender.connect(queue="stackoverflow-questions")
# sender.send_message(exchange="", routing_key="stackoverflow-questions", message="Message")