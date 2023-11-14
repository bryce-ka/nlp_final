import pickle
import pandas as pd
from tqdm import tqdm
import lyricsgenius
import requests
import lyricsgenius

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


# # Step 4: load the user ordering
with open("kaggle_users.txt", "r") as f:
    canonical_users = map(lambda line: line.strip(), f.readlines())
    pass


# # Step 5: load the song ordering

with open("kaggle_songs.txt", "r") as f:
    song_to_index = dict(map(lambda line: line.strip().split(" "), f.readlines()))
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

spotify_ds = pd.read_csv("spotify_millsongdata.csv")

# now trying to make a dataset of msd songs that get the lyric info from the spotify dataset
spotify_songs_dict = {}
song_and_artist_index = {}


genius = lyricsgenius.Genius(
    "g4zT_dicPfN839Lvvbg8D3AxQBH4-0zVa6XS63btWRX74zTvu7KLh8ZoNASBL6pa",
    skip_non_songs=True,
)
failed_songs = []

for song in tqdm(song_to_count.keys()):  # for all song id's in msd
    try:
        song_name = song_id_to_name[song]
        song_artist = song_id_to_artist_name[song]
        if song not in song_id_to_lyrics.keys():
            # try to get song lyrics
            try:
                song = genius.search_song(song_name, song_artist)
                # print(song_name, '\n', song.lyrics)
                song_id_to_lyrics[song] = song.lyrics
                print("success for", song_name, song_artist, len(list(song_id_to_lyrics.keys())))
            except:
                failed_songs.append(song)
                print("failed for", song_name, song_artist)
        else:
            #already exists pass
            pass
    except:
        failed_songs.append(song)
        print("failed", len(failed_songs))
        pass

# Save the list to a pickle file
with open("failed_songs.pkl", "wb") as f:
    pickle.dump(failed_songs, f)

# Save the dictionary to a pickle file
with open("song_id_to_name.pkl", "wb") as f:
    pickle.dump(song_id_to_name, f)

with open("song_id_to_artist_name.pkl", "wb") as f:
    pickle.dump(song_id_to_artist_name, f)

with open("song_id_to_lyrics.pkl", "wb") as f:
    pickle.dump(song_id_to_lyrics, f)


# with open("failed_songs.pkl", 'rb') as f:
#     failed_songs = pickle.load(f)

# # Load the dictionary from a pickle file
# with open('song_id_to_name.pkl', 'rb') as f:
#     song_id_to_name = pickle.load(f)

# with open('song_id_to_artist_name.pkl', 'rb') as f:
#     song_id_to_artist_name = pickle.load(f)

# with open('song_id_to_lyrics.pkl', 'rb') as f:
#     song_id_to_lyrics = pickle.load(f)
