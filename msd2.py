# import pickle 

# song_id_to_name= {}
# # Load the dictionary from a pickle file
# with open('song_id_to_name.pkl', 'rb') as f:
#     song_id_to_name = pickle.load(f)
# song_id_to_artist_name= {}
# with open('song_id_to_artist_name.pkl', 'rb') as f:
#     song_id_to_artist_name = pickle.load(f)
# song_id_to_lyrics = {}
# with open('song_id_to_lyrics.pkl', 'rb') as f:
#     song_id_to_lyrics = pickle.load(f)
# count = 0 
# #making final user history file
# with open("user_data.txt", "w") as user_data:
#     with open("usable_user_histories.txt", "r") as f:
#         for line in f:
#             user_id, song_id, artist, song= line.strip().split(',')
#             #no need for artist and song reformatting with updates above 
#             artist = str.lower(artist[3:-1])
#             song = str.lower(song[2:-2])
#             print(artist, song, song_id)
#             if song_id in song_id_to_lyrics.keys():
#                 print(count)
#                 count+=1
#                 user_data.write(
#                     user_id
#                     + ", "
#                     + song_id
#                     + ", "
#                     + song
#                     + ", "
#                     + artist
#                     + "\n"
#                 )

import matplotlib.pyplot as plt

users_to_songs = {}
with open("user_data.txt", "r") as f:
    for line in f:
        user_id, song_id, song, artist = line.strip().split(",")
        if user_id not in users_to_songs.keys():
            users_to_songs[user_id] = [song_id]
        else:
            users_to_songs[user_id].append(song_id)

counts = []
for user in users_to_songs.keys():
    counts.append(len(list(users_to_songs[user])))

plt.hist(counts, bins=100)
plt.title("Distribution of Number of Songs Listened to by Users")
plt.xlabel("Number of Songs")
plt.ylabel("Number of Users")
plt.show()

