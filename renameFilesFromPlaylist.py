'''
Had an issue with a Philips stereo not able to read .m3u playlists, so played everything alphabetically.
Created script to rename the files to "number - filename"

reads from an m3u playlist file in format:

#EXTM3U
#EXTINF:235,Cher - Believe
Cher - Believe.mp3
'''
# modules
import os

# Read playlist
def gen_playlist(objFilename):
    for line in objFilename:
        if line.startswith("#") or len(line)<3:
            continue
        else:
            yield line.strip("\n")
            
with open("_PlayList.m3u","r") as f:
    number = 1
    for line in gen_playlist(objFilename=f):
        line.strip("\n")
        newname = "00" + str(number) + " - " + str(line)
        try:
            os.rename(line,newname)
        except:
            print("error"+line)
        number += 1

