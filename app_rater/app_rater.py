import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from google_play_scraper import app, reviews, search

# Fetch app data from the Google Play Store using the app ID
def fetch_app_data(app_id):
    try:
        return app(app_id)  # Returns app data as a dictionary
    except Exception as e:
        messagebox.showerror("Error", str(e))  # Show error message if fetching fails
        return None

# Fetch app reviews from the Google Play Store using the app ID
def fetch_app_reviews(app_id):
    try:
        result, _ = reviews(
            app_id, 
            lang="en", 
            country="ng", 
            count=3
            )  # Fetches the latest 3 reviews
        return result
    except Exception as e:
        messagebox.showerror("Error", str(e))  # Show error message if fetching fails
        return None

# Update the GUI with the fetched app data and reviews
def update_gui_with_app_data(app_data, app_info_text, app_reviews_text):
    app_info_text.delete("1.0", tk.END)  # Clear previous app info
    app_info_text.insert(tk.END, f"Title: {app_data['title']}\n")  # Display app title
    app_info_text.insert(tk.END, f"Description: {app_data['description']}\n")  # Display app description
    score = app_data['score']
    stars = "⭐" * int(score)  # Create star rating based on score
    app_info_text.insert(tk.END, f"Rating: {score} ({stars})\n")  # Display app rating
    app_info_text.insert(tk.END, f"Installs: {app_data['installs']}\n")  # Display install count
    if 'size' in app_data:
        app_info_text.insert(tk.END, f"Size: {app_data['size']}\n")  # Display app size if available

    app_reviews_text.delete("1.0", tk.END)  # Clear previous reviews
    reviews_data = fetch_app_reviews(app_data['appId'])  # Fetch reviews for the app
    if reviews_data:
        for review in reviews_data:
            app_reviews_text.insert(tk.END, f"Author: {review['userName']}\n")  # Display review author
            app_reviews_text.insert(tk.END, f"Rating: {review['score']}\n")  # Display review rating
            app_reviews_text.insert(tk.END, f"Comment: {review['content']}\n\n")  # Display review comment

# Fetch and display app data based on the app ID entered by the user
def fetch_and_display_app_data(app_id_entry, app_info_text, app_reviews_text):
    app_id = app_id_entry.get()  # Get app ID from entry field
    if not app_id:
        messagebox.showwarning("Input Error", "Please enter an App ID")  # Warn if no ID is entered
        return
    app_data = fetch_app_data(app_id)  # Fetch app data
    if app_data:
        update_gui_with_app_data(app_data, app_info_text, app_reviews_text)  # Update GUI with app data

# Search for an app by name and display its data
def search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text):
    app_name = app_name_entry.get().strip()  # Get app name from entry field
    if not app_name:
        messagebox.showwarning("Input Error", "Please enter an App Name")  # Warn if no name is entered
        return
    search_results = search(app_name)  # Search for the app
    if not search_results:
        messagebox.showinfo("No Results", "No apps found with that name")  # Inform if no results found
        return
    
    app_id = search_results[0]['appId']  # Get the app ID from the first search result
    app_data = fetch_app_data(app_id)  # Fetch app data
    if app_data:
        update_gui_with_app_data(app_data, app_info_text, app_reviews_text)  # Update GUI with app data

# Main function to set up the GUI
def main():
    root = tk.Tk()  # Create the main window
    root.title("App Rater")  # Set the window title

    frame = ttk.Frame(root, padding="20")  # Create a frame for layout
    frame.pack(padx=10, pady=10)  # Add padding around the frame

    app_id_label = ttk.Label(frame, text="App Name:")  # Label for app name entry
    app_id_label.grid(row=0, column=0, padx=5, pady=5)  # Position the label
    app_id_entry = ttk.Entry(frame)  # Entry field for app name
    app_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')  # Position the entry field

    fetch_button = ttk.Button(frame, text='Fetch App', command=lambda: search_and_display_app_data(app_id_entry, app_info_text, app_reviews_text))  # Button to fetch app data
    fetch_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    app_info_label = ttk.Label(frame, text="App Information: ")  # Label for app information section
    app_info_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)  # Position the label

    app_info_text = tk.Text(frame, height=10, width=50)  # Text area for app information
    app_info_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)  # Position the text area

    app_reviews_label = ttk.Label(frame, text="App Reviews: ")  # Label for app reviews section
    app_reviews_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)  # Position the label

    app_reviews_text = tk.Text(frame, height=10, width=50)  # Text area for app reviews
    app_reviews_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)  # Position the text area

    root.mainloop()  # Start the GUI event loop

if __name__ == "__main__":
    main()  # Run the main function