import pickle
import pandas as pd 
import lyricsgenius

with open("failed_songs.pkl", 'rb') as f:
    failed_songs = pickle.load(f)

# Load the dictionary from a pickle file
with open('song_id_to_name.pkl', 'rb') as f:
    song_id_to_name = pickle.load(f)

with open("failed_songs.pkl", 'rb') as f:
    failed_songs = pickle.load(f)

# Load the dictionary from a pickle file
with open('song_id_to_name.pkl', 'rb') as f:
    song_id_to_name = pickle.load(f)

with open('song_id_to_artist_name.pkl', 'rb') as f:
    song_id_to_artist_name = pickle.load(f)

with open('song_id_to_lyrics.pkl', 'rb') as f:
    song_id_to_lyrics = pickle.load(f)



# load the failed songs list 
with open("failed_songs.pkl", 'rb') as f:
    failed_songs = pickle.load(f)

genius = lyricsgenius.Genius(
    "g4zT_dicPfN839Lvvbg8D3AxQBH4-0zVa6XS63btWRX74zTvu7KLh8ZoNASBL6pa",
    skip_non_songs=True,
)
count = 0
# for song in failed_songs:
#     try:
#         song_name = song_id_to_name[song]
#         song_artist = song_id_to_artist_name[song]

#         try:
#             song = genius.search_song(song_name, song_artist)
#             # print(song_name, '\n', song.lyrics)
#             song_id_to_lyrics[song] = song.lyrics
#             print("success for", song_name, song_artist, len(list(song_id_to_lyrics.keys())))
#         except:
#             print("failed for", song_name, song_artist)
#             break

#     except:
#         count+=1
#         print("song_id fail ", count )
        
#         continue
    
# # Step 3: load the user histories
partial_histories = 0
count = 0 
with open("kaggle_visible_evaluation_triplets.txt", "r") as f:
    for line in f:
        old_count = count
        user, song, _ = line.strip().split("\t")
        if song in list(song_id_to_lyrics.keys()):
            count+=1
        else:
            pass
        if count > old_count:
            partial_histories+=1
print(count)
print("partial histories", partial_histories)

            



