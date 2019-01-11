'''
Runs BackgroundChange program

Prompted to give search keyword for image
Asks to give full path to directory to save images to
Sets desktop wallpaper to hd image based on search term

'''

import BackgroundChange

#asks for search keyword for unsplash.com
keyword = input('Enter search keyword: ')
websitelink = BackgroundChange.unsplashSearch(keyword)

#asks for full path to save image
direc = input('Enter full path to directory to save images:')

#gets download URL from unsplash.com
dlurl = BackgroundChange.getWallpaperDownloadURL(websitelink)

#creates image file in directory
BackgroundChange.downloadWallpaper(dlurl,direc)


