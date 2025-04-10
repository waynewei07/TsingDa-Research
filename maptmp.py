# Example Usage : python3 n-gram.py -f harry.txt -g 5
import argparse
import os
import sqlite3
from bs4 import BeautifulSoup
from colorama import *
import time
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
    gram text primary key,
    cnt integer
)""")

def find(str):
    c.execute("SELECT * FROM n_gram WHERE gram=:gram", {'gram': str})
    return len(c.fetchall())>0'''



def array2string(x):
    ret=x[0]
    for i in range(1, len(x)):
        ret+=' '
        ret+=x[i]
    return ret

def string2array(x):
    return x.split()

def expand_query(query):
    prefix=''
    suffix=''
    convert=0
    middle=''

    # 找出有特殊詢問字元的位置
    for sen in query.split():
        if(sen.find('/')==-1 and sen.find('?')==-1):
            if(convert):
                suffix+=' '+sen
            else:
                prefix+=' '+sen
        else:
            convert=1
            middle=sen
            
    # 處理詢問
    middle=middle.replace('?','/')
    result=[]
    for sen in middle.split('/'):
        if(sen!=''): sen=(' '+sen)
        result.append((prefix+sen+suffix).strip())
        #cnt=cnt+1
    return result

sorted_gram_box={'':0}
gram_box={'':0}
prv_time=time.time()

def check(aa,bb):
    a=string2array(aa)
    b=string2array(bb)
    for i in range(0,len(a)-len(b)+1):
        cur=True
        for j in range(0,len(b)):
            if(b[j]=='_'):
                continue
            if(a[i+j]!=b[j]):
                cur=False
                break
        if(cur==True):
            return 1
    return 0

def check1(a,b):
    for i in range(0,len(b)):
        if(check(a,b[i])):
            return 1
    return 0

def query(x):
    sum=0
    arr=expand_query(x)
    for v in sorted_gram_box:
        key=v[0]
        if check1(key,arr)==1:
            #print(f'"{key}"', ':', v[1])
            sum+=v[1]
    cnt=0
    for v in sorted_gram_box:
        key=v[0]
        if check1(key,arr)==1 and cnt<20:
            cnt+=1
            s=f'"{key}"'.ljust(35)
            t=(str(v[1])+'/'+str(sum)).ljust(20)
            # print(s,t,'%:',round(v[1]/sum*100,2))

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
                strr=array2string(sen[i:i+n])
                if strr not in gram_box and len(strr)>0:
                    #str=array2string(sen[i:i+n])
                    #c.execute("INSERT INTO n_gram VALUES (:gram,:cnt)",{'gram':str,'cnt':1})
                    gram_box[strr]=1
                elif len(strr)>0:
                    #str=array2string(sen[i:i+n])
                    #c.execute("INSERT INTO n_gram VALUES (:gram,:cnt)",{'gram':str,'cnt':1})
                    gram_box[strr]+=1
    sorted_gram_box=sorted(gram_box.items(), key=lambda x: x[1], reverse=True)
    prv_time=time.time()
    query("in/on the")
    print(n,' ',time.time()-prv_time)


'''while 1:
    x=input("please enter query:")
    if(x=="!quit"):
        break
    query(x)'''
    