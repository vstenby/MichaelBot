import pandas as pd
import os
import random
from youtube_search import YoutubeSearch
import json

os.chdir('/Volumes/Seagate/Best of Mat 1/MichaelBot')

num = random.randint(1, 4)
filepath = './Mat1Guessr/mat1guessr_' + str(num) + '.mp4'
df = pd.read_excel('./Mat1Guessr/correct_answers.xlsx')



search = YoutubeSearch(prompt, max_results=1).to_json()
ID = json.loads(search)['videos'][0]['id']