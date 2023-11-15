import pickle
import pandas as pd
from tqdm import tqdm
import lyricsgenius
import time

"""
This script uses the training data availiable from the million songs dataset Challenge on kaggle (https://www.kaggle.com/c/msdchallenge). 
The music.csv dataset from github user Vatshayan (https://github.com/Vatshayan/Music-Songs-Genre-Dataset/tree/master) and the genius API to 
create a set of data consisting of the listening sessions of users along with the songs, song_lyrics and artists thaat they listened to. 
These datasources were used because the echo nest website is not functioning at the time of this project. 

The data set was created by:

1. Getting a list of all the song_id's in the "kaggle_visible_evaluation_triplets.txt" file.

2. Creating a dictionary of the song_id's listened to by each user from the "kaggle_visible_evaluation_triplets.txt" file.
The keys for this dictionary are the user_id's and the values are the song_id's that the user has listened to. 

3. Creating dictionaries to map the song_id's to the song's name, the artist name and artist id using the music.csv file. 

4. The file usable_user_history.txt was created by reducing the "kaggle_visible_evaluation_triplets.txt" file to only include the song_id's that
are in the music.csv file. each row in the usable_user_history.txt file is in the format: user_id, song_id, (artist_name, song_name).

5. This was then used to create a dictionary containing lyrics for each song_id using the genius API to get the lyrics.

6. The final dataset is a text file and dictionary containing the user_id, song_id, song_name, artist_name, artist_id for each song_id and a 
dictionary that can be used to get the lyrics to each song_id. Note this file only contains song_id's that we also have lyrics for.
"""


# # Step 1: load the triplets and compute song counts
with open("kaggle_visible_evaluation_triplets.txt", "r") as f:
    song_to_count = dict()
    for line in f:
        _, song, _ = line.strip().split("\t")
        if song in song_to_count:
            song_to_count[song] += 1
        else:
            song_to_count[song] = 1
            pass
        pass
    pass

# # Step 3: load the user histories
with open("kaggle_visible_evaluation_triplets.txt", "r") as f:
    user_to_songs = dict()
    for line in f:
        user, song, _ = line.strip().split("\t")
        if user in user_to_songs:
            user_to_songs[user].add(song)
        else:
            user_to_songs[user] = set([song])
            pass
        pass
    pass

#can we get actual song names
songs = pd.read_csv("music.csv")
song_id_to_name = {}
song_id_to_artist_name = {}
song_id_to_artist_id = {}
song_id_to_lyrics = {}

# song information based on song_id in msd dataset
for index, row in songs.iterrows():
    try:
        song_id_to_name[row["song.id"]] = str.lower(row["title"])
    except:
        song_id_to_name[row["song.id"]] = row["title"]

    song_id_to_artist_name[row["song.id"]] = str.lower(row["artist.name"])
    song_id_to_artist_id[row["song.id"]] = row["artist.id"]

# # Step 4: create a new file with only the usable user histories
with open("usable_user_history.txt", "w") as f:
    with open("kaggle_visible_evaluation_triplets.txt", "r") as g:
        for line in g:
            user, song, _ = line.strip().split("\t")
            if song in song_id_to_name.keys():
                f.write(
                    user
                    + ","
                    + song
                    + ","
                    + song_id_to_artist_name[song]
                    + ","
                    + song_id_to_name[song]
                    + "\n"
                )
                pass
            pass
        pass
    pass

# # Step 5: create a dictionary of lyrics for each song_id
genius = lyricsgenius.Genius(
    "g4zT_dicPfN839Lvvbg8D3AxQBH4-0zVa6XS63btWRX74zTvu7KLh8ZoNASBL6pa",
    skip_non_songs=True,
)
song_id_to_lyrics = {}
failed_ids = []
# Open the input file for reading
with open('usable_user_histories.txt', 'r') as input_file:
    # Open the output file for writing
    with open('msd_users.txt', 'w') as output_file:
        # Loop through each line in the input file
        for line in tqdm(input_file):
            # Split the line into song ID and lyrics
            user_id, song_id, artist, song= line.strip().split(',')
            artist = str.lower(artist[3:-1])
            backup_song =  str.lower(song[2:-2])
            song = str.lower(song[2:-2])
            print(song, artist)
            if song in song_id_to_lyrics.keys() or failed_ids:
                continue
            # Get the lyrics for the song
            try:
                song = genius.search_song(song, artist)
                lyrics = song.lyrics
            except:
                print("failed for", backup_song, artist)
                backup_song = str.split(backup_song, '(')
                if len(backup_song) > 1:
                    for i in range(len(backup_song)):
                        song = genius.search_song(backup_song[i], artist)
                        time.sleep(2)
                        if lyrics is not None:
                            break
            if lyrics is not None:
                song_id_to_lyrics[song_id] = lyrics
            else:
                failed_ids.append(song_id)

# Save the list to a pickle file
with open("failed_ids.pkl", "wb") as f:
    pickle.dump(failed_ids, f)

# Save the dictionary to a pickle file
with open("song_id_to_name.pkl", "wb") as f:
    pickle.dump(song_id_to_name, f)

with open("song_id_to_artist_name.pkl", "wb") as f:
    pickle.dump(song_id_to_artist_name, f)

with open("song_id_to_lyrics.pkl", "wb") as f:
    pickle.dump(song_id_to_lyrics, f)


#OPEN THE RESULTS LATER 
# with open("failed_ids.pkl", 'rb') as f:
#     failed_ids = pickle.load(f)

# # Load the dictionary from a pickle file
# with open('song_id_to_name.pkl', 'rb') as f:
#     song_id_to_name = pickle.load(f)

# with open('song_id_to_artist_name.pkl', 'rb') as f:
#     song_id_to_artist_name = pickle.load(f)

# with open('song_id_to_lyrics.pkl', 'rb') as f:
#     song_id_to_lyrics = pickle.load(f)


song_id_to_name= {}
# Load the dictionary from a pickle file
with open('song_id_to_name.pkl', 'rb') as f:
    song_id_to_name = pickle.load(f)
song_id_to_artist_name= {}
with open('song_id_to_artist_name.pkl', 'rb') as f:
    song_id_to_artist_name = pickle.load(f)
song_id_to_lyrics = {}
with open('song_id_to_lyrics.pkl', 'rb') as f:
    song_id_to_lyrics = pickle.load(f)
count = 0 
#making final user history file
with open("user_data.txt", "w") as user_data:
    with open("usable_user_histories.txt", "r") as f:
        for line in f:
            user_id, song_id, artist, song= line.strip().split(',')
            #no need for artist and song reformatting with updates above 
            artist = str.lower(artist[3:-1])
            song = str.lower(song[2:-2])
            print(artist, song, song_id)
            if song_id in song_id_to_lyrics.keys():
                print(count)
                count+=1
                user_data.write(
                    user_id
                    + ", "
                    + song_id
                    + ", "
                    + song
                    + ", "
                    + artist
                    + "\n"
                )







