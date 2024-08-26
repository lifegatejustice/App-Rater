import pytest
from unittest.mock import patch
import tkinter as tk
from app_rater import  update_gui_with_app_data, fetch_and_display_app_data, search_and_display_app_data


sample_app_data = {
    'title': 'Facebook',
    'description': 'Keeping up with friends is faster and easier than ever. Share updates and photos, engage with friends and Pages, and stay connected to communities important to you.',
    'score': 4.1,
    'installs': '5,000,000,000+',
    'appId': 'com.facebook.katana'
}

sample_reviews_data = [
    {'userName': 'User1', 'score': 5, 'content': 'Great app!'},
    {'userName': 'User2', 'score': 4, 'content': 'Good app.'},
    {'userName': 'User3', 'score': 3, 'content': 'Average app.'}
]


sample_app_data_efootball = {
    'title': 'eFootball',
    'description': 'Experience the most realistic and authentic soccer game with eFootball.',
    'score': 4.3,
    'installs': '100,000,000+',
    'appId': 'jp.konami.pesam'
}

sample_reviews_data_efootball = [
    {'userName': 'UserA', 'score': 5, 'content': 'Amazing soccer game!'},
    {'userName': 'UserB', 'score': 4, 'content': 'Very good.'},
    {'userName': 'UserC', 'score': 2, 'content': 'Could be better.'}
]

def test_update_gui_with_app_data(mocker):
    root = tk.Tk()
    app_info_text = tk.Text(root)
    app_reviews_text = tk.Text(root)
    
    mocker.patch('app_rater.fetch_app_reviews', return_value=sample_reviews_data)

    update_gui_with_app_data(sample_app_data, app_info_text, app_reviews_text)

    assert "Title: Facebook" in app_info_text.get("1.0", tk.END)
    assert "Rating: 4.1 (⭐⭐⭐⭐)" in app_info_text.get("1.0", tk.END)
    assert "Great app!" in app_reviews_text.get("1.0", tk.END)

    mocker.patch('app_rater.fetch_app_reviews', return_value=sample_reviews_data_efootball)

    update_gui_with_app_data(sample_app_data_efootball, app_info_text, app_reviews_text)

    assert "Title: eFootball" in app_info_text.get("1.0", tk.END)
    assert "Rating: 4.3 (⭐⭐⭐⭐)" in app_info_text.get("1.0", tk.END)
    assert "Amazing soccer game!" in app_reviews_text.get("1.0", tk.END)
    assert "Very good." in app_reviews_text.get("1.0", tk.END)

    root.destroy()

# def test_search_and_display_app_data(mocker):
#     root = tk.Tk()
#     app_id_entry = tk.Entry(root)
#     app_name_entry = tk.Entry(root)
#     app_name_entry.insert(0, 'Facebook')
#     app_info_text = tk.Text(root)
#     app_reviews_text = tk.Text(root)
    
#     mocker.patch('google_play_scraper.search', return_value=[{'appId': 'com.facebook.katana'}])
#     mocker.patch('app_rater.fetch_app_data', return_value=sample_app_data)
#     update_gui_mock = mocker.patch('app_rater.update_gui_with_app_data')
    
#     search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text)
    
#     update_gui_mock.assert_called_once_with(sample_app_data, app_info_text, app_reviews_text)

#     assert "Title: Facebook" in app_info_text.get("1.0", tk.END)
#     assert "Description: Keeping up with friends is faster and easier than ever." in app_info_text.get("1.0", tk.END)

  
#     app_id_entry.delete(0, tk.END)
#     app_id_entry.insert(0, 'jp.konami.pesam')
#     mocker.patch('app_rater.fetch_app_data', return_value=sample_app_data_efootball)
    
#     fetch_and_display_app_data(app_id_entry, app_info_text, app_reviews_text)

#     update_gui_mock.assert_called_with(sample_app_data_efootball, app_info_text, app_reviews_text)

#     assert "Title: eFootball" in app_info_text.get("1.0", tk.END)
#     assert "Description: Experience the most realistic and authentic soccer game with eFootball." in app_info_text.get("1.0", tk.END)
#     assert "Rating: 4.3 (⭐⭐⭐⭐)" in app_info_text.get("1.0", tk.END)
#     assert "Installs: 100,000,000+" in app_info_text.get("1.0", tk.END)

#     assert "Amazing soccer game!" in app_reviews_text.get("1.0", tk.END)
#     assert "Very good." in app_reviews_text.get("1.0", tk.END)
#     root.destroy()


def test_fetch_and_display_app_data_no_app_id():
    root = tk.Tk()
    app_id_entry = tk.Entry(root)
    app_info_text = tk.Text(root)
    app_reviews_text = tk.Text(root)
    
    with patch('tkinter.messagebox.showwarning') as mock_showwarning:
        fetch_and_display_app_data(app_id_entry, app_info_text, app_reviews_text)
        mock_showwarning.assert_called_once_with("Input Error", "Please enter an App ID")
    root.destroy()
class TestSearchAndDisplayAppData:
     def test_search_and_display_app_data(self, mocker):
        from app_rater import search_and_display_app_data
    
        # Mocking the search function to return a valid app result
        mock_search = mocker.patch('app_rater.search', return_value=[{'appId': 'com.facebook.katana'}])
    
        # Mocking the fetch_app_data function to return a valid app data
        mock_fetch_app_data = mocker.patch('app_rater.fetch_app_data', return_value={
            'title': 'Facebook',
            'description': 'Keeping up with friends is faster and easier than ever.',
            'score': 4.5,
            'installs': '1,000,000+',
            'appId': 'com.facebook.katana'
        })
    
        # Mocking the update_gui_with_app_data function
        mock_update_gui_with_app_data = mocker.patch('app_rater.update_gui_with_app_data')
    
        # Creating mock tkinter Text widgets
        app_name_entry = mocker.Mock()
        app_name_entry.get.return_value = 'Facebook'
        app_info_text = mocker.Mock()
        app_reviews_text = mocker.Mock()
    
        # Calling the function under test
        search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text)
    
        # Asserting that the search function was called with the correct parameters
        mock_search.assert_called_once_with('Facebook')
    
        # Asserting that the fetch_app_data function was called with the correct app ID
        mock_fetch_app_data.assert_called_once_with('com.facebook.katana')
    
        # Asserting that the update_gui_with_app_data function was called with the correct parameters
        mock_update_gui_with_app_data.assert_called_once_with(mock_fetch_app_data.return_value, app_info_text, app_reviews_text)




        mock_search = mocker.patch('app_rater.search', return_value=[{'appId': 'jp.konami.pesam'}])
    
        # Mocking the fetch_app_data function to return a valid app data
        mock_fetch_app_data = mocker.patch('app_rater.fetch_app_data', return_value={
            'title': 'efootball',
            'description': 'Keeping up with friends is faster and easier than ever.',
            'score': 4.5,
            'installs': '1,000,000+',
            'appId': 'jp.konami.pesam'
        })
    
        # Mocking the update_gui_with_app_data function
        mock_update_gui_with_app_data = mocker.patch('app_rater.update_gui_with_app_data')

    
        # Creating mock tkinter Text widgets
        app_name_entry = mocker.Mock()
        app_name_entry.get.return_value = 'efootball'
        app_info_text = mocker.Mock()
        app_reviews_text = mocker.Mock()
    
        # Calling the function under test
        search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text)
    
        # Asserting that the search function was called with the correct parameters
        mock_search.assert_called_once_with('efootball')
    
        # Asserting that the fetch_app_data function was called with the correct app ID
        mock_fetch_app_data.assert_called_once_with('jp.konami.pesam')
    
        # Asserting that the update_gui_with_app_data function was called with the correct parameters
        mock_update_gui_with_app_data.assert_called_once_with(mock_fetch_app_data.return_value, app_info_text, app_reviews_text)
    

    # app_name_entry.delete(0, tk.END)
    # app_name_entry.insert(0, 'eFootball')
    # mocker.patch('google_play_scraper.search', return_value=[{'appId': 'jp.konami.pesam'}])
    # mocker.patch('app_rater.fetch_app_data', return_value=sample_app_data_efootball)
    
    # search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text)
    
    # update_gui_mock.assert_called_with(sample_app_data_efootball, app_info_text, app_reviews_text)
    
    # assert "Title: eFootball" in app_info_text.get("1.0", tk.END)
    # assert "Description: Experience the most realistic and authentic soccer game with eFootball." in app_info_text.get("1.0", tk.END)

    # root.destroy()


def test_search_and_display_app_data_no_app_name():
    root = tk.Tk()
    app_name_entry = tk.Entry(root)
    app_info_text = tk.Text(root)
    app_reviews_text = tk.Text(root)
    
    with patch('tkinter.messagebox.showwarning') as mock_showwarning:
        search_and_display_app_data(app_name_entry, app_info_text, app_reviews_text)
        mock_showwarning.assert_called_once_with("Input Error", "Please enter an App Name")

    assert app_info_text.get("1.0", tk.END) == "\n"
    assert app_reviews_text.get("1.0", tk.END) == "\n"
    root.destroy()
pytest.main(["-v", "--tb=line", "-rN", __file__])

