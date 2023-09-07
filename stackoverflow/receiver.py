import pika
from config import RabbitMQConfig


class RabbitMQReceiver:
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

    def receive_message(self, queue="stackoverflow-questions"):
        self.channel.basic_consume(queue=queue,
                                   on_message_callback=self.callback,
                                   auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)



# rabbitmq_receiver = RabbitMQReceiver(host=RabbitMQConfig.host, port=RabbitMQConfig.port, username=RabbitMQConfig.username, password=RabbitMQConfig.password)
# rabbitmq_receiver.connect(queue="stackoverflow-questions")
# rabbitmq_receiver.receive_message(queue="stackoverflow-questions")