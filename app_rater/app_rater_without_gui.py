from google_play_scraper import app, reviews, search

def fetch_app_data(app_id):
    try:
        return app(app_id)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def fetch_app_reviews(app_id):
    try:
        result, _ = reviews(
            app_id,
            lang="en", 
            country="ng", 
            count=3
        )
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def display_app_data(app_data):
    print(f"Title: {app_data['title']}")
    print(f"Description: {app_data['description']}")
    score = app_data['score']
    stars = "⭐" * int(score)
    print(f"Rating: {score} ({stars})")
    print(f"Installs: {app_data['installs']}")
    if 'size' in app_data:
        print(f"Size: {app_data['size']}")

def display_app_reviews(reviews_data):
    if reviews_data:
        for review in reviews_data:
            print(f"Author: {review['userName']}")
            print(f"Rating: {review['score']}")
            print(f"Comment: {review['content']}\n")

def fetch_and_display_app_data(app_id):
    app_data = fetch_app_data(app_id)
    if app_data:
        display_app_data(app_data)
        reviews_data = fetch_app_reviews(app_data['appId'])
        if reviews_data:
            display_app_reviews(reviews_data)

def search_and_display_app_data(app_name):
    search_results = search(app_name)
    if not search_results:
        print("No apps found with that name")
        return
    
    app_id = search_results[0]['appId']
    fetch_and_display_app_data(app_id)

def main():
    while True:
        option = input("Enter 1 to search by app name or 2 to enter app ID (or 'q' to quit): ").strip()
        if option == 'q':
            break
        elif option == '1':
            app_name = input("Enter the App Name: ").strip()
            search_and_display_app_data(app_name)
        elif option == '2':
            app_id = input("Enter the App ID: ").strip()
            fetch_and_display_app_data(app_id)
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
