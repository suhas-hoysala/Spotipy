from webbrowser import get
from scanLikedSongs import SongsScanner
import math
import json
import re
import os
from dateutil.relativedelta import relativedelta
from datetime import datetime


class TokenizeSong():
    def unwanted(self):
        return ['mono', 'bbc one', 're-master', 'remastered', 'from', 'rarities', 'spider-man: into the spider-verse', 'style', 'reanimation', 'blend', 'stereo', 'official', 'original', 'session', 'sessions', 'demo', 'edition', 'instrumental', 'motion picture', 'film', 'edit', 'remastered', 'track', 'remaster', 'theme', 'studio recording', 'live', 'version', 'acoustic', 'remix', 'single', 'recorded', 'feat', 'b-side' 'bsides', 'with(?! god)', 'mix', 'master']

    def splitters(self):
        return ['-', ';', '/', ]

    def remove_from_para(self, name):
        reg_exes = ['\((.*?)\)', '\[(.*?)\]']
        for reg_ex in reg_exes:
            pattern = re.compile(reg_ex)
            in_para = pattern.finditer(name)
            prev_pos = 0
            for match in in_para:
                x = match.group()
                if any([re.search(y, x.lower()) for y in self.unwanted()]):
                    name = name[:prev_pos] + \
                        re.sub(reg_ex,  '', name[prev_pos:], count=1)
                prev_pos = match.start() + 1
            name = re.sub(' +', ' ', name)

        return name

    def split_song(self, name):
        name = re.sub('- \d+ - Remaster(?!ed)', '', name)
        for split in self.splitters():
            if not split in name:
                continue
            split_name = str(name).split(split)
            name = split_name[0]
            for part in split_name[1:]:
                if not any([re.search(y, part.lower()) for y in self.unwanted()]):
                    name += split + part
                else:
                    break
        return name

    def remove_extra(self, name):
        reg_exes = ['\d+ Remaster', '\d+ Remastered', 'Remaster \d+', 'Remastered \d+', '\d+ remastered', '\d+ Remastered',  '\d+ - Remaster',
                    'feat\. [^\(,]*', 'feat [^\(,]*', '\d+ Digital Remaster', '\d+th Anniversary Edition', '\d+ Mix', '\d+" Mix', 'Remaster', 'Broadway Rhearsals Demo', 'Underground Tour']
        for reg_ex in reg_exes:
            name = re.sub(reg_ex, '', name)
        if name.endswith('- '):
            name = name.replace('- ', '')
        return name

    def tokenize_song_name(self, name):
        return self.remove_extra(self.split_song(self.remove_from_para(name))).strip()


def get_parent_dir():
    return os.path.dirname(os.path.realpath(__file__))

class SongSimilarity():
    def songSimilarity(self, song1, song2):
        ts = TokenizeSong()
        song1_name = ts.tokenize_song_name(song1['track']['name'])
        song2_name = ts.tokenize_song_name(song2['track']['name'])

        song1_artists = set(map(lambda x: x['name'], song1['track']['artists']))
        song2_artists = set(map(lambda x: x['name'], song2['track']['artists']))

        if song1_name == song2_name and (
            song1_artists.issubset(song2_artists)
            or song2_artists.issubset(song1_artists)
        ):
            return True
        return False


    def test_song_similarity(self):
        scu = SongCountUpdater()
        songs_list = scu.get_songs_list()
        for i in range(len(songs_list)):
            for j in range(i+1, len(songs_list)):
                song1 = songs_list[i]
                song2 = songs_list[j]
                if self.songSimilarity(song1, song2):
                    song1_name = song1['track']['name']
                    song2_name = song2['track']['name']
                    print(f'{song1_name} {song2_name}')

class SongCountUpdater():
    def get_songs_list(self):

        ts_now = datetime.now()

        parent_dir = get_parent_dir()
        util_file = open(f'{parent_dir}\\util.json', 'r')
        util = json.load(util_file)
        ts_then = datetime.fromtimestamp(util.get('last_updated'))

        update_interval = util.get('update_interval')

        time_change = relativedelta(ts_now, ts_then).hours

        if time_change > update_interval:
            scanner = SongsScanner()
            songs_list = scanner.get_songs()
            with open(f'{parent_dir}\\data\\songs_list.json', 'w+', encoding='utf8') as songs_file:
                songs_file.write(json.dumps(
                    songs_list, ensure_ascii=False).encode('utf8').decode('utf8'))
            util['last_updated'] = ts_now.timestamp()
            util_file_write = open(f'{parent_dir}\\util.json', 'w+')
            json.dump(util, util_file_write)

        else:
            songs_list = json.load(
                open(f'{parent_dir}\\data\\songs_list.json', encoding='utf8'))

        return songs_list


    def artist_to_tracks(self):
        songs_list = self.get_songs_list()
        artist_dict = {}
        for item in songs_list:
            track = item['track']
            for artist_rec in track['artists']:
                name = artist_rec['name']
                if not name in artist_dict:
                    artist_dict[artist_rec['name']] = []
                artist_dict[artist_rec['name']].append(item)
        return artist_dict


    def write_30_song_artists_to_file(self):
        songs_list = self.get_songs_list()
        parent_dir = os.path.dirname(os.path.realpath(__file__))
        with open(f'{parent_dir}\\data\\artists_list.json', encoding='utf8') as file:
            artists_list = json.load(file)

        artists_list_30 = artists_list['30']

        artist_dict = {name: [] for name in artists_list_30}

        artists_list_lower = list(map(lambda x: x.lower(), artists_list_30))

        for item in songs_list:
            track = item['track']
            for artist_rec in track['artists']:
                name = artist_rec['name']
                try:
                    index = artists_list_lower.index(name.lower())
                    artist_dict[artists_list_30[index]].append(item)
                except(ValueError):
                    continue

        #remove duplicates
        song_sim = SongSimilarity()
        for artist_name, artist_list in artist_dict.items():
            artist_list_new = artist_list.copy()
            for i in range(len(artist_list)):
                for j in range(i+1, len(artist_list)):
                    if song_sim.songSimilarity(artist_list[i], artist_list[j]):
                        artist_list_new.remove(artist_list[j])
            artist_dict[artist_name] = artist_list_new

        artist_dict_count = {}
        for artist, artist_song_list in artist_dict.items():
            artist_dict_count[artist] = len(artist_song_list)

        with open(f'{parent_dir}\\data\\target_artists.json', 'w+', encoding='utf8') as file:
            file.write(json.dumps(artist_dict, ensure_ascii=False).encode(
                'utf8').decode('utf8'))

        with open(f'{parent_dir}\\data\\target_artists_count.json', 'w+', encoding='utf8') as file:
            file.write(json.dumps(artist_dict_count,
                    ensure_ascii=False).encode('utf8').decode('utf8'))

scu = SongCountUpdater()
scu.write_30_song_artists_to_file()