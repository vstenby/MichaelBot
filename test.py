import pandas as pd
import os
import random
os.chdir('/Volumes/Seagate/Best of Mat 1/MichaelBot')

num = random.randint(1, 4)
filepath = './Mat1Guessr/mat1guessr_' + str(num) + '.mp4'
df = pd.read_excel('./Mat1Guessr/correct_answers.xlsx')