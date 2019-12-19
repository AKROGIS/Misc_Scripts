import os
with open(r'C:\tmp\list2.txt', 'w') as outfile:
    for (root,dirs,files) in os.walk(r'T:\PROJECTS\AKR\FMSS\TRAILS\Data\DENA\2015_FMSSMapping\SavageAlpine'):
        # print(root)
        for name in files:
            ext = name[-4:].lower()
            # print(ext)
            if ext == '.jpg' or ext == 'jpeg':
                outfile.write(root + ',' + name + '\n')

