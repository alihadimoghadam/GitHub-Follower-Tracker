import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_user_followers(username):
    url = f"https://api.github.com/users/{username}/followers"
    response = requests.get(url)
    if response.status_code == 200:
        followers = [follower["login"] for follower in response.json()]
        return followers
    else:
        messagebox.showerror("Error", f"Failed to retrieve followers for {username}.")
        return []

def get_user_following(username):
    url = f"https://api.github.com/users/{username}/following"
    response = requests.get(url)
    if response.status_code == 200:
        following = [user["login"] for user in response.json()]
        return following
    else:
        messagebox.showerror("Error", f"Failed to retrieve following for {username}.")
        return []

def find_users_not_following_back():
    username = entry.get()
    
    if not username:
        messagebox.showwarning("Warning", "Please enter your GitHub username.")
        return
    
    followers = get_user_followers(username)
    following = get_user_following(username)
    
    not_following_back = [user for user in following if user not in followers]
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Users not following you back ({username}):\n")
    for user in not_following_back:
        result_text.insert(tk.END, f"{user}\n")

# Create the main window
window = tk.Tk()
window.title("GitHub Follower Analyzer")
window.geometry("400x300")

# Create a label and an entry field for the username
label = ttk.Label(window, text="Enter your GitHub username:")
label.pack(pady=10)

entry = ttk.Entry(window, width=30)
entry.pack()

# Create a button to initiate the search
button = ttk.Button(window, text="Find Users", command=find_users_not_following_back)
button.pack(pady=10)

# Create a text box to display the result
result_text = tk.Text(window, height=8, width=40)
result_text.pack()

# Configure the text box with a scroll bar
scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.configure(yscrollcommand=scrollbar.set)

# Start the UI main loop
window.mainloop()
