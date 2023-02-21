# -*- coding: utf-8 -*-
"""
Backup files in folder
auther: p1xckha
"""

import os, zipfile

def backupToZip(folder, extension=None):
    '''
    Backup the files in folder as the zip file.
    
    for example:
        backupToZip("C:\\python", extension="py")
        
    then, the backup file was saved like 'C:\\python.zip'
    python.zip include python files only, because extension was specified.
    '''
    
    first = os.getcwd() # come back here at the end
    
    # prepare to put folder in the zip file
    os.chdir(folder)
    os.chdir('../') 
    relPathToFolder = os.path.realpath(folder)
    
    # determine the backup zip filename
    num = 1
    while True:
        zipFilename = os.path.basename(folder) + '_' + str(num) + '.zip'
        if not os.path.exists(zipFilename):
            break
        num += 1
    
    # create the backup zip file
    print("creating %s..." % (zipFilename))
    backupZip = zipfile.ZipFile(zipFilename, "w")
    
    # walk through the folder and add files to the zip file
    for foldername, subfoldernames, filenames in os.walk(relPathToFolder):
        '''
        foldername: relpath in this case 
        subfolders: list of subfoldername (not used in this program)
        filenames: list of filename
        '''
        foldername = os.path.relpath(foldername)
        backupZip.write(foldername)
        newBase = os.path.basename(folder) + '_'
        for filename in filenames:
            if filename.startswith(newBase) and filename.endswith(".zip"):
                continue
            
            if extension is None or len(extension) == 0:
                backupZip.write(os.path.join(foldername, filename))
            elif filename.endswith("." + extension):
                backupZip.write(os.path.join(foldername, filename))
    backupZip.close()
    print("Done")
    os.chdir(first)

if __name__ == "__main__":
    path = os.getcwd()
    backupToZip(path, "py")
    
