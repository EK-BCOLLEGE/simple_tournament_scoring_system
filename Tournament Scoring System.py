import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv

events = [] 
theme = "light"

def toggle_theme(): # This will allow the user to switch between light and dark theme
    global theme # Store their theme choice
    if theme == "light":
        root.configure(bg="#1E1E2E") 
        style.configure("TButton", background="#3B82F6", foreground="#000000", font=("Segoe UI", 12), padding=8, relief="flat")
        style.map("TButton", background=[("active", "#2563EB")])
        style.configure("TLabel", background="#1E1E2E", foreground="#000000", font=("Segoe UI", 12))
        listbox_events.configure(bg="#2A2A3B", fg="white", selectbackground="#3B82F6", selectforeground="white")
        theme = "dark"
    else:
        root.configure(bg="#F5F5F5")
        style.configure("TButton", background="#2563EB", foreground="#000000", font=("Segoe UI", 12), padding=8, relief="flat")
        style.map("TButton", background=[("active", "#1D4ED8")])
        style.configure("TLabel", background="#F5F5F5", foreground="#000000", font=("Segoe UI", 12))
        listbox_events.configure(bg="white", fg="black", selectbackground="#2563EB", selectforeground="white")
        theme = "light"

def create_event(): # Function to create a event
    def save_event(): # Save the event and update the listbox
        event_name = entry_event_name.get().strip()
        event_type = event_type_var.get()
        
        if not event_name:
            messagebox.showwarning("Input Error", "Event name cannot be empty!")
            return
        
        events.append({"name": event_name, "type": event_type, "participants": []})
        listbox_events.insert(tk.END, f"{event_name} ({event_type})")
        
        window.destroy()
        open_event_window(event_name, event_type)

    # UI elements for creating a event
    window = tk.Toplevel(root)
    window.title("Create Event")
    window.geometry("300x200")
    
    ttk.Label(window, text="Enter Event Name:").pack(pady=5)
    entry_event_name = ttk.Entry(window)
    entry_event_name.pack(pady=5)
    
    event_type_var = tk.StringVar(value="Team")
    ttk.Label(window, text="Select Event Type:").pack(pady=5)
    ttk.Radiobutton(window, text="Team", variable=event_type_var, value="Team").pack()
    ttk.Radiobutton(window, text="Individual", variable=event_type_var, value="Individual").pack()
    
    ttk.Button(window, text="Create Event", command=save_event).pack(pady=10)

def open_event_window(event_name, event_type): # Window to add participants/team after creating an event
    def add_participant(): # Add participants for the event
        name = simpledialog.askstring("Add Participant", "Enter participant name:")
        if name:
            selected_event["participants"].append({"name": name, "score": 0})
            listbox_participants.insert(tk.END, f"{name} (Score: 0)")

    def add_team(): # Add teams for the event
        team_name = simpledialog.askstring("Add Team", "Enter team name:")
        if not team_name:
            return
        
        team_size = simpledialog.askinteger("Team Size", "How many members in the team?")
        if not team_size or team_size < 1:
            return
        
        team_members = []
        for i in range(team_size): # Loops for the size of team and asks them for the team member names.
            member_name = simpledialog.askstring("Team Member", f"Enter name of member {i+1}:")
            if member_name:
                team_members.append(member_name)
        
        team_entry = {"team_name": team_name, "members": team_members, "score": 0}
        selected_event["participants"].append(team_entry)
        listbox_participants.insert(tk.END, f"{team_name} ({', '.join(team_members)}) (Score: 0)")

    def record_scores(): # Function to record team/participant scores.
        selected = listbox_participants.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a participant/team to record the score.")
            return

        score = simpledialog.askinteger("Record Score", "Enter the new score:")

        index = selected[0]
        participant = selected_event["participants"][index]

        if score is None:
            return  

        # Update the listbox with the new recorded scores
        if isinstance(participant, dict) and "members" in participant:
            participant["score"] = score  
            listbox_participants.delete(index)
            listbox_participants.insert(index, f"{participant['team_name']} ({', '.join(participant['members'])}) - Score: {score}")
        else:   
            participant["score"] = score  
            listbox_participants.delete(index)
            listbox_participants.insert(index, f"{participant['name']} - Score: {score}")

        messagebox.showinfo("Success", "Score updated successfully.")

    # Event UI elements
    window = tk.Toplevel(root)
    window.title(f"Manage {event_name}")
    window.geometry("400x300")
    
    ttk.Label(window, text=f"{event_name} ({event_type})").pack(pady=10)
    
    # Participants Listbox UI element 
    listbox_participants = tk.Listbox(window, height=8, width=50)
    listbox_participants.pack(pady=10)
    
    selected_event = next(event for event in events if event["name"] == event_name)

    # Loop for each participant in selected event it will update the listbox
    for participant in selected_event["participants"]:
        if isinstance(participant, str):
            listbox_participants.insert(tk.END, f"{participant} (Score: 0)")
        elif isinstance(participant, dict):
            listbox_participants.insert(tk.END, f"{participant['team_name']} ({', '.join(participant['members'])}) (Score: 0)")
    
    # Add's the relevant button to add a team/participant based on the Event Type
    if event_type == "Team":
        ttk.Button(window, text="Add Team", command=add_team).pack(pady=5)
    else:
        ttk.Button(window, text="Add Participant", command=add_participant).pack(pady=5)

    #
    ttk.Button(window, text="Record Score", command=record_scores).pack(pady=10)
    
    def on_close(): # Handle the closing of the event window
        updated_participants = [listbox_participants.get(i) for i in range(listbox_participants.size())]
        selected_event["participants"] = updated_participants
        window.destroy()
    
    window.protocol("WM_DELETE_WINDOW", on_close)

import os
import csv
from tkinter import messagebox

def save_to_csv(): # Save participant, teams, and event data to a .CSV file. 
    file_path = "events.csv"
    existing_events = {}

    # Check if the file already exists, if it does then it will read the .CSV file contents.
    if os.path.exists(file_path):
        with open(file_path, "r", newline="") as file: # Open the file in read mode
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                event_name = row[0]
                existing_events[event_name] = row

    # Open the CSV file in write mode, it will overwrite the file contents.
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Event Name", "Event Type", "Participants", "Scores"])

        # Loop through the list of events
        for event in events:
            event_name = event["name"]
            participants_list = []
            scores_list = []

            # Loop through the participants in the event
            for p in event["participants"]:
                if isinstance(p, dict):
                    if "name" in p:
                        participants_list.append(p["name"])
                        scores_list.append(str(p["score"]))
                    elif "team_name" in p:
                        team_info = f"{p['team_name']} ({', '.join(p['members'])})"
                        participants_list.append(team_info)
                        scores_list.append(str(p["score"]))
                else:
                    participants_list.append(str(p))
                    scores_list.append("N/A")

            # Check if event already exists, if so display a warning message that it will overwrite.
            if event_name in existing_events:
                confirm = messagebox.askyesno("Duplicate Event", 
                                              f"Event '{event_name}' already exists.\n"
                                              "Do you want to overwrite it?")
                if not confirm:
                    continue

            writer.writerow([event_name, event["type"], " | ".join(participants_list), " | ".join(scores_list)])

    messagebox.showinfo("Success", "Events saved to 'events.csv'.")


# Load the event data from the .CSV file and use it to fill up the events list
def load_from_csv():
    try:
        with open("events.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header is None:
                return
            
            # Loop through each row in the CSV file
            for row in reader:
                event_name, event_type, participants_str, scores_str = row
                participants = []
                scores = scores_str.split(" | ")
                
                # Loop through the participants strings
                for p in participants_str.split(" | "):
                    if '(' in p: 
                        if ')' in p: 
                            try:
                                team_name, members_str = p.split(" (", 1)
                                members_str = members_str.rstrip(")")
                                members = members_str.split(", ")
                                participants.append({"team_name": team_name, "members": members, "score": 0})  # Temporarily set score to 0
                            except ValueError:
                                print(f"Error parsing team data: {p}")
                        else:
                            try:
                                name, score_str = p.split(" (")
                                score = int(score_str.rstrip(')').split(":")[1].strip())
                                participants.append({"name": name, "score": score})
                            except ValueError:
                                print(f"Error parsing individual data: {p}")
                    else:
                        name, score_str = p.split(" (")
                        score = int(score_str.rstrip(')').split(":")[1].strip())
                        participants.append({"name": name, "score": score})
                
                # Update the events list
                event = {"name": event_name, "type": event_type, "participants": participants}
                events.append(event)
                listbox_events.insert(tk.END, f"{event_name} ({event_type})")
    except FileNotFoundError:
        pass



def open_leaderboard_window():
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("500x400")

    listbox_leaderboard = tk.Listbox(leaderboard_window, height=10, width=50)
    listbox_leaderboard.pack(pady=20)

    events_sorted = sorted(events, key=lambda e: sum([p["score"] for p in e["participants"] if isinstance(p, dict)]), reverse=True)

    for event in events_sorted:
        listbox_leaderboard.insert(tk.END, f"{event['name']} ({event['type']})")

    def show_event_details():
        selected = listbox_leaderboard.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an event to view details.")
            return
        
        event_name = listbox_leaderboard.get(selected[0])
        event = next(event for event in events if event["name"] == event_name.split(" (")[0])

        details_window = tk.Toplevel(leaderboard_window)
        details_window.title(f"Details for {event_name}")
        details_window.geometry("400x300")
        
        listbox_details = tk.Listbox(details_window, height=8, width=50)
        listbox_details.pack(pady=10)

        for participant in event["participants"]:
            if isinstance(participant, dict) and "members" in participant:
                listbox_details.insert(tk.END, f"{participant['team_name']} ({', '.join(participant['members'])}) - Score: {participant['score']}")
            else:
                listbox_details.insert(tk.END, f"{participant['name']} - Score: {participant['score']}")

    ttk.Button(leaderboard_window, text="View Details", command=show_event_details).pack(pady=10)

def refresh_event_list():
    listbox_events.delete(0, tk.END)
    for event in events:
        listbox_events.insert(tk.END, f"{event['name']} ({event['type']})")

def search_participant():
    search_term = simpledialog.askstring("Search", "Enter team or individual name:")
    if not search_term:
        return
    
    search_term = search_term.lower()
    search_results = []
    
    for event in events:
        for participant in event["participants"]:
            if isinstance(participant, dict):
                if "members" in participant:
                    if search_term in participant["team_name"].lower() or any(search_term in m.lower() for m in participant["members"]):
                        search_results.append((event, participant))
                else:
                    if search_term in participant["name"].lower():
                        search_results.append((event, participant))
    
    if not search_results:
        messagebox.showinfo("Search Results", "No matching participants found.")
        return
    
    search_window = tk.Toplevel(root)
    search_window.title("Search Results")
    search_window.geometry("400x300")
    
    listbox_results = tk.Listbox(search_window, height=10, width=50)
    listbox_results.pack(pady=10)
    
    for event, participant in search_results:
        if "members" in participant:
            listbox_results.insert(tk.END, f"{participant['team_name']} ({', '.join(participant['members'])}) - {event['name']}")
        else:
            listbox_results.insert(tk.END, f"{participant['name']} - {event['name']}")

    def edit_selected():
        selected = listbox_results.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a participant to edit.")
            return
        
        event, participant = search_results[selected[0]]
        new_score = simpledialog.askinteger("Edit Score", f"Enter new score for {participant['name'] if 'name' in participant else participant['team_name']}")
        
        if new_score is not None:
            participant["score"] = new_score
            refresh_event_list()
            messagebox.showinfo("Success", "Score updated successfully.")
            search_window.destroy()

    ttk.Button(search_window, text="Edit Score", command=edit_selected).pack(pady=10)

root = tk.Tk()
root.title("Tournament Scoring System")
root.geometry("500x500")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12))

ttk.Button(root, text="Create Event", command=create_event).pack(pady=10)
ttk.Button(root, text="Leaderboard", command=open_leaderboard_window).pack(pady=10)
ttk.Button(root, text="Toggle Theme", command=toggle_theme).pack(pady=10)
ttk.Button(root, text="Save to CSV", command=save_to_csv).pack(pady=10)
ttk.Button(root, text="Search", command=search_participant).pack(pady=10)

listbox_events = tk.Listbox(root, height=10, width=50)
listbox_events.pack(pady=20)

load_from_csv()

root.mainloop()