import tkinter as tk
from tkinter import ttk
import threading
import time
import requests

def check_status():
    global running
    running = True
    notification_var.set("Checking statuses...")

    for idx, url in enumerate(urls):
        if not running:
            break

        try:
            start_time = time.time()
            response = requests.get(url)
            response_time = time.time() - start_time

            if response.status_code == 200:
                status_var[idx].set("✔")  # Checkmark for active
            else:
                status_var[idx].set("✘")  # X for not active

            time_var[idx].set(f"{response_time:.4f} seconds")

        except requests.RequestException as e:
            status_var[idx].set("✘")  # X for not active
            time_var[idx].set("N/A")
            error_var.set(f"Error for {url}: {e}")
            break

    notification_var.set("Status check completed.")
    root.after(100, update_treeview)  # Schedules the update_treeview function after a short delay

def update_treeview():
    for idx, url in enumerate(urls):
        item_id = f"row{idx}"
        if not tree.exists(item_id):
            create_rows()
        tree.item(item_id, values=(url, status_var[idx].get(), time_var[idx].get()))

def start_status_check():
    create_rows()
    global check_thread
    check_thread = threading.Thread(target=check_status)
    check_thread.start()

def end_status_check():
    global running
    running = False
    if check_thread.is_alive():
        check_thread.join()

def schedule_status_check():
    current_time = time.localtime(time.time())
    hours = current_time.tm_hour
    minutes = current_time.tm_min

    # Checks if the current time matches the scheduled times
    if (hours == 4 and minutes == 0) or (hours == 6 and minutes == 0) or (hours == 7 and minutes == 0):
        check_status()
    
    # Scheduling the function to run again after a minute
    root.after(60000, schedule_status_check)

def create_rows():
    # rows for each URL in the treeview
    for idx, url in enumerate(urls):
        tree.insert("", "end", values=(url, "", ""), tags=(f"row{idx}",))

# list of URLs (can add more.) NB- gracecourttake-away is a demo non active website to confirm the not active output works.
urls = [
    'https://www.namibiansun.com/',
    'https://www.republikein.com.na/',
    'http://www.gracecourttake-away.com.au/',
    'https://www.we.com.na/'
]

# Initializes GUI
root = tk.Tk()
root.title("URL Status Checker")

# Variables
notification_var = tk.StringVar()
notification_var.set("")

status_var = [tk.StringVar() for _ in urls]
time_var = [tk.StringVar() for _ in urls]

# UI Elements
start_button = tk.Button(root, text="Start Status Check", command=start_status_check)
start_button.pack(pady=10)

end_button = tk.Button(root, text="End Status Check", command=end_status_check)
end_button.pack(pady=10)

notification_label = tk.Label(root, textvariable=notification_var, fg="blue")
notification_label.pack(pady=10)

# treeview for the grid
columns = ("URL", "Status", "Response Time")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("URL", text="URL")
tree.heading("Status", text="Status")
tree.heading("Response Time", text="Response Time")

# column sizes
tree.column("URL", anchor="center", width=500)
tree.column("Status", anchor="center", width=100)
tree.column("Response Time",anchor="center", width=200)



tree.pack(pady=10)

# Runs the create_rows function in the main thread to create rows initially
create_rows()

# Runs the GUI
root.mainloop()
# IMPORTANT NOTE: for now the the GUI does not show the website statuses but I will work on that. Critism will be much appreciated. :) 