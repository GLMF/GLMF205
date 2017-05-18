import os.path 
  
def populate(path, sizeMax):  
    filesList = []  
    for root, dirs, files in os.walk(path):  
        for f in files:  
            filename = os.path.join(root, f)
            if os.path.getsize(filename) > sizeMax:
                cell = 1
            else:
                cell = 0
            filesList.append((filename, cell))
    return filesList

def applyRules(strip):
    current = strip.pop(0)
    if current[1] == 1:
        print('Hit :', current[0])

def detectBigFiles(path, sizeMax=5000):
    strip = populate(path, sizeMax)    
    while strip != []:
        applyRules(strip)


if __name__ == '__main__':
    detectBigFiles('/home')
