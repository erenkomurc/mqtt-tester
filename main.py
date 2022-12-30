import json
import paho.mqtt.client as mqtt
import traceback
import time

# Global config dictionary
config = dict()

# MQTT Return Codes
returnCodes = {
    0: "Connection successful",
    1: "Connection refused - incorrect protocol version",
    2: "Connection refused - invalid client identifier",
    3: "Connection refused - server unavailable",
    4: "Connection refused - bad username or password",
    5: "Connection refused - not authorised"
}

# Flag for MQTT message match.
message_match = list()

def read_config():
    global config
    try:
        with open("config.json", "r") as json_file:
            config = json.load(json_file)
    except:
        pass
    if "ip" not in config:
        config["ip"] = input("ip: ")
    if "port" not in config:
        config["port"] = int(input("port: "))
    if "username" not in config:
        config["username"] = input("username: ")
    if "password" not in config:
        config["password"] = input("password: ")
    if "sub_topic" not in config:
        config["sub_topic"] = input("sub_topic: ")
    if "pub_topic" not in config:
        config["pub_topic"] = input("pub_topic: ")
    if "payload_file_path" not in config:
        config["payload_file_path"] = input("payload_file_path: ")
    if "interval" not in config:
        config["interval"] = int(input("interval: "))
    if "count" not in config:
        config["count"] = int(input("count: "))

    # Save changes to the config file.
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

def edit_config():
    print("Enter new values. Press enter to leave the current value unchanged.")
    print("ip current value: ", config["ip"], "\nNew Value: ", end="")
    new_value = input()
    config["ip"] = new_value if new_value != "" else config["ip"]
    print("port current value: ", config["port"], "\nNew Value: ", end="")
    new_value = input()
    config["port"] = int(new_value) if new_value != "" else config["port"]
    print("username current value: ", config["username"], "\nNew Value: ", end="")
    new_value = input()
    config["username"] = new_value if new_value != "" else config["username"]
    print("password current value: ", config["password"], "\nNew Value: ", end="")
    new_value = input()
    config["password"] = new_value if new_value != "" else config["password"]
    print("sub_topic current value: ", config["sub_topic"], "\nNew Value: ", end="")
    new_value = input()
    config["sub_topic"] = new_value if new_value != "" else config["sub_topic"]
    print("pub_topic current value: ", config["pub_topic"], "\nNew Value: ", end="")
    new_value = input()
    config["pub_topic"] = new_value if new_value != "" else config["pub_topic"]
    print("payload_file_path current value: ", config["payload_file_path"], "\nNew Value: ", end="")
    new_value = input()
    config["payload_file_path"] = new_value if new_value != "" else config["payload_file_path"]
    print("interval current value (ms) : ", config["interval"], "\nNew Value: ", end="")
    new_value = input()
    config["interval"] = int(new_value) if new_value != "" else config["interval"]
    print("count current value: ", config["count"], "\nNew Value: ", end="")
    new_value = input()
    config["count"] = int(new_value) if new_value != "" else config["count"]

    # Save changes to the config file.
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

def mode_1():
    if config["count"] == 0:
        while True:
            response = client.publish(config["pub_topic"], payload=payload)
            print("Publish successful." if response.rc == 0 else "Payload could not be published.")
            time.sleep(config["interval"] / 1000)
    else:
        for count in range(config["count"]):
            response = client.publish(config["pub_topic"], payload=payload)
            print("Publish successful." if response.rc == 0 else "Payload could not be published.")
            time.sleep(config["interval"] / 1000)

def mode_2():
    client.subscribe(config["sub_topic"], qos=0)
    client.loop()
    global message_match
    missed_messages = 0
    while config["count"] == 0:
        config["count"] = int(input("Infinite count is not accepted. New count value: "))
    for count in range(config["count"]):
        message_match.append(False)
        response = client.publish(config["pub_topic"], payload=(payload + "_" + str(count)))
        print("Publish", count, "successful." if response.rc == 0 else "Payload could not be published.")
        time.sleep(config["interval"] / 1000)
        count += 1

    time.sleep(5)

    print("Missed messages: ", end="")
    for i in range(len(message_match)):
        if not message_match[i]:
            print(f", {i}" if missed_messages != 0 else i, end="")
            missed_messages += 1
    print("")
    print("Number of missed messages:", missed_messages)


def on_message(client, userdata, msg):
    global message_match
    # print(f"{msg.topic}: {msg.payload.decode('utf-8')}\n")
    message_payload = msg.payload.decode('utf-8')
    counter = int(message_payload.split('_')[-1].strip())
    message_match[counter] = True


def on_connect(client, userdata, flag, rc):
    print(returnCodes[rc], end="\n\n")

def on_disconnect(client, userdata, rc):
    print("Disconnected.")


if __name__ == '__main__':
    read_config()
    
    # Select mode
    while True:
        mode  = input("Select Mode, 1 or 2. Enter 0 to edit configurations. ")
        if mode == '0':
            edit_config()
        elif mode == '1' or mode == '2':
            break
        else:
            print("Invalid Input.")

    # Read payload
    try:
        with open(config["payload_file_path"], "r", encoding="utf-8") as payload_file:
            payload = payload_file.read()
    except:
        print("Payload file could not be read.")

    # Connect to MQTT client
    try:
        client = mqtt.Client(client_id="mqtt_app_1917", clean_session=True)
        client.on_message = on_message
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect

        client.username_pw_set(config["username"], config["password"])
        client.connect(host=config["ip"], port=config["port"])
        client.loop_start()
    except:
        print(traceback.format_exc())
        time.sleep(5)
        quit()

    if mode == '1':
        mode_1()
    else:
        mode_2()

    client.loop_stop()
    client.disconnect()

    # Save final configurations
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
