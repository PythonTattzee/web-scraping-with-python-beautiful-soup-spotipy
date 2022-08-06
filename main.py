import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
# first I create my application on developer spotify dashboard and then save my ID and Client Secret into variables
# yes, I know It is better to save it into environment variables but for now just simple constant variables.
YOUR_APP_CLIENT_ID = "7f42e97de4e1425ba993cce3885a9fbb"
YOUR_APP_CLIENT_SECRET = "15100b28891445308f593a5b41ee8ac1"


# Now with a help of beautiful soup and request I will web-scrape out top 100 songs from a specific date
# and the date will be defined by the users input.
date = input("Which year would you like to travel to? Write the date in this format YYYY-MM-DD")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
# now to work with html element we get the text of out=r request result
music_page = response.text

# after that we use Beautiful soup to scrape out (get) top 100 songs for the date of our choice.
soup = BeautifulSoup(music_page, "html.parser")
# and we will save all these songs titles into the list
songs_list = [song.getText().strip() for song in soup.find_all(name="h3", id="title-of-a-story")]
print(songs_list)

# now we will connect to the Spotify server with a help of spotipy
# also, for this step we will need to create redirect url inside of the spotify application we created earlier
# to use it as one of the parameters
# remember, one of the parameters is cache_path  where we put temporary file with our auth token
# (for connection to the server we use "playlist-modify-private" scope parameter
# when we first run the code it will open the redirect url which we created earlier where we will need to copy the link
# of the opened page and paste it into the prompt line in our pycharm console. The we will need to close our programm and reopen it
# after that we will see that there will appear the temporary file with our token inside
# In my case it was '.cache' file
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=YOUR_APP_CLIENT_ID,
                                               client_secret=YOUR_APP_CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               cache_path=".cache"))
# after connection we get out the user ID and username and save them into variables that we will need later
curr_user_id = sp.current_user()["id"]
curr_username = sp.current_user()["display_name"]
# print(curr_user_id["id"])

# next step we will need to extract the year out of the date that the user input previously
year = date.split("-")[0]
# now we will search each song through the loop
# and then for each song we will create Spotify URI to use them in order to add the songs into playlist
# (Spotify URI  - The resource identifier that you can enter, for example,
# in the Spotify Desktop client’s search box to locate an artist, album, or track)
songs_uris = []
for song in songs_list:
    result = sp.search(q=f"track: {song}, year: {year}", type="track")
    #to avoid any errors we wwilluse try except, so that if there is no such song it will pass it and continue searching
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} isn't found. Continue")
# finally, we will create the playlist using suer id and date
playlist = sp.user_playlist_create(user=curr_user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
# lastly, we will add songs into our playlist using playlist id and songs_uris list
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)
