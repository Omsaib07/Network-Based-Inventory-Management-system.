import socket
import threading
import csv
import os

filename = "inventory.csv"

def load_inventory_from_file(filename):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            inventory = {rows[0]: int(rows[1]) for rows in reader}
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("Inventory file not found. Creating a new inventory.")
        inventory = {}
    return inventory

def save_inventory_to_file(filename, inventory):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item, qty in inventory.items():
            writer.writerow([item, qty])

def add_inventory(item_name, item_qty):
    inventory = load_inventory_from_file(filename)
    if item_name in inventory:
        inventory[item_name] += item_qty
    else:
        inventory[item_name] = item_qty
    save_inventory_to_file(filename, inventory)
    return f"Inventory updated for {item_name}: {inventory[item_name]}"

def remove_inventory(item_name, item_qty):
    inventory = load_inventory_from_file(filename)
    if item_name in inventory:
        inventory[item_name] = max(0, inventory[item_name] - item_qty)
        save_inventory_to_file(filename, inventory)
        return f"Inventory updated for {item_name}: {inventory[item_name]}"
    else:
        return f"Item {item_name} not found in inventory."

def calculate_inventory(filename):
    inventory = load_inventory_from_file(filename)
    return "\n".join([f"{item}: {qty}" for item, qty in inventory.items()])

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode().lower().strip()
        if not data:
            break

        parts = data.split(',')
        action = parts[0]
        if action == "add":
            item_name = parts[1]
            item_qty = int(parts[2])
            response = add_inventory(item_name, item_qty)
        elif action == "remove":
            item_name = parts[1]
            item_qty = int(parts[2])
            response = remove_inventory(item_name, item_qty)
        elif action == "calculate":
            response = calculate_inventory(filename)
        else:
            response = "Invalid request"

        client_socket.sendall(response.encode())

    client_socket.close()

def start_server():
    HOST = '127.0.0.1'
    PORT = 1235

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address[0]}:{address[1]}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

    server_socket.close()

if __name__ == "__main__":
    start_server()
