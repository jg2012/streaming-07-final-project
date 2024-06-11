import pika
import csv
import time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="hello")

# CSV file variable
atp_tennis = "atp_tennis.csv"

with open(atp_tennis, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)
    
    for row in csvreader:
        message = ', '.join(f"{header}: {value}" for header, value in zip(headers, row))
        channel.basic_publish(exchange="", routing_key="hello", body=message)
        print(f" [x] Sent '{message}'")
        time.sleep(3)

connection.close()