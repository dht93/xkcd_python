import requests
from bs4 import BeautifulSoup
import sqlite3

conn=sqlite3.connect('xkcd.sqlite')                     #database file
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS xkcd (num NUMBER PRIMARY KEY, url TEXT)''')

cur.execute('''
SELECT num FROM xkcd''')

l=len(cur.fetchall())+1                                 #starts where the last execution left

for i in range(10):                                     #downloads 20 images in one run
    url='http://xkcd.com/'+str(l)+'/'
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    div=soup.find(id='comic')
    comic='http:'+div.find('img')['src']
    print comic
    p=requests.get(comic)
    c_name=comic.split('comics/')[1]
    f_name=str(l)+'_'+c_name
    with open(f_name,'wb') as f:
            f.write(p.content)
            f.close()
    cur.execute('''
    INSERT INTO xkcd (num,url) VALUES (?,?)''',(l,comic))     #keeping track of photos downloaded
    conn.commit()
    l+=1
