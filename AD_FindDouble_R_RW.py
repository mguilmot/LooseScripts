'''
    Will check if users are both in read and write access groups in AD
    Prereq: both groups should have the same prefix, with the suffix different for R or RW groups
    Ex:
        r : adgroup-Usr
        RW: adgroup-Adm
    Filename should be 1 adgroup per line
    
    Modules needed:
    installs: 
    pywin32:
        https://sourceforge.net/projects/pywin32
    pyad:
        pip install https://github.com/zakird/pyad/archive/master.zip
'''

import os
from pyad import *

useFile = True
fileName = "c:\\temp\\in.txt"
fileName_out = "c:\\temp\\uit.txt"

suffixlength="4" # in our example our suffix is "-Adm" or "-Usr" == 4
suffixignore="-Share"

if (os.path.isfile(fileName))==False:
    raise FileExistsError ("Make sure c:\temp\in.txt exists")
    
def outputlines(f):
    for line in f:
        if line.startswith("#") or len(line)<2:
            continue
        else:
            yield line.strip("\n")

def allGroups(fileName=fileName):
    with open(fileName) as f:
        lst = [line for line in outputlines(f) if not line.endswith(suffixignore)]
        lst = sorted(lst,key=lambda x:x.split("-")[:-1])
        return lst

def getMembers(groupName):
    try:
        GN = pyad.adgroup.ADGroup.from_cn(groupName)
        members = pyad.adgroup.ADGroup.get_members(GN,recursive=False, ignoreGroups=False)
        return [str(member).split(",")[0][12:] for member in members]
    except:
        return ["_Error_"]

def combineGroupMembers(groupName):
    # tupleCombined = ("groupName",['member1','member2'])
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
    lst=[combineGroupMembers(groupName) for groupName in allGroups]
    while ('_Error_', '_Error_') in lst:
        lst.remove(("_Error_", "_Error_"))
    return lst

def runItAll(suffixlength=suffixlength):
    
    lstAllDoubles = []
    
    for num,combination in enumerate(allCombinations(allGroups())):
        # combination = (groupname,[members])

        groupNameShort = combination[0][:-int(suffixlength)]
        groupName = combination[0]
        members = combination[1]
        
        if num>0:
        
            lst = []
            
            if prevgroupNameShort == groupNameShort:
            
                lena = len(prevmembers)
                lenb = len(members)
                
                if lena<lenb:
                    shortest = prevmembers
                    longest = members
                else:
                    shortest = members
                    longest = prevmembers
                
                for member in shortest:
                    if member in longest:
                        lst.append(member)
                
                if len(lst)>0:
                    lstAllDoubles.append(([groupName,prevgroupName],lst))
                    
        prevgroupName = groupName
        prevgroupNameShort = groupNameShort
        prevmembers = members

    if len(lstAllDoubles)>0:
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

with open(fileName_out,"w") as f:
    f.write(runItAll())


