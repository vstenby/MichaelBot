import numpy as np
import random
import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
from youtube_search import YoutubeSearch
import json

def load_mp3s():
    file = open('./resources/str_to_mp3.txt', 'r')
    lines = file.readlines()
    lines = [x.replace('\n','').split(', ') for x in lines]
    lines = [x for x in lines if x!=['']]
    lines = np.array(lines)
    return lines

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


def rand_mp3(mp3):
    #Takes a mp3 path (random_kanisedet for instance), and returns a correct path.

    if mp3=='random_sedet':
        path_folder = './resources/soundfiles/kanisedet/'
    elif mp3=='random_eneste':
        path_folder = './resources/soundfiles/eneste/'
    elif mp3=='random_cirkel':
        path_folder = './resources/soundfiles/enhedsæg/'
    elif mp3=='random_ødeø':
        path_foler = './resources/soundfiles/ødeø/'


    path_contents = os.listdir(path_folder)
    path_contents = [x for x in path_contents if x[0] != '.']

    mp3 = path_folder + random.choice(path_contents)

    return mp3

def load_bom1():
    lectures = os.listdir('./resources/bom1_export/lecture/')

    clips = np.array([])
    clips_lecture = np.array([])
    for lecture in lectures:
        clips = np.append(clips, os.listdir('./resources/bom1_export/lecture/' + lecture))
        clips_lecture = np.append(clips_lecture, [lecture] * len(os.listdir('../export/lecture/' + lecture)))

    obj =  np.char.split(clips, ' ', maxsplit=3)

    df = pd.DataFrame.from_records(list(obj), columns=['L', 'K', 'R', 'Navn'])
    paths = [''] * len(clips)
    for i in range(len(clips)):
        paths[i] = '../export/lecture/' + clips_lecture[i] + '/'+ clips[i]
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
    isYouTube = s.find('youtube.com') != -1
    if isYouTube:
        #Code for getting the ID if it is a YouTube URL.
        s = s.split(' ',1)[0]
        url = s
        u_pars = urlparse(url)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            ID = quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            ID = pth[-1]
    else:
        #Getting the ID from a YouTube search if it is not a YouTube URl.
        search = YoutubeSearch(s, max_results = 1).to_json()
        ID = json.loads(search)['videos'][0]['id']
    
    url = 'https://www.youtube.com/watch?v=' + ID
    return url, ID



def stream_wait_msg():
    #If MichaelBot has to download the file.
    msgs = ['Åh forhelvede, den skal jeg lige have støvet frem. Giv mig 2 sekunder.',
            'Hmm, jeg plejede at have den på vinyl, men den skal jeg måske lige have hentet ned på computeren...',
            'Åh nej, hjælp - moar. Hyl og skrig, den har jeg ikke liggende... Hvordan gør man nu det her...']
    msg = random.choice(msgs)
    return msg

def load_QA():
    #Returns the answer based on the message sent in the chat.
    file = open('./resources/QA.txt', 'r')
    lines = file.readlines()
    
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

def error_message(s):
    #Returns a custom error message.
    file = open('./resources/error_msg.txt', 'r')
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
    


