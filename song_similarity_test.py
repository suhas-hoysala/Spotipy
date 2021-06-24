from TodoSpotify import SongSimilarity

def test_song_similarity():
    song_sim = SongSimilarity()
    songs_list = song_sim.get_songs_list()
    for i in range(len(songs_list)):
        for j in range(i+1, len(songs_list)):
            song1 = songs_list[i]
            song2 = songs_list[j]
            if song_sim.songSimilarity(song1, song2):
                song1_name = song1['track']['name']
                song2_name = song2['track']['name']
                print(f'{song1_name} {song2_name}')