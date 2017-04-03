'''
    Will check if users are both in read and write access groups in ActiveDirectory
    
    Wrote it because I needed to check for users having both RO and RW access in thousands of AD groups.
    If you want to use this script, you will probably need to adapt it to your needs.
    Running this script is safe: it only gets out information, does not remove or change data in AD
    
    Prereq: both groups should have the same prefix, with the suffix different for R or RW groups
    Ex:
        RO: adgroupName-Usr
        RW: adgroupName-Adm
    
    FileName should contain 1 adgroup per line, plain text format. If using a CSV, you should adapt outputlines(f)
    
    Modules needed:
    pywin32 for your specific Python version:
        https://sourceforge.net/projects/pywin32
    pyad by Zakir Durumeric:
        pip install https://github.com/zakird/pyad/archive/master.zip
        Documentation on pyad webpage: https://zakird.com/pyad/index.html
'''

### Variables
# Filenames we will use
# Lenght of the suffix of the AD groups we will check. In our example our suffix is "-Adm" or "-Usr" == 4
# Suffixes we will ignore, if any. If none use ""
fileName = "c:\\temp\\in.txt"
fileName_out = "c:\\temp\\uit.txt"
suffixlength="4"
suffixignore="-Share"

### Modules we need
import os
from pyad import *

### Check if input file exists
if (os.path.isfile(fileName))==False:
    raise FileExistsError ("Make sure c:\temp\in.txt exists")
    
### Helper functions
def allGroups(fileName=fileName):
    '''
    Getting all the AD groups, sorted, in a list
    '''
    def outputlines(f):
        for line in f:
            if line.startswith("#") or len(line)<2:
                continue
            else:
                yield line.strip("\n")

    with open(fileName) as f:
        lst = [line for line in outputlines(f) if not line.endswith(suffixignore)]
        lst = sorted(lst,key=lambda x:x.split("-")[:-1])
        return lst

def getMembers(groupName):
    '''
    Getting all the members of our AD groups, in a list. Returns an error if group does not exist
    '''
    try:
        GN = pyad.adgroup.ADGroup.from_cn(groupName)
        members = pyad.adgroup.ADGroup.get_members(GN,recursive=False, ignoreGroups=False)
        return [str(member).split(",")[0][12:] for member in members]
    except:
        # Group does not exist
        return ["_Error_"]

def combineGroupMembers(groupName):
    '''
    Combining all AD groups and their members, in a tuple, in format:
    ("groupName",['member1','member2'])
    ''' 
    members = getMembers(groupName)
    if len(members)==0:
        result = (groupName,[])
    else:
        if members[0] != "_Error_":
            result = (groupName,members)
        else:
            result = ("_Error_","_Error_")
    return result
  
def allCombinations(allGroups):
    '''
    Returning all the combinations as a list, stripped from error entries
    '''
    lst=[combineGroupMembers(groupName) for groupName in allGroups]
    while ('_Error_', '_Error_') in lst:
        lst.remove(("_Error_", "_Error_"))
    return lst

def runItAll(suffixlength=suffixlength):
    '''
    Function that is acutally running all our other functions, getting info we need.
    Returning a string with information about groups having double entries.
    
    Example output:
    
    Found double entries
    
    Doubles for: adgroup1 & adgroup2
    aduser1
    aduser2
    '''
    lstAllDoubles = []
    
    for num,combination in enumerate(allCombinations(allGroups())):
        # combination = (groupname,[members])
        groupNameShort = combination[0][:-int(suffixlength)]
        groupName = combination[0]
        members = combination[1]
        
        # Ignore the first num, as there is nothing to compare
        # Find intersecting members, add them to lstAllDoubles
        if num>0:
            if prevgroupNameShort == groupNameShort:
                intersection = list(set.intersection(set(members),set(prevmembers)))
                if len(intersection>0):
                    lstAllDoubles.append(([groupName,prevgroupName],lst))
        
        # Setting "previous" entries, to compare
        prevgroupName = groupName
        prevgroupNameShort = groupNameShort
        prevmembers = members

    if len(lstAllDoubles)>0:
        # If lstAllDoubles has entries, we have doubles. Setting result accordingly
        text = "Found double entries"
        text += "\n\n"
        for double in lstAllDoubles:
            text += "Doubles for: " + str(double[0][0] + " & " + str(double[0][1]))
            text += "\n"
            for member in double[1]:
                text += str(member)
                text += "\n"
            text += "\n"
    else:
        text = "No doubles found."
    
    return text

'''
Check for doubles, output to file
'''
with open(fileName_out,"w") as f:
    f.write(runItAll())


