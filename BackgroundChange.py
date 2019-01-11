import ctypes
import os
import time
import random
from bs4 import BeautifulSoup
import requests
import re
import send2trash


def setWallpaper(filepath):
    #checks that filepath given is an existing one
    if not os.path.isfile(filepath):
        return False
    
    #checks that file has image extension
    if not re.search('.jpg', filepath) and not re.search('.png', filepath):
        return False
    
    #configuration
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, 0)

    print('\nDone!')
    return True


def downloadWallpaper(downloadlink, directory):
    if downloadlink is None:
        return
    #makes an http request
    r = requests.get(downloadlink, allow_redirects=True)

    #retrieves filename from cd and creates save directory
    full_file_name = getFilename(r.headers.get('content-disposition'))
    full_file_name = os.path.join(directory, full_file_name) + '.jpg'
    
    #creates image file  
    open(full_file_name, 'wb').write(r.content)
    time.sleep(1)

    setWallpaper(full_file_name)
    return


def getFilename(cd):
    #checks that content-diposition exists
    if not cd:
        return None
    
    #finds file name from content-disposition
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    fname[0] = fname[0].strip('"')
    return fname[0]

    
def getWallpaperDownloadURL(link):
    
    #gets webpage html from given link
    result = requests.get(link)
    pagehtml = result.content
    
    #parses through html to find img elements
    soup = BeautifulSoup(pagehtml, 'html.parser')
    samples = soup.find_all('a', attrs={'title': 'Download photo'})

    #checks that at least one img element was found
    if not len(samples):
        print('No images found for keyword: ' + re.sub('https://unsplash.com/search/photos/', '', link))
        return None
        
    #chooses random image url to from list of img elements 
    size = len(samples)
    x = random.choice(range(size))
    imglink = samples[x]['href']
    print('Setting desktop background to an image of ' + re.sub('https://unsplash.com/search/photos/', '', link))
    return imglink


def unsplashSearch(keyword):
    #creates unsplash search link randomly
    if keyword == 'random':
        randomlibrary = ['https://unsplash.com/t/wallpapers', 'https://unsplash.com/t/arts-culture',
                         'https://unsplash.com/t/textures-patterns', 'https://unsplash.com/t/architecture',
                         'https://unsplash.com/t/animals', 'https://unsplash.com/t/travel',
                         'https://unsplash.com/t/food-drink']
        link = random.choice(randomlibrary)
        
    #creates unsplash search link for given keyword
    else:
        keyword = keyword.replace(' ', '-')
        link = 'https://unsplash.com/search/photos/' + keyword
    
    return link


def getOldestFile(directory):
    #checks that path is existing directory
    if not os.path.isdir(directory):
        return None
    
    #gets filenames of images in directory
    imagelist = os.listdir(directory)

    if not len(imagelist):
        return None
    
    timelist = []
    pathlist = []

    #creates list with file times and corresponding path list
    for image in imagelist:
        path = os.path.join(directory, image)
        pathlist.append(path)
        timelist.append(os.path.getctime(path))

    #finds oldest file from minimum time
    targetimage = timelist.index(min(timelist))
    return pathlist[targetimage]

def manageFolder(directory):
    #checks if folder has too many files
    if len(os.listdir(directory)) > 7:
        f = getOldestFile(directory)
        if f is None:
            return
        elif re.search('unsplash', f):
            send2trash.send2trash(f)
    return 







    
        




