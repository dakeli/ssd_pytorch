import os
import shutil

##################移动文件##################
file = r"D:\two_cluster_li"
dst = r"D:\two_cluster_zhenzhunaicha"

files = [obj for obj in os.listdir(file) if 'zhenzhunaicha' in obj]
for file_ in files:
    print(file_)
    shutil.move(os.path.join(file + '\\' + file_), os.path.join(dst))
    # os.rename(os.path.join(file + '\\' + file_), os.path.join(file + '\\' + file_.replace('|', '-')))
    # sub = [sub for sub in os.listdir(file + '\\' + file_)]
    # for sub_ in sub:
    #     shutil.move(os.path.join(file+'\\'+file_+'\\'+sub_), os.path.join(dst))


##########################################


filepath = r"C:\Users\dake\Desktop\tx"
dstpath = r'C:\Users\dake\Desktop\New folder'

filename = [filename for filename in os.listdir(filepath)]
for file_name in filename:
    subfile =[subfile for subfile in os.listdir(filepath+'\\'+file_name)]
    for sub_file in subfile:
        print(file_name+'__'+sub_file)
        # xml = filepath+'\\'+sub_file[:-4]+'.xml'
        # new_xml = dstpath+'\\'+file_name+'\\'+sub_file[:-4]+'.xml'
        # shutil.copy(xml, new_xml)


        # shutil.copyfile(os.path.join(filepath, file_name+'\\'+sub_file), os.path.join(dst))
        # 重命名
        os.rename(os.path.join(filepath, file_name+'\\'+sub_file), os.path.join(filepath, file_name+'\\'+file_name+"----"+sub_file))
        # 剔除多加的重名
        # os.rename(os.path.join(filepath, file_name+'\\'+sub_file), os.path.join(filepath, file_name+'\\'+sub_file.split('----')[-1]))