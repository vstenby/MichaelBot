import numpy as np
import random
import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
from youtube_search import YoutubeSearch
import json
import youtube_dl
import csv
from datetime import datetime

def load_mp3s():
    file = open('./resources/txt/str_to_mp3.txt', 'r')
    lines = file.readlines()
    lines = [x for x in lines if x[0]!='#']
    lines = [x.replace('\n','').split(', ') for x in lines]
    lines = [x for x in lines if x!=['']]
    lines = np.array(lines)
    return lines

def list_mp3s():
    lines = load_mp3s()
    s = '```\n'
    s + 'Du kan afspille de følgende klip: \n\n'
    for i in range(len(lines)):
        s = s + lines[i,0]
        if i != len(lines)-1:
            s = s + '\n'
    s = s + '```'
    return s
    
    
def rand_mp3(mp3):
    #Takes a mp3 path (random_kanisedet for instance), and returns a correct path.

    if mp3=='random_sedet':
        path_folder = './resources/random/kanisedet/'


    path_contents = os.listdir(path_folder)
    path_contents = [x for x in path_contents if x[0] != '.']

    mp3 = path_folder + random.choice(path_contents)

    return mp3

def str_to_mp3(p, lines):
    strs = lines[:,0]
    mp3s = lines[:,1]

    str_c = [s for s in strs if s.lower() in p.lower()]

    mp3 = mp3s[strs == str_c]
    if len(mp3) != 1:
        #Wrong number of mp3s found, and it should go on error.
        mp3 = ''
    else:
        mp3 = mp3[0].strip()

    if 'random' in mp3:
        mp3 = rand_mp3(mp3)

    return mp3

def enote_comment(arg):
    #Generates a random comment for the eNotes.
    import random
    eNote = 'eNote '+str(arg+1)

    answers = [eNote + ' - det er sgu en banger.',
              'Jeg kunne næsten ikke have skrevet ' + eNote + ' bedre selv. Der ramte Karsten sgu hovedet på sømmet.',
              eNote + " - og så er pdf'en ovenikøbet lovlig.",
              'Hørte jeg nogen råbe efter ' + eNote +'? Den kommer ihvertfald her!']

    return random.choice(answers)

def load_bom1():
    lectures = os.listdir('./resources/bom1_export/lecture/')

    clips = np.array([])
    clips_lecture = np.array([])
    for lecture in lectures:
        clips = np.append(clips, os.listdir('./resources/bom1_export/lecture/' + lecture))
        clips_lecture = np.append(clips_lecture, [lecture] * len(os.listdir('./resources/bom1_export/lecture/' + lecture)))

    obj =  np.char.split(clips, ' ', maxsplit=3)

    df = pd.DataFrame.from_records(list(obj), columns=['L', 'K', 'R', 'Navn'])
    paths = [''] * len(clips)
    for i in range(len(clips)):
        paths[i] = './resources/bom1_export/lecture/' + clips_lecture[i] + '/'+ clips[i]
    df['Path'] =  paths
    df['L_n'] = df['L'].str.replace('L', '').astype(int)
    df['K_n'] = df['K'].str.replace('K', '').astype(int)
    df['R_n'] = df['R'].str.replace('R', '').astype(int)
    df['Navn'] = df['Navn'].str.replace('.mp4', '')
    df['Navn'] = df['Navn'].str.replace('.m4v', '')
    df = df.sort_values(['L_n', 'K_n'])

    return df

def str_to_bom1(arg, df_bom1):
    #Takes a string, returns bom1 path.
    LK = df_bom1['L'] + ' ' + df_bom1['K']
    path = df_bom1['Path'].loc[arg == LK].squeeze()
    return path


def msg_bom1_table(df_bom1):
    df = df_bom1
    str_list = [''] * len(np.unique(df.L_n))
    idx = 0
    for i in np.unique(df.L_n):
        string = ''
        df_temp = df.loc[df.L_n == i]
        strings = df_temp['L'] + ' ' + df_temp['K'] + ' ' + df_temp['R'] + ' ' + df_temp['Navn'].str.strip()
        for x in strings: string = string + x.strip() + '\n'
        
        str_list[idx] = string
        idx = idx + 1

    return str_list

def get_youtube_id(s):
    #Recieves the YouTube ID for a given string. Input is either <url> or <search words>.
    ID = None
    #Code for getting the ID if it is a YouTube URL.
    query = urlparse(s)
    if query.hostname == 'youtu.be':
        ID = query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            ID = p['v'][0]
        if query.path[:7] == '/embed/':
            ID = query.path.split('/')[2]
        if query.path[:3] == '/v/':
            ID = query.path.split('/')[2]
    if ID is None:
        #Getting the ID from a YouTube search if it is not a YouTube URl.
        search = YoutubeSearch(s, max_results = 1).to_json()
        ID = json.loads(search)['videos'][0]['id']
    
    url = 'https://www.youtube.com/watch?v=' + ID
    return url, ID

def song_available(search):
    url, song_id = get_youtube_id(search)
    song_path = './resources/yt/' + song_id + '.mp3'
    song_exist = os.path.isfile(song_path)
    
    return song_exist
    


def load_QA():
    #Returns the answer based on the message sent in the chat.
    file = open('./resources/txt/QA.txt', 'r')
    lines = file.readlines()
    lines = [x for x in lines if x[0] != '#'] #removes start comments
    Q = [x.replace('Q:', '').replace('\n', '').strip() for x in lines if x[:2] == 'Q:']
    A = [x.replace('A:', '').replace('\n', '').strip() for x in lines if x[:2] == 'A:']
    
    q = []
    a = []
    
    for i in range(len(Q)):
        a_temp = ''
        q_temp = ''
        if Q[i].find(';') != -1:
            #Several answers
            q_temp = Q[i].split(';')
        else:
            q_temp = [Q[i]]
            
        if A[i].find(';') != -1:
            a_temp = A[i].split(';')
        else:
            a_temp = [A[i]]
            
        q.append(q_temp)
        a.append(a_temp)
    
    return q, a

def QA(q_prompt, q_list, a_list):
    idx = -1
    q_prompt = q_prompt.strip()
  
    for i in range(len(q_list)): 
        if q_prompt in q_list[i]: 
            idx = i
            
    if idx==-1:
        a_prompt = ''
    else:
        if len(a_list[idx]) != 1:
            a_prompt = random.choice(a_list[idx])
        else:
            a_prompt = a_list[idx][0]          
    return a_prompt

def custom_msg(s):
    #Returns a custom message (e.g error messages)
    file = open('./resources/txt/custom_msg.txt', 'r')
    lines = file.readlines()
    lines = [x.replace('\n', '') for x in lines]
    lines = np.asarray(lines)    
    try:
        idx1 = np.where(lines == s)[0][0]
    except:
        return ''
    idx2 = idx1 + 1
    temp_line = lines[idx2]
    answs = []; 
    
    while temp_line != '':
        answs.append(temp_line)
        idx2 = idx2 + 1
        try:
            temp_line = lines[idx2]
        except:
            break
    response = random.choice(answs)
    return response

#Queue functions
    
def add_to_queue(path):
    #Adds a song to the queue.
    file = open('./resources/txt/queue.txt', 'a')
    file.write(path + '\n')
    file.close()
    
def clear_queue():
    #Clears the queue.
    file = open('./resources/txt/queue.txt', 'w')
    file.close()
    
def remove_from_queue(ID):
    #Removes a song from the queue.
    file = open('./resources/txt/queue.txt', 'r')
    lines = file.readlines()
    file = open('./resources/txt/queue.txt', 'w')
    for line in lines:
        if line.strip('\n') != ID:
            file.write(line)

def remove_first_queue():
    #Removes the first song in the queue
    file = open('./resources/txt/queue.txt', 'r')
    lines = file.readlines()
    file = open('./resources/txt/queue.txt', 'w')
    for line in lines[1:]:
        file.write(line)

def fetch_from_queue():
    #Fetches the first song from the queue.
    file = open('./resources/txt/queue.txt', 'r')
    line = file.readline().strip('\n')
    return line
    
def is_queue_empty():
    #Checks if the queue is empty
    file = open('./resources/txt/queue.txt', 'r')
    lines = file.readlines()
    lines = [x.strip('\n') for x in lines]
    if len(lines) == 0: 
        return True 
    else: 
        return False

def init_points():
    df = pd.DataFrame({'User' : [], 'Point' : [], 'Timestamp' : [], 'Reason' : []})
    df.to_excel('./resources/other/point_history.xlsx')
        
def save_points(df):
    df.to_excel('./resources/other/point_history.xlsx', index=False)
                   
def load_points():
    df = pd.read_excel('./resources/other/point_history.xlsx')
    return df

def gamble(user, df, n):
    #Available points
    p = np.sum(df['Point'].loc[df['User'] == user])
    
    time = datetime.now()
    ts = time.strftime("%m/%d/%Y, %H:%M:%S")
    
    if type(n) is str:
        if n.lower() == 'max':
            n = p
    
    if n > p: return df, None
    
    #Coin is flipped.
    c = random.randint(0,1)
    
    if c:
        rtrn = n
    else:
        rtrn = -n
    
    if rtrn > 0: 
        rson = 'Won a gamble with ' + str(n)
    else:
        rson = 'Lost a gamble with ' + str(n)
        
    df = df.append(pd.DataFrame({'User' : user, 'Point' : rtrn, 'Timestamp' : ts, 'Reason' : rson}, index=[0]))
    
    return df, rtrn > 0

def bank(user, df):
    #Returns the amount the person has in the pocket.
    p = np.sum(df['Point'].loc[df['User'] == user])
    return p

def graph(user, df):
    #Plots a users MichaelBucks.
    import matplotlib.pyplot as plt
    points = df['Point'].loc[df['User'] == user]
    ts = df['Timestamp'].loc[df['User'] == user]
    fix, ax = plt.subplots(1)
    
    ax.plot(ts, np.cumsum(points))
    
    ax.set_xlabel('Tid')
    ax.set_xticklabels([])
    plt.title('Pointoversigt for ' + user)
    
    plt.savefig('./resources/other/temp.png')   
    
def donate_points(user1, user2, v, df):
    #Donates from User 1 to User 2.
    p = bank(user1, df)
    if v > p: 
        #User 1 cannot send that much money.
        rtrn = False
        return df, -1
    
    if not np.isin(user2, df['User']):
        #Unknown reciever
        rtrn = False
        return df, -2
    
    else:
        time = datetime.now()
        ts = time.strftime("%m/%d/%Y, %H:%M:%S")
        df = df.append(pd.DataFrame({'User' : [user1, user2], 'Point' : [-v, v], 'Timestamp' : [ts] * 2, 'Reason' : ['Donated ' + str(v) + ' to ' + user2, 'Recieved ' + str(v) + ' from ' + user1]}))
        rtrn = True
        return df, rtrn

def highscore(df):
    #Returns the 5 highest scores
    df_temp = df.groupby(["User"]).sum().reset_index()
    df_temp = df_temp.sort_values(by=['Point'], ascending=False)
    users = df_temp['User'].iloc[0:5]
    points = df_temp['Point'].iloc[0:5]
    users = list(users)
    points = list(points)
    
    time = datetime.now()
    ts = time.strftime("%d/%m/%Y, %H:%M:%S")
    
    s = '```\n'
    s = s + 'MichaelBucks - highscore for ' + ts + ' \n\n'
    for i in range(len(users)):
        s = s + str(i+1) + ': ' + users[i] + ' med ' + str(points[i]) + ' MichaelBucks.\n'
    s = s + '\n```'
    return s

