import os
import shutil

jpegfile_path = r"C:\Users\dake\OneDrive\picture\yin_xing"
annotations = r"C:\Users\dake\Desktop\picture_200_200"

# filename = [filename for filename in os.listdir(jpegfile_path)]
# xmlname = [xmlname.split('----')[0] for xmlname in os.listdir(annotations)]
# for file_name in filename:
#     if file_name[:-5] in xmlname:
#         continue
#     else:
#         print(file_name)
#         # shutil.move(jpegfile_path+'\\'+file_name, annotations+'\\'+file_name)

filenames = [filename for filename in os.listdir(jpegfile_path)]
# xmlnames = [xmlname if 'modify' in xmlname else xmlname.replace('modify_J', 'J') for xmlname in os.listdir(annotations) ]
xmlnames = [xmlname for xmlname in os.listdir(annotations) ]
for file_name in filenames:
    num = file_name.split('----')[-1].split('.')[0].split('_')
    x = int(num[0]) - 200
    y = int(num[1]) - 200
    w = int(num[2]) + 400
    h = int(num[3]) + 400
    f_name = file_name.split('----')[0] + '----' + str(x) + '_' + str(y) + '_' + str(w) + str('_') + str(h) + '.png'
    if f_name in xmlnames:
        shutil.copy(annotations+'\\'+f_name, r"C:\Users\dake\OneDrive\picture_200\yin_xing"+'\\'+f_name)
    else:
        print(file_name)
        