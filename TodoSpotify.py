from scanLikedSongs import SongsScanner
import math
import json
import re
from random import shuffle

unwanted = ['mono', 'bbc one', 're-master', 'remastered', 'from', 'rarities', 'spider-man: into the spider-verse', 'style', 'reanimation', 'blend', 'stereo', 'official', 'original', 'session', 'sessions', 'demo', 'edition', 'instrumental', 'motion picture', 'film', 'edit', 'remastered', 'track', 'remaster', 'theme', 'studio recording', 'live', 'version', 'acoustic', 'remix', 'single', 'recorded', 'feat', 'b-side' 'bsides', 'with(?! god)', 'mix', 'master']
splitters = ['-', ';', '/', ]
def remove_from_para(name):
    reg_exes = ['\((.*?)\)', '\[(.*?)\]']
    for reg_ex in reg_exes:
        pattern = re.compile(reg_ex)
        in_para = pattern.finditer(name)
        prev_pos = 0
        for match in in_para:
            x = match.group()
            if any([re.search(y, x.lower()) for y in unwanted]):
                name = name[:prev_pos] + re.sub(reg_ex,  '', name[prev_pos:], count=1)
            prev_pos = match.start() + 1
        name = re.sub(' +', ' ', name)
    return name

def split_song(name):
    name = re.sub('- \d+ - Remaster(?!ed)', '', name)
    for split in splitters:
        if not split in name:
            continue
        split_name = str(name).split(split)
        name = split_name[0]
        for part in split_name[1:]:
            if not any([re.search(y, part.lower()) for y in unwanted]):
                name += split + part
            else:
                break
    return name

def remove_extra(name):
    reg_exes = ['\d+ Remaster', '\d+ Remastered', 'Remaster \d+', 'Remastered \d+', '\d+ remastered', '\d+ Remastered',  '\d+ - Remaster', 'feat\. [^\(,]*', 'feat [^\(,]*', '\d+ Digital Remaster', '\d+th Anniversary Edition', '\d+ Mix', '\d+" Mix', 'Remaster', 'Broadway Rhearsals Demo', 'Underground Tour']
    for reg_ex in reg_exes:
        name = re.sub(reg_ex, '', name)
    if name.endswith('- '):
        name = name.replace('- ', '')
    return name

def tokenize_song_name(name):
    return remove_extra(split_song(remove_from_para(name))).strip()
    
def songSimilarity(song1, song2):
    pass
# def songSimilarity(song1, song2):
#     global getter
#     time1, time2 = (getter(song1,'duration_ms'), getter(song2, 'duration_ms'))
#     name1, name2 = (getter(song1,'name'), getter(song2, 'name'))
#     album1, album2 = (song1['track']['album']['name'], song2['track']['album']['name'])
#     artist1, artist2 = (getter(song1,'artists'), getter(song2, 'artists'))

#     name1,name2, album1, album2 = map(lambda x: x.replace("Remastered", ""), (name1,name2, album1, album2))
#     hammingsim = lambda x1, x2: textdistance.hamming.normalized_similarity(x1,x2)

#     if abs(time1-time2)<0.05*time1:
#         if hammingsim(name1, name2)>0.5:
#             return True
#     return False


exceptions = ['Lord Ullin\'s Daughter feat. Jude Law (Japanese Bonus Track)', 'Dedicated - LPU Rarities', 'She Sells Sanctuary (2009 Re-master)', 'Dayton, Ohio - 1903 - Remastered', 'Ghost Rider - 2019 - Remaster', 'Running Up That Hill (A Deal with God)', 'Suicide Is Painless - From the 20th Century-Fox film ""M*A*S*H"']
for ex in exceptions:
    print(tokenize_song_name(ex)+"**")
scanner = SongsScanner()
songs_list = scanner.get_songs()
shuffle(songs_list)
count = 1
for x in songs_list:
    if str(x["track"]["name"]) != str(tokenize_song_name(x["track"]["name"])):
        print(f'{str(x["track"]["name"])} *** {str(tokenize_song_name(x["track"]["name"]))}')
        count+=1
    if count%10==0:
        input("")
        count+=1

#test tokenizer
# for i in range(len(songs_list)):
#     print(tokenize_song_name(songs_list[i]))
#     if i%10==0:
#         input("")
#print(json.dumps(songs_list[0], indent=4))
# for index1 in range(len(songs_list)):
#     for index2 in range(index1+1, len(songs_list)):
#         song1, song2 = map(lambda x: songs_list[x], (index1, index2))
#         if songSimilarity(songs_list[index1], songs_list[index2]):
#             print([song1['track']['name'], song1['track']['album']['name'], song1['track']['duration_ms']], [song2['track']['name'], song2['track']['album']['name'], song2['track']['duration_ms']])