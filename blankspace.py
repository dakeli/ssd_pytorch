import os

filepath = r"D:\xml_xifenlei\JPEGImages\xibaowu"
filename = [filename for filename in os.listdir(filepath)]
for file_name in filename:
    if len(file_name.split(' ')) == 2:
        curfilename=file_name.split(' ')[0]+'-'+file_name.split(' ')[1]
        os.rename(os.path.join(filepath, file_name), os.path.join(filepath, curfilename))
        print(curfilename)
