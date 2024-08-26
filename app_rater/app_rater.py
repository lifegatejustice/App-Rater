
import tkinter as tk
from tkinter import messagebox
from google_play_scraper import app, reviews, search
def fetch_app_data(app_id):
    try:
        return app(app_id)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def fetch_app_reviews(app_id):
    try:
        result, _ = reviews(
            app_id, 
            lang="en", 
            country="ng", 
            count=3
            ) # type: ignore
        return result
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def update_gui_with_app_data(app_data, app_info_text, app_reviews_text):
    app_info_text.delete("1.0", tk.END)
    app_info_text.insert(tk.END, f"Title: {app_data['title']}\n")
    app_info_text.insert(tk.END, f"Description: {app_data['description']}\n")
    score = app_data['score']
    stars = "⭐" * int(score)
    app_info_text.insert(tk.END, f"Rating: {score} ({stars})\n")
    
    
    app_info_text.insert(tk.END, f"Installs: {app_data['installs']}\n")
    if 'size' in app_data:
        app_info_text.insert(tk.END, f"Size: {app_data['size']}\n")

    app_reviews_text.delete("1.0", tk.END)
    reviews_data = fetch_app_reviews(app_data['appId'])
    if reviews_data:
        for review in reviews_data:
            app_reviews_text.insert(tk.END, f"Author: {review['userName']}\n")
            app_reviews_text.insert(tk.END, f"Rating: {review['score']}\n")
            app_reviews_text.insert(tk.END, f"Comment: {review['content']}\n\n")


def fetch_and_display_app_data(app_id_entry, app_info_text, app_reviews_text):
    app_id = app_id_entry.get()
    if not app_id:
        messagebox.showwarning("Input Error", "Please enter an App ID")
        return
    app_data = fetch_app_data(app_id)
    if app_data:
        update_gui_with_app_data(app_data, app_info_text, app_reviews_text)

def search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text):
    app_name = app_name_entry.get().strip()
    if not app_name:
        messagebox.showwarning("Input Error", "Please enter an App Name")
        return
    search_results = search(app_name)
    if not search_results:
        messagebox.showinfo("No Results", "No apps found with that name")
        return
    
    print("Search Results:", search_results)
    app_id = search_results[0]['appId']
    app_data = fetch_app_data(app_id)
    if app_data:
        update_gui_with_app_data(app_data, app_info_text, app_reviews_text)


def main():
    root = tk.Tk()
    root.title("App Rater")

    frame = tk.Frame(root, bg='#102C47')
    frame.pack(padx=100, pady=100)

    app_id_label = tk.Label(frame, text="App Name:")
    app_id_label.grid(row=0, column=0, padx=5, pady=5,)
    app_id_entry = tk.Entry(frame)
    app_id_entry.grid(row=0, column=1, padx=5, pady=5)

    fetch_button = tk.Button(frame, text='Fetch App', command=lambda: search_and_display_app_data(app_id_entry, app_info_text, app_reviews_text))
    fetch_button.grid(row=1,column=0, columnspan=2, padx=5, pady=5)

    app_info_label = tk.Label(frame, text="App Information: ")
    app_info_label.grid(row=2,column=0, columnspan=2, padx=155, pady=5)

    app_info_text = tk.Text(frame, height=10, width=50)
    app_info_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    app_reviews_label = tk.Label(frame, text="App Reviews: ")
    app_reviews_label.grid(row=4, column=0, columnspan=2, padx=155, pady=5)

    app_reviews_text = tk.Text(frame, height=10, width=50)
    app_reviews_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()