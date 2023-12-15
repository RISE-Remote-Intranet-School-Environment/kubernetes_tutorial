# Intercommunication bus

# Goal

My part of the project was to create an intercommunication bus. An intercommunication bus in microservices architecture is a message-oriented communication system that enables microservices to interact indirectly through a central messaging layer. **Microservices will send messages to each other via an intercommunication bus. Instead of sending messages to each other, they will send messages on the intercommunication bus and read messages that interest them on the bus.** This approach ensures loose coupling, scalability, and flexibility, allowing microservices to evolve independently. Messages are sent and received through the bus, promoting a decentralized and event-driven architecture. Message brokers or middleware handle the routing and delivery of messages, facilitating reliable and asynchronous communication between microservices.


In order to do this we had several choice :
- Kafka
- RabbitMQ


I choosed RabbitMQ for his implementation with Kubernetes. 

# RabbitMQ

RabbitMQ enables the creation of an intercommunication bus between microservices by serving as a message broker. Microservices can communicate indirectly through RabbitMQ by sending and receiving messages. Each microservice interacts with RabbitMQ, publishing messages to specific "exchanges" and subscribing to relevant "queues". Message are put on the intercommunication bus and microservices can access to the bus to read only the messages they are interested in. This intercommunication bus where messages are stored is represented as a queue in RabbitMQ. The **queue** is the **intercommunication bus**: it contains all the messages. RabbitMQ then routes messages from producers to the appropriate consumers based on message types or routing keys. This approach ensures loose coupling, scalability, and asynchronous communication, allowing microservices to exchange information without direct dependencies.

# Docker


Docker is a platform that enables the development, deployment, and running of applications inside containers. These containers are lightweight, self-contained units that encompass everything necessary to run software, from code and runtime to libraries and system tools. Docker introduces a standardized approach to package and distribute applications, ensuring their portability and consistency across diverse environments.

## Application to RabbitMQ:
In the context of RabbitMQ, Docker proves invaluable by encapsulating the messaging broker and its dependencies within containers. This not only ensures a uniform and isolated environment but also simplifies the deployment process. To illustrate, the initialization of a RabbitMQ server involves a straightforward Docker command:

## Implementation

First install Docker. https://docs.docker.com/engine/install .
Then create a container, open the terminal and use the command : 

```
docker run -d --hostname rmq --name rabbit-server -p 8080:15672 -p 5672:5672 rabbitmq:3-management
```

In Docker you will see a RabbitMQ container with status running. Click on the port number (it is a link) to open RabbitMQ server. It opens a web page to login to RabbitMQ. The user name and password are "guest". You now have a RabbitMQ server installed. Docker runs RabbitMQ locally.



# Send and receive messages on the intercommunication bus using Python

what I did is based from this tutorial, you can follow it for comprehension but I implemented new things that are not in the tutorial : https://www.youtube.com/watch?v=kwQDpHcM4HM

I did a simple implementation of the intercommunication bus in Python. There will be a producer that will send messages on the communication bus and a consumer that will read the messages. You can find a file for each one and you can runs those files at the same time in differents terminals. 
You will see that the producer send message to RabbitMQ. You will be able to see them on the RabbitMQ interface. And by running the consumer file, you will be able to read those messages. Let's do it step by step.

### Implementation

First install pika:
```
pip install pika
```

The producer will send messages and consumer read them. You can find those file in the folder.

Let's test it. Begin by Running docker application (you first have to install Docker on your computer).
Create a rabbitmq container on Docker by running this command on the terminal: 

```
docker run -d --hostname localhost --name rabbit-server -p 8080:15672 -p 5672:5672 rabbitmq:3-management
```

In Docker your will see a new container named "rabbit-server". You will see a link on the port section of the container. It will open RabbitMQ web page http://localhost:8080/#/queues. You can see RabbitMQ running locally.

In a terminal run python producer code :
```
python producer.py
```
You can see in the terminal that the producer is sending message on the intercommunication bus, on the RabbitMQ queue.

On the rabbitmq page web, in the "connection" part you can see that you have a new connection running. In the "queues and stream" on you can see your queue : "letterbox" and messages appearing in it. It is the producer which is sending message on the intercommunication bus. 

In another terminal run python code :
```
python consumer.py
```

You can see that the consumer is able to read messages from the intercommunication bus.

On the RabbitMq web page (part "Queue and stream"), you can see your messages sitting on the queue.

### Explaination of the code

On the declaration of the channel, the argument {'x-max-length': 100} limit the RabbitMQ queue, in other words the intercommunication bus, to store a maximum of 100 messages. This means that old messages will be automatically deleted after 100 new messages have been had on the intercommunication bus.
```
channel.queue_declare(queue='letterbox', arguments={'x-max-length': 100})
```

```
channel.basic_consume(queue='letterbox', auto_ack=False, on_message_callback=on_message_received)
```
If auto_ack=True the consumer will delete the messages on the intercommunication bus after reading it. It would be good for a single consumer.

For several microservices, there are several consumers and messages that stays on the intercomunication bus so that every consumers can read the same message. We have to put the parameter auto_ack=False.

# What's next ?
The most important thing is to implement the intercommunication bus with the rest of the project. You have to **implement RabbitMQ on Kubernetes**.

Other points to take into account are:
- Consumers can read specific messages that interest them.
- There is a priority system on messages so that important messages are delete after the less important messages.


# Using other languages
I tried to use other languages than python but had problems.

### Using C#
In C# I couldn't completely download the .NET extension that we need to communicate with RabbitMQ. Here is the tutorial I followed: https://youtu.be/bfVddTJNiAw?si=sKObgYQsFrQCOajZ


### Using Java
It would be interesting to use Java to communicate with RabbitMQ so that we use Java as the language for all the project of the course.

Here is the tutorial I followed : https://www.youtube.com/watch?v=Gj9YiBfJKxk&list=PL1xVF1dBM4bnc-NeY-yBMvJuKXY6IY9yP&index=1

### With Kubernetes
Here is the tutorial I beginned to follow to implement RabbitMQ on Kubernetes: https://www.youtube.com/watch?v=_lpDfMkxccc.






Thibaut François 195195




