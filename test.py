from pytube import YouTube
import pytube
import os
import json
import tempfile
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url)

for i in yt.streams.order_by("resolution").desc().filter(file_extension="mp4",only_video=True,progressive=False):
    if i.filesize <= 10485760:
        break
print(i.filesize/1000)
    
# with open("G:\projects\disBot2/tmp2.txt","w") as f:
#     for i,k in enumerate(yts):
#         # f.write(f"{k} ; {i} ; {k.filesize/1000} \n")
#         f.write(str(k)+"\n")

'''
for vidm,vid in enumerate(yts):
    if vid.filesize >= 10485760: 
        # print("Too large: "+str(round(vid.filesize/1000)))
        if prev:
            print("AAAAAAAAA: "+str(vid.filesize/1000)+" ; "+vid.resolution)
            print(f"prev {yts[vidm-1].filesize/1000}; {vidm}")
        continue
    with tempfile.TemporaryDirectory() as td:
        prev = True
        # print("just right: "+str(round(vid.filesize/1000))+" ; "+vid.resolution)
'''