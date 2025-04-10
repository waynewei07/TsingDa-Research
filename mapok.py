# Example Usage : python3 n-gram.py -f harry.txt -g 5
import argparse
import os
import sqlite3
from bs4 import BeautifulSoup
from colorama import *
info = lambda x: print(Fore.GREEN+'[+] '+Fore.WHITE+f'{x}')

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help='File name')
parser.add_argument('-g', '--gram', required=True, help='Max gram value')
args = parser.parse_args()

N_gram=int(args.gram)+1
f=open(args.file, 'rb')
content=f.read().decode()
sentences=content.split('\n')
# print(len(sentences))

'''conn=sqlite3.connect('database.db')

c=conn.cursor()

c.execute("""CREATE TABLE n_gram(
    gram text,
    cnt integer
)""")'''

def find(str):
    c.execute("SELECT * FROM n_gram WHERE gram=:gram", {'gram': str})
    return len(c.fetchall())>0

def array2string(x):
    ret=x[0]
    for i in range(1, len(x)):
        ret+=' '
        ret+=x[i]
    return ret

def expand_query(query):
    # TODO: write your query expansion, e.g.,
    #  "in/at afternoon" -> ["in afternoon", "at afternoon"]
    #  "listen ?to music" -> ["listen music", "listen to music"]_
    # print('test')
    pre=''
    suf=''
    tf=0
    mid=''
    for sen in query.split():
        if(sen.find('/')==-1 and sen.find('?')==-1):
            if(tf):
                suf+=' '+sen
            else:
                pre+=' '+sen
        else:
            tf=1
            mid=sen
    vec=[]
    cnt=0
    mid=mid.replace('?','/')
    # print(mid)
    for sen in mid.split('/'):
        if(sen!=''): sen=(' '+sen)
        #print((pre+sen+suf).strip())
        vec.append((pre+sen+suf).strip())
        #cnt=cnt+1
    for sen in vec:
        print(sen)
    return vec

gram_box={[]:0}

for n in range(1, N_gram):
    info(f"Counting {n} - gram")
    for sen in sentences:
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
                str=sen[i]
                if array2string(sen[i:i+n]) not in gram_box and len(array2string(sen[i:i+n]))>0:
                    #str=array2string(sen[i:i+n])
                    #c.execute("INSERT INTO n_gram VALUES (:gram,:cnt)",{'gram':str,'cnt':1})
                    gram_box[array2string(sen[i:i+n])]=1
                elif len(array2string(sen[i:i+n]))>0:
                    #str=array2string(sen[i:i+n])
                    #c.execute("INSERT INTO n_gram VALUES (:gram,:cnt)",{'gram':str,'cnt':1})
                    gram_box[array2string(sen[i:i+n])]+=1

sorted_gram_box=sorted(gram_box.items(), key=lambda x: x[1], reverse=True)

while 1:
    x=input("please enter query:")
    if(x=="!quit"):
        break
    sum=0
    for v in sorted_gram_box:
        key=v[0]
        if key.find(x)==0:
            #print(f'"{key}"', ':', v[1])
            sum+=v[1]
    for v in sorted_gram_box:
        key=v[0]
        if key.find(x)==0 and 0.01<(v[1]/sum*100):
            s=f'"{key}"'.ljust(25)
            t=(str(v[1])+'/'+str(sum)).ljust(10)
            print(s,t,'%:',round(v[1]/sum*100,2))