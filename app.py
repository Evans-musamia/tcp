import socket
import threading
import re
import paho.mqtt.client as mqtt

HEADER = 64
PORT = 8081
FORMAT = "utf-8"
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    mqtt_broker = "mqtt-factory.omnivoltaic.com"
    mqtt_port = 1883
    mqtt_username = "Admin"
    mqtt_password = "7xzUV@MT"
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)

                msg = conn.recv(msg_length).decode(FORMAT)
                #print(msg)
                pattern = r'"devId":"([^"]+)"'
                match = re.search(pattern, msg)

                if match:
                    dev_id = match.group(1)
                else:
                    print("devId not found in the JSON string.")

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                def on_publish(client, userdata, result):
                    print("Message published successfully")

                # Create MQTT client
                mqtt_client = mqtt.Client()

                # Set username and password
                mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)

                # Connect to the MQTT broker
                mqtt_client.connect(mqtt_broker, mqtt_port)

                # Set the callback function for when a message is published
                mqtt_client.on_publish = on_publish

                # Publish the JSON payload to the specified topic
                mqtt_client.publish(dev_id, msg)

                # Wait for the message to be published (you can adjust the time based on your needs)
                mqtt_client.loop_start()
                mqtt_client.loop_stop()

                # Disconnect from the MQTT broker
                mqtt_client.disconnect()

                print(f"[{addr}] dt/oves/{dev_id}")

        except ConnectionResetError:
            # Handle case where the connection was reset by the client
            connected = False
        except Exception as e:
            print(f"An error occurred: {e}")
            connected = False

    print(f"[CONNECTION CLOSED] {addr}")
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting ...")
start()
