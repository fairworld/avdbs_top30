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
        newname = re.sub('_FHD', '', newname)
        newname = re.sub('\[88q.me\]', '', newname)
        newname = re.sub('\[44x.me\]', '', newname)
        newname = re.sub('\[456k.me\]', '', newname)
        newname = re.sub('xhd1080.com@', '', newname)
        newname = re.sub('hhb', '', newname)
        newname = re.sub('FHD_6M-', '', newname)
        newname = re.sub(' [AVC 高质量和大小]', '', newname)
        newname = re.sub('\[AVC质量和大小\]', '', newname)
        newname = re.sub('\[ThZu.Cc\]', '', newname)
        newname = re.sub('\[Thz.la\]', '', newname)
        newname = re.sub('\[99u.me\]', '', newname)

        newname = re.sub('hjd2048.com-[0-9]{4}', '', newname)
        newname = re.sub('-h264.', '.', newname)


        newname = re.sub('ch.', '.', newname)
        newname = re.sub('stars00', 'stars-', newname)
        newname = re.sub('ssni00', 'ssni-', newname)
        newname = re.sub('supd00', 'supd-', newname)
        newname = re.sub('ipx00', 'ipx-', newname)
        newname = re.sub('sdmu00', 'sdmu-', newname)
        newname = re.sub('pred00', 'pred-', newname)
        newname = re.sub('kawd00', 'kawd-', newname)
        newname = re.sub('tek00', 'tek-', newname)
        newname = re.sub('mide00', 'mide-', newname)

        # print(re.findall('[a-zA-Z]{2,4}',newname)[0])
        # print(re.findall('[0-9]{3,4}', newname))

        label = re.findall('[a-zA-Z]{2,4}',newname)[0]
        number = re.findall('[0-9]{3,4}', newname)[0]
        label = str.upper(label)
        # print(label)
        print(str(label+"-"+number.__str__()))

        # print('oldname: ' + oldname)
        # print('newname: ' + newname)
        # print('')

        try:
            os.rename(oldname, newname)
            count += 1
        except FileExistsError as e:
            print("File Exist")

print(count.__str__() + ' 건이 처리되었습니다.')
