# Example Usage : python3 n-gram.py -f harry.txt -g 5
import argparse
import os
import sqlite3
from bs4 import BeautifulSoup
from colorama import *
info = lambda x: print(Fore.GREEN+'[+] '+Fore.WHITE+f'{x}')

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help='File name')
parser.add_argument('-gmn', '--gramn', required=True, help='Min gram value')
parser.add_argument('-gmx', '--gramx', required=True, help='Max gram value')
args = parser.parse_args()

N_gramn=int(args.gramn)
N_gramx=int(args.gramx)+1
f=open(args.file, 'rb')
content=f.read().decode()
sentences=content.split('\n')
# print(len(sentences))

# conn=sqlite3.connect('database.db')
conn = sqlite3.connect(':memory:')


c=conn.cursor()

# 資料型態為 {n-gram, count of n-gram}

c.execute("""CREATE TABLE n_gram(
    gram text, 
    cnt integer
)""")

def find(strr):
    c.execute("SELECT * FROM n_gram WHERE gram=:gram", {'gram': strr})
    return c.fetchone()!=None

def arraytostring(x):
    ret=x[0]
    for i in range(1, len(x)):
        ret+=' '
        ret+=x[i]
    return ret

gram_box={'':0}

for n in range(N_gramn, N_gramx):
    info(f"Counting {n} - gram")
    now=0
    print(len(sentences))
    for sen in sentences:
        now+=1
        print(now)
        #print(sen)
        '''if(now==20):
            break'''
        sen=sen.replace(',','')
        sen=sen.replace('"','')
        sen=sen.replace(':','')
        sen=sen.replace('.','')
        sen=sen.replace('!','')
        sen=sen.replace('?','')
        sen=sen.replace(']','')
        sen=sen.replace('[','')
        sen=sen.split(' ')
        if len(sen)<n:
            continue
        else:
            for i in range(0, len(sen)-n+1):
                # 將陣列轉換為字串
                str=arraytostring(sen[i:i+n])
                if(len(str)<=0):
                    continue
                # 插入 n_gram
                if(find(str)==0):
                    with conn:
                        c.execute("INSERT INTO n_gram VALUES (:gram,:cnt)",{'gram':str,'cnt':1})
                        conn.commit()
                # 更新 n_gram 出現次數
                else:
                    c.execute("SELECT * FROM n_gram WHERE gram=:gram", {'gram': str})
                    current_gram=c.fetchone()
                    with conn:
                        c.execute("""UPDATE n_gram SET cnt = :cnt WHERE gram = :gram""",{'gram': current_gram[0], 'cnt': current_gram[1]+1})
                        conn.commit()

c.execute("SELECT * FROM n_gram order by cnt desc")
box=c.fetchall()
# sorted_gram_box=sorted(box.items(), key=lambda x: x[1], reverse=True)

while 1:
    x=input("please enter phrase(quit to quit):")
    if(x=="quit"):
        break
    sum=0
    for v in box:
        key=v[0]
        if key.find(x)==0:
            #print(f'"{key}"', ':', v[1])
            sum+=v[1]
    for v in box:
        key=v[0]
        if key.find(x)==0 and 0.01<(v[1]/sum*100):
            s=f'"{key}"'.ljust(25)
            t=(str(v[1])+'/'+str(sum)).ljust(10)
            print(s,t,'%:',round(v[1]/sum*100,2))