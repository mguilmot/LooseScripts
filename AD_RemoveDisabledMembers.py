'''
    Will remove disabled users from AD groups it is member of.
    Requires input file in.csv
    Will not give back errors.
'''

### Modules
import logging
from pyad import *

### Variables
fileName_in = "in.csv"      # input filename
hasheader = True            # True if the file has a header line we should ignore
iscsv = True                # True if the input file is a CSV file
iscsv_userNamefield = 0     # Which field in your CSV file contains the userName (first field = 0!)
checked = {}                # dictionary, we don't need to check users twice

### Functions
def readFile(fileName=fileName_in,checked=checked,hasheader=hasheader,iscsv=iscsv,iscsv_userNamefield=iscsv_userNamefield):
    '''
        Yields every line that is not empty, and is not a comment (#)
        Ignores lines we already checked.
    '''
    with open(fileName,"r") as f:
        for num,l in enumerate(f):
            line = l.strip("\n")
            line.strip()
            if line.startswith("#") or len(line)<2 or ( num == 0 and hasheader == True ):
                continue
            else:
                if iscsv == True:
                    line = line.split(",")[iscsv_userNamefield]
                if line in checked:
                    continue
                else:
                    checked[line]=True
                    yield line

def remUser(userName="Administrator"):
    '''
        Will remove the users from their AD groups if they are disabled.
        Returns 0 if:
                    - user is enabled
                    - user is disabled, and removed from groups
    '''
    try:
        disabledlist=[514,546,66050,66082,262658,262690,328194,328226]
        userObj = pyad.aduser.ADUser.from_cn(userName)
        if userObj.get_attribute("userAccountControl")[0] in disabledlist:
            groups = userObj.get_attribute("memberOf")
            for group in groups:
                groupName = group.split(",")[0][3:]
                grpObject = pyad.adgroup.ADGroup.from_cn(groupName)
                try:
                    grpObject.remove_members(userObj)
                except Exception as e:
                    # ignore groups we do not have access to.
                    #logging.exception(e)
                    pass
            return 0
        else:
            # User is enabled, nothing to do
            pass
        return 0
    except Exception as e:
        # Error with user in AD, nothing to do
        # logging.exception(e)
        return 1

if __name__ == "__main__":
    # Read the file, remove users from groups.
    for userName in readFile(fileName=fileName_in):
        remUser(userName=userName)

