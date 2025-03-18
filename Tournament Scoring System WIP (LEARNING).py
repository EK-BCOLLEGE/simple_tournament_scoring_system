import tkinter as tk

events = []

def create_event():
    events_name = input("Enter event name: ")
    events.append(events_name)
    print(f"Event '{events_name}' has been added")

root = tk.Tk()
root.title("Tournament System")

create_event_button = tk.Button(root, text="Create a event", command=create_event)
create_event_button.pack()

root.mainloop()