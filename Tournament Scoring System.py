import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv

events = [] 
theme = "light"

def toggle_theme():
    global theme
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

def create_event():
    def save_event():
        event_name = entry_event_name.get().strip()
        event_type = event_type_var.get()
        
        if not event_name:
            messagebox.showwarning("Input Error", "Event name cannot be empty!")
            return
        
        events.append({"name": event_name, "type": event_type, "participants": []})
        listbox_events.insert(tk.END, f"{event_name} ({event_type})")
        
        window.destroy()
        open_event_window(event_name, event_type)

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

def open_event_window(event_name, event_type):
    def add_participant():
        name = simpledialog.askstring("Add Participant", "Enter participant name:")
        if name:
            selected_event["participants"].append({"name": name, "score": 0})
            listbox_participants.insert(tk.END, f"{name} (Score: 0)")

    def add_team():
        team_name = simpledialog.askstring("Add Team", "Enter team name:")
        if not team_name:
            return
        
        team_size = simpledialog.askinteger("Team Size", "How many members in the team?")
        if not team_size or team_size < 1:
            return
        
        team_members = []
        for i in range(team_size):
            member_name = simpledialog.askstring("Team Member", f"Enter name of member {i+1}:")
            if member_name:
                team_members.append(member_name)
        
        team_entry = {"team_name": team_name, "members": team_members, "score": 0}
        selected_event["participants"].append(team_entry)
        listbox_participants.insert(tk.END, f"{team_name} ({', '.join(team_members)}) (Score: 0)")

    def record_scores():
        selected = listbox_participants.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a participant/team to record the score.")
            return
        
        participant_info = listbox_participants.get(selected[0])
        score = simpledialog.askinteger("Record Score", f"Enter score for {participant_info}:")
        
        if score is None:
            return
        
        participant = selected_event["participants"][selected[0]]
        
        if isinstance(participant, dict) and "members" in participant:
            participant["score"] = score
            listbox_participants.delete(selected[0])
            listbox_participants.insert(selected[0], f"{participant['team_name']} ({', '.join(participant['members'])}) (Score: {score})")
        else:
            participant["score"] = score
            listbox_participants.delete(selected[0])
            listbox_participants.insert(selected[0], f"{participant['name']} (Score: {score})")

    window = tk.Toplevel(root)
    window.title(f"Manage {event_name}")
    window.geometry("400x300")
    
    ttk.Label(window, text=f"{event_name} ({event_type})").pack(pady=10)
    
    listbox_participants = tk.Listbox(window, height=8, width=50)
    listbox_participants.pack(pady=10)
    
    selected_event = next(event for event in events if event["name"] == event_name)

    for participant in selected_event["participants"]:
        if isinstance(participant, str):
            listbox_participants.insert(tk.END, f"{participant} (Score: 0)")
        elif isinstance(participant, dict):
            listbox_participants.insert(tk.END, f"{participant['team_name']} ({', '.join(participant['members'])}) (Score: 0)")
    
    if event_type == "Team":
        ttk.Button(window, text="Add Team", command=add_team).pack(pady=5)
    else:
        ttk.Button(window, text="Add Participant", command=add_participant).pack(pady=5)

    ttk.Button(window, text="Record Score", command=record_scores).pack(pady=10)
    
    def on_close():
        updated_participants = [listbox_participants.get(i) for i in range(listbox_participants.size())]
        selected_event["participants"] = updated_participants
        window.destroy()
    
    window.protocol("WM_DELETE_WINDOW", on_close)

import os
import csv
from tkinter import messagebox

def save_to_csv():
    file_path = "events.csv"
    existing_events = {}

    if os.path.exists(file_path):
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                event_name = row[0]
                existing_events[event_name] = row

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Event Name", "Event Type", "Participants", "Scores"])

        for event in events:
            event_name = event["name"]
            participants_list = []
            scores_list = []

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

            if event_name in existing_events:
                confirm = messagebox.askyesno("Duplicate Event", 
                                              f"Event '{event_name}' already exists.\n"
                                              "Do you want to overwrite it?")
                if not confirm:
                    continue

            writer.writerow([event_name, event["type"], " | ".join(participants_list), " | ".join(scores_list)])

    messagebox.showinfo("Success", "Events saved to 'events.csv'.")


def load_from_csv():
    try:
        with open("events.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header is None:
                return
            
            for row in reader:
                event_name, event_type, participants_str, scores_str = row
                participants = []
                scores = scores_str.split(" | ")
                
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

listbox_events = tk.Listbox(root, height=10, width=50)
listbox_events.pack(pady=20)

load_from_csv()

root.mainloop()