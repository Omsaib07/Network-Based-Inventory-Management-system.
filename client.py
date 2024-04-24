import tkinter as tk
import socket

def send_request():
    action = action_var.get().lower().strip()
    if action in ["add", "remove", "calculate"]:
        try:
            item_name = item_name_entry.get().strip()
            item_qty = int(item_qty_entry.get().strip()) 
            HOST = '192.168.156.117'
            PORT = 40000

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                try:
                    client_socket.connect((HOST, PORT))
                    if action == "add" or action == "remove":
                        request_data = f"{action},{item_name},{item_qty}"  
                    else:
                        request_data = action
                    client_socket.sendall(request_data.encode())
                    response = client_socket.recv(1024).decode()
                
                    response_var.set("Response from server: " + response)
                except ConnectionRefusedError:
                    response_var.set("Connection refused. Make sure the server is running.")
                except ValueError:
                    response_var.set("Invalid quantity. Please enter a valid number.")
        except ValueError:
            response_var.set("Invalid quantity. Please enter a valid number.")
    else:
        response_var.set("Invalid action. Please enter 'add', 'remove', or 'calculate'.")


root = tk.Tk()
root.title("Inventory Management Client")


action_label = tk.Label(root, text="Action:")
action_label.grid(row=0, column=0, padx=5, pady=5)
action_var = tk.StringVar()
action_combobox = tk.OptionMenu(root, action_var, "Add", "Remove", "Calculate")
action_combobox.grid(row=0, column=1, padx=5, pady=5)

item_name_label = tk.Label(root, text="Item Name:")
item_name_label.grid(row=1, column=0, padx=5, pady=5)
item_name_entry = tk.Entry(root)
item_name_entry.grid(row=1, column=1, padx=5, pady=5)


item_qty_label = tk.Label(root, text="Item Quantity:")
item_qty_label.grid(row=2, column=0, padx=5, pady=5)
item_qty_entry = tk.Entry(root)
item_qty_entry.grid(row=2, column=1, padx=5, pady=5)


send_button = tk.Button(root, text="Send Request", command=send_request)
send_button.grid(row=3, columnspan=2, padx=5, pady=5)


response_var = tk.StringVar()
response_label = tk.Label(root, textvariable=response_var)
response_label.grid(row=4, columnspan=2, padx=5, pady=5)

root.mainloop()
