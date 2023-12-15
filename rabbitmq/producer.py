import pika
import time

for i in range(100):    # Send 100 Messages on the intercommunication bus
    connection_parameters = pika.ConnectionParameters('localhost')

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.queue_declare(queue='letterbox', arguments={'x-max-length': 100})   # Define max lenght of the queue 

    message = "Hello, this is the {} message I send".format(i+1)

    channel.basic_publish(exchange='', routing_key='letterbox', body= message)

    print(f"sent message: {message}")

    connection.close()
    time.sleep(6)

