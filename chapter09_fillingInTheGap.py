# -*- coding: utf-8 -*-
"""
Renamer

author:p1xckha
"""

import os, shutil, re

class Renamer:
    '''
    rename filenames with continuous integers
    '''
    def __int__(self):
        self.filenames = []
        self._digits = None
    
    def findFiles(self, folder, prefix, extension):
        folder = os.path.abspath(folder)
        filenamesFound = []
        
        for filename in os.listdir(folder):
            if filename.startswith(prefix) and filename.endswith("." + extension):
                filenamesFound.append(os.path.join(folder, filename))
        
        self.filenames = filenamesFound
    
    def createTestFiles(self, folder, filenames):
        folder = os.path.abspath(folder)
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        for filename in filenames:
            path = os.path.join(folder, filename)
            with open(path, "w") as f :
                f.write("Rename me!")
    
    @property
    def digits(self):
        return self._digits
    
    @digits.setter
    def digits(self, digits):
        self._digits = digits
        
    def getFilenames(self):
        return self.filenames
    
    def getNumFiles(self):
        return len(self.filenames)
        
    def getDigits(self):
        return self._digits
    
    def fillZeros(self, number, digits):
        '''
        return number as string filled zeros at its head.
    
        for example:
        if number = 99, digits = 3 , then "099" is returned
        '''
        numstr = str(number)
        if len(numstr) < digits:
            numstr = "0" * (digits - len(numstr)) + str(number) 
        return numstr
    
    def getExtension(self, filename):
        extension = re.search('[a-z]+$', filename).group(0)
        return extension
            
    def rename(self, folder, prefix, extension, digits):
        '''
        rename filenames with continuous integers
        
        ["spam001.txt", "spam02.txt", "spam08.txt"]
        -> ["spam001.txt", "spam002.txt", "spam003.txt"]
        
        Parameters
        ----------
        folder : folder path as string
            folder is relative or absolute 
        prefix : the head of filenames as string
            if prefix is "spam", then filenames are renamed like "spam05.txt"
        extension : as string
            for example, "txt", "jpg", "pdf", etc.
        digits : 
            number of digits in filename string.
            for example, digit is 4, then filenames are renamed like "spam0006.txt"

        Returns
        -------
        None.

        '''
        folder = os.path.abspath(folder)
        self.findFiles(folder, prefix, extension)
        self.digits = digits

        if self._digits < 1 + self.getNumFiles() / 10:
            self._digits = 1 + int(self.getNumFiles()/10)
        
        number = 1
        numstr = ""
        for filename in self.getFilenames():
            numstr = self.fillZeros(number, self.getDigits())
            afterFilename = "%s%s.%s" % (prefix, numstr, extension)
            afterFilename = os.path.join(folder, afterFilename)
            print("Renaming %s to %s" % (filename, afterFilename))
            shutil.move(filename, afterFilename)
            number += 1
        print("Done.")
        
        
if __name__ == "__main__":
    # instantiate
    renamer = Renamer()
    
    # variables
    folder = 'C:\\DeleteMe'
    prefix = "spam"
    extension = "txt"
    digits = 4
    filenames = ['spam001.txt', 'spam010.txt', 'spam099.txt', 'spam005.txt', 'dont_rename_me.txt']
    
    # create test files
    renamer.createTestFiles(folder, filenames)
    
    # rename 
    renamer.rename(folder, prefix, extension, digits)
    

    

