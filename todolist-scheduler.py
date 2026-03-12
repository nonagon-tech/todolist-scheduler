import json
from datetime import datetime
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# --- Data Structure ---
class ToDoData:
    def __init__(self, description, urgency, deadline):
        self.description = description
        self.urgency = urgency
        self.created_at = datetime.now()
        self.deadline = deadline

    def show_info(self):
        print(f"Task          : {self.description}")
        print(f"Urgency       : {self.urgency}")
        print(f"Created at    : {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Deadline      : {self.deadline.strftime('%Y-%m-%d %H:%M')}")

    def is_overdue(self):
        return datetime.now() > self.deadline

# --- Storage ---
class ListStorage():
    def __init__(self):
        self.tasks = []

# --- Task Operations ---
def add_task(to_the_storage):
    desc = input("Enter what task will you do: ").strip()
    if not desc: 
        print("Task description cannot be empty. Please try again.")
        return
    
    valid_urgencies = ["optional", "nice to have", "must do", "urgent"]
    while True:
        print("Enter how urgent is your task (1 = optional, 2 = nice to have, 3 = must do, 4 = urgent): ")
        for i, u in enumerate(valid_urgencies, start=1):
            print(f" {i}. {u}")
        urg_input = input("> ").strip()
        if urg_input in ["1", "2", "3", "4"]:
            urg = valid_urgencies[int(urg_input) - 1]
            break
        print("Invalid urgency level. Please enter a number between 1 and 4.")

    while True:
        deadline_input = input("Enter when is the deadline of your task (YYYY-MM-DD HH:MM): ").strip()
        try:
            the_deadline = datetime.strptime(deadline_input, "%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("Invalid date format. Please try again. Example: 2024-12-31 23:59")
    task_info = ToDoData(desc, urg, the_deadline)
    to_the_storage.tasks.append(task_info)

def load_tasks(storage):
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)

            for t in data:
                try:
                    deadline = datetime.strptime(t['deadline'], "%Y-%m-%d %H:%M:%S")
                    task = ToDoData(t['description'], t['urgency'], deadline)
                    task.created_at = datetime.strptime(t['created_at'], "%Y-%m-%d %H:%M:%S.%f")  # ← tambahkan ini
                    storage.tasks.append(task)
                except (KeyError, ValueError) as e:
                        print(f"Error loading task: {e}. Skipping this task.")

    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Error: tasks.json is corrupted. Starting with an empty task list.")
    
def save_tasks(storage):
    try:
        with open("tasks.json", "w") as f:
            json.dump([{
                'description': task.description,
                'urgency': task.urgency,
                'created_at': str(task.created_at),  
                'deadline': str(task.deadline)
            } for task in storage.tasks], f)
    except OSError as e:
        print(f"Error saving tasks: {e}")

def show_tasks(storage):
    if not storage.tasks:
        print("You don't have any tasks yet.\n")
        return
    
    print("Your tasks:")
    for i, task in enumerate(storage.tasks, start=1):
        print(f"\nTask #{i}")
        task.show_info()
        if task.is_overdue():
            print("⚠ Overdue!")

def delete_task(storage):
    if not storage.tasks:
        print("You don't have any tasks to delete.\n")
        return
    
    show_tasks(storage)
    while True:
        try:
            choice = int(input("\nEnter the task number to delete (or 0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(storage.tasks):
                del storage.tasks[choice - 1]
                print("Task deleted successfully.")
                return
            else:
                print(f"Please enter a number between 1 and {len(storage.tasks)}, or 0 to cancel.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")

def change_task(storage):
    if not storage.tasks:
        print("You don't have any tasks to change.\n")
        return
    
    show_tasks(storage)
    while True:
        try:
            choice = int(input("\nEnter the task number to change (or 0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(storage.tasks):
                task = storage.tasks[choice - 1]
                print("\nCurrent task details:")
                task.show_info()
                print("\nEnter new details for the task (leave blank to keep current value):")
                
                new_desc = input("New description: ").strip()
                if new_desc:
                    task.description = new_desc
                
                valid_urgencies = ["optional", "nice to have", "must do", "urgent"]
                while True:
                    print("New urgency level (1 = optional, 2 = nice to have, 3 = must do, 4 = urgent, or leave blank to keep current): ")
                    for i, u in enumerate(valid_urgencies, start=1):
                        print(f" {i}. {u}")
                    urg_input = input("> ").strip()
                    if not urg_input:
                        break
                    if urg_input in ["1", "2", "3", "4"]:
                        task.urgency = valid_urgencies[int(urg_input) - 1]
                        break
                    print("Invalid urgency level. Please enter a number between 1 and 4, or leave blank.")
                
                while True:
                    deadline_input = input("New deadline (YYYY-MM-DD HH:MM, or leave blank to keep current): ").strip()
                    if not deadline_input:
                        break
                    try:
                        task.deadline = datetime.strptime(deadline_input, "%Y-%m-%d %H:%M")
                        break
                    except ValueError:
                        print("Invalid date format. Please try again. Example: 2024-12-31 23:59")
                
                print("Task updated successfully.")
                return
            else:
                print(f"Please enter a number between 1 and {len(storage.tasks)}, or 0 to cancel.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")

# --- Utility Functions ---
def refresh(storage):
    clear()
    show_tasks(storage)
    print("-----------------------------------------------\n")

# --- Main Program ---
              
clear()
real_list_storage = ListStorage()

print("Welcome.")
print("This is simple To-Do List Scheduler from Python.")
print("-----------------------------------------------\n")
load_tasks(real_list_storage)
show_tasks(real_list_storage)
print("-----------------------------------------------\n")
while True:
    print(" • Enter (N/n) to add new tasks.")
    print(" • Enter (C/c) to change existing tasks.")
    print(" • Enter (D/d) to delete existing tasks.")
    print(" • Enter (Q/q) to exit.")
    choice = input("> ").lower()

    if choice == "n":
        add_task(real_list_storage)
        refresh(real_list_storage)
    elif choice == "c":
        change_task(real_list_storage)
        refresh(real_list_storage)
    elif choice == "d":
        delete_task(real_list_storage)
        refresh(real_list_storage)
    elif choice == "q":
        save_tasks(real_list_storage)
        break
        

        
    





