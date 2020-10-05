import os
import sys
import re

if len(sys.argv) >= 2:
    path_name = sys.argv[1]
else:
    path_name = 'D:\\점검중'

file_list = os.listdir(path_name)
os.chdir(path_name)

count = 0

for f in file_list:
    if  f.endswith(('mp4', 'wmv', 'avi', 'mkv')):
        oldname = f
        newname = oldname
        newname = re.sub('-uncensored', '', newname)
        newname = re.sub('\[88q.me\]', '', newname)
        newname = re.sub('\[44x.me\]', '', newname)
        newname = re.sub('\[456k.me\]', '', newname)

        newname = re.sub('ch.', '.', newname)
        newname = re.sub('stars00', 'stars-', newname)

        # print('oldname: ' + oldname)
        # print('newname: ' + newname)
        # print('')

        try:
            os.rename(oldname, newname)
            count += 1
        except FileExistsError as e:
            print("File Exist")

print(count.__str__() + ' 건이 처리되었습니다.')
