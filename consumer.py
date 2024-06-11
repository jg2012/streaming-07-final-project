import pika
import sys
import os

def main():
    player_name = input("Enter the player name to listen for: ").strip()

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="hello")

        def callback(ch, method, properties, body):
            message = body.decode()
            # Extract the winner from the message
            parts = message.split(', ')
            winner = None
            for part in parts:
                if part.startswith("Winner: "):  # Make sure the key matches exactly
                    winner = part.split(": ")[1].strip()
                    break

            # Check if the player's name is in the winner's name
            if winner and player_name.lower() in winner.lower():
                alert_message = f"We found your player! Message: {message}"
                print(alert_message)

        channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)
        print(f" [*] Listening for player: {player_name}. To exit press CTRL+C")
        channel.start_consuming()

    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
