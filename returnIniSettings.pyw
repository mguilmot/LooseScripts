''' 
    Script that will return all the keys and values of a 
    chosen ini (or other text) file via a dictionary

    Example Usage:

    myinifile.ini contains:

    [GENERAL]
    windowTitle=Test Window Title
    progName=Test program
    progVersion=1.0

    python script contains:

    settingsDict=returnIniSettings('myinifile.ini')

    progName = settingsDict['progName']
    progVersion = settingsDict['progVersion']
    windowTitle =  settingsDict['windowTitle']
'''

def returnIniSettings(filename='settings.ini'):
    '''
        Expects a plain text ini file as argument. 
        Default filename = settings.ini
        returns every setting in format key=value via a dictionary
        Ignores every non 'key=value' line
    '''

    import os
    if not os.path.isfile(filename):
        err = "Error with file: " + filename + ". It does not exist."
        raise FileExistsError(err)

    settingsDict = {}

    def gen_readfile(f):
        '''
            Generator which returns line per line.
            Expects an open("file") object as input
        '''
        for line in f:
            if line.startswith("#") or line.startswith("[") or line.startswith("\n") or "=" not in line:
                continue
            else:
                yield line

    with open(filename,"r") as f:
        for line in gen_readfile(f):
            key = line.split("=")[0]
            value = line.split("=")[1].strip("\n")
            settingsDict[key]=value

    return settingsDict

# Test
# print(returnIniSettings(filename="settings.ini"))