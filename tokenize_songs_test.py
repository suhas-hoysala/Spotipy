from TodoSpotify import TokenizeSong, get_songs_list
from random import shuffle
exceptions = {
    "Lord Ullin's Daughter feat. Jude Law (Japanese Bonus Track)": "Lord Ullin's Daughter",
    "Dedicated - LPU Rarities": "Dedicated",
    "She Sells Sanctuary (2009 Re-master)": "She Sells Sanctuary",
    "Dayton, Ohio - 1903 - Remastered": "Dayton, Ohio - 1903",
    "Ghost Rider - 2019 - Remaster": "Ghost Rider",
    "Running Up That Hill (A Deal with God)": "Running Up That Hill (A Deal with God)",
    "Suicide Is Painless - From the 20th Century-Fox film \"\"M*A*S*H\"": "Suicide Is Painless"
}

def run_test():
    for k, v in exceptions.items():
        ts = TokenizeSong()
        assert ts.tokenize_song_name(k) == v

#run_test()

def list_duplicate_song_names():
    songs_list = get_songs_list()
    shuffle(songs_list)
    count = 1
    for x in songs_list:
        ts = TokenizeSong()
        if str(x["track"]["name"]) != str(ts.tokenize_song_name(x["track"]["name"])):
            print(f'{str(x["track"]["name"])} *** {str(ts.tokenize_song_name(x["track"]["name"]))}')
            count+=1
        if count%10==0:
            input("")
            count+=1