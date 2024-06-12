import pika
import sys
import os

def main():
    player_name = input("Enter the player name to listen for: ").strip().lower()

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="atp_tennis")

        def callback(ch, method, properties, body):
            message = body.decode()
            # Extract relevant fields from the message
            parts = message.split(', ')
            winner = None
            player_1 = None
            player_2 = None
            for part in parts:
                if part.startswith("Winner: "):
                    winner = part.split(": ")[1].strip().lower()
                elif part.startswith("Player_1: "):
                    player_1 = part.split(": ")[1].strip().lower()
                elif part.startswith("Player_2: "):
                    player_2 = part.split(": ")[1].strip().lower()

            # Check if the player is playing
            if player_name in (player_1, player_2):
                opponent = player_1 if player_name == player_2 else player_2
                alert_message = f"Your player {player_name.capitalize()} is playing against {opponent.capitalize()}."
                print(alert_message)

                # Check if the player won
                if winner and player_name == winner:
                    win_message = f"Your player won the match! Message: {message}"
                    print(win_message)
                else:
                    loss_message = f"Your player lost the match. Message: {message}"
                    print(loss_message)

        channel.basic_consume(queue="atp_tennis", on_message_callback=callback, auto_ack=True)
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
