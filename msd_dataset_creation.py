import lyricsgenius
import pickle
import time
import tqdm

# with open('song_id_to_lyrics.pkl', 'rb') as f:
#     song_id_to_lyrics = pickle.load(f)
song_id_to_lyrics2 = {}
genius = lyricsgenius.Genius(
    "g4zT_dicPfN839Lvvbg8D3AxQBH4-0zVa6XS63btWRX74zTvu7KLh8ZoNASBL6pa",
    skip_non_songs=True,
)
failed_ids = 0 
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
            if song in song_id_to_lyrics2.keys() or failed_ids:
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
                song_id_to_lyrics2[song_id] = lyrics
            else:
                failed_ids.append(song_id)
             


with open("song_id_to_lyrics2.pkl", "wb") as f:
    pickle.dump(song_id_to_lyrics2, f)

# with open("song_id_to_lyrics2.pkl", "rb") as f:
#     pickle.load(song_id_to_lyrics2, f)