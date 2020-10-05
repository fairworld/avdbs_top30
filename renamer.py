import os
import sys
import re

if len(sys.argv) >= 0:
    path_name = sys.argv[1]
else:
    path_name = 'D:\\점검중'

file_list = os.listdir(path_name)
os.chdir(path_name)

for f in file_list:
    if  f.endswith(('mp4', 'wmv', 'avi', 'mkv')):
        oldname = f
        newname = oldname
        newname = re.sub('-uncensored', '', newname)
        newname = re.sub('\[88q.me\]', '', newname)
        newname = re.sub('ch.', '.', newname)
        newname = re.sub('stars00', 'stars-', newname)

        print('oldname: ' + oldname)
        print('newname: ' + newname)
        print('')

        try:
            os.rename(oldname, newname)
        except FileExistsError as e:
            print("File Exist")
