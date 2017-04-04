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
        
    tested on 650 groups at once: execution time: 180 sec (0.28sec/group)
'''

### Variables
fileName = "c:\\temp\\in.txt"           # input filename
fileName_out = "c:\\temp\\uit.txt"      # plain text output filename
fileName_csv = "c:\\temp\\uit.csv"      # csv output filename
suffixlength="4"                        # Lenght of the suffix of the AD groups we will check. In our example our suffix is "-Adm" or "-Usr" == 4
suffixRO="-Usr"                         # Suffix of the Read Only  AD groups
suffixRW="-Adm"                         # Suffix of the Read+Write AD groups
suffixignore=""                         # Specific suffixes to ignore
dictChecked={}                          # Dictionary we will use to speed things up, do not change this one

### Modules we need
import os, string
from pyad import *

### Check if input file(s) exists
if (os.path.isfile(fileName))==False:
    raise FileExistsError ("Make sure c:\temp\in.txt exists")

### Helper functions
def allGroups(fileName=fileName):
    '''
    Generator, getting all the AD groups, sorted, returning them 1 by 1
    '''
    
    print("Reading input file",fileName)
    
    def outputlines(f):
        for line in f:
            if line.startswith("#") or len(line)<2:
                continue
            else:
                yield line.strip("\n").lower()

    with open(fileName) as f:
        #lst = [line for line in outputlines(f) if not line.endswith(suffixignore)]
        #lst = sorted(lst,key=lambda x:x.split("-")[:-1])
        #return lst
        if suffixignore == "":
            genGroups = sorted((line for line in outputlines(f)),key=lambda x:x.split("-")[:-1])
        else:
            genGroups = sorted((line for line in outputlines(f) if not line.endswith(suffixignore)),key=lambda x:x.split("-")[:-1])
        for group in genGroups:
            yield group

def getMembers(groupName,suffixRO=suffixRO,suffixRW=suffixRW,dictChecked=dictChecked):
    '''
    Getting all the members of our AD groups, in a list. Returns an error if group does not exist
    Checks if "other" group was already checked. If so, and empty: skip it. Should speed up things.
    '''

    print("Getting members for AD group:",groupName)
    
    suffixes=[suffixRO,suffixRW]
    groupNameShort = groupName[:-int(suffixlength)]
    groupNameSuffix = groupName[-int(suffixlength):]
    
    def findMembers(groupName,groupNameShort=groupNameShort):
        try:
            GN = pyad.adgroup.ADGroup.from_cn(groupName)
            members = pyad.adgroup.ADGroup.get_members(GN,recursive=False, ignoreGroups=False)
            result = [str(member).split(",")[0][12:] for member in members]
            dictChecked[groupNameShort] = len(result)
            return result
        except:
            # Group does not exist
            return ["_Error_"]    
    
    if groupNameShort + suffixes[0] == groupName:
        other = groupNameShort + suffixes[0]
    else:
        other = groupNameShort + suffixes[1]
    
    if groupNameShort in dictChecked:
        if dictChecked[groupNameShort]>0:
            # found. Not empty. Adding
            members = findMembers(groupName)
            return members
        else:
            # found. Empty. Skipping
            return []
    else:
        # not found. Adding
        members = findMembers(groupName)
        return members
    
def combineGroupMembers(groupName):
    '''
    Combining all AD groups and their members, in a tuple, in format:
    ("groupName",['member1','member2'])
    ''' 
    members = getMembers(groupName)
    if len(members)==0:
        return (groupName,[])
    else:
        if members[0] != "_Error_":
            return (groupName,members)
        else:
            return ("_Error_","_Error_")
  
def allCombinations(allGroups):
    '''
    Generator returning all the combinations 1 by 1
    '''
    
    print("Generating information about groups.")
    
    lst=(combineGroupMembers(groupName) for groupName in allGroups)
    for combination in lst:
        # If error or empty, we shouldn't be evaluating
        if combination == ("_Error_","_Error_") or combination[1]==[]:
            continue
        else:
            yield combination

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
    
    print("Starting.")
    
    for num,combination in enumerate(allCombinations(allGroups())):
        # combination = (groupname,[members])
        groupNameShort = combination[0][:-int(suffixlength)]
        groupName = combination[0]
        members = combination[1]
        
        # Ignore the first num, as there is nothing to compare
        # Find intersecting members, add them to lstAllDoubles
        if num>0:
            if prevgroupNameShort == groupNameShort:
                print("Comparing", prevgroupName,"with",groupName)
                intersection = list(set.intersection(set(members),set(prevmembers)))
                if len(intersection)>0:
                    lstAllDoubles.append(([groupName,prevgroupName],intersection))
        
        # Setting "previous" entries, to compare
        prevgroupName = groupName
        prevgroupNameShort = groupNameShort
        prevmembers = members
        
    if len(lstAllDoubles)>0:
        textcsv=""
        # If lstAllDoubles has entries, we have doubles. Setting result accordingly
        print()
        print('Found double entries. Check chosen output file(s).')
        print()
        text = "Found double entries"
        text += "\n\n"
        for double in lstAllDoubles:
            text += "Doubles for: " + str(double[0][0] + " & " + str(double[0][1]))
            text += "\n"
            textcsv += str(double[0][0]) + "," + str(double[0][1]) + ","
            for member in double[1]:
                text += str(member)
                text += "\n"
                textcsv += str(member)
                textcsv += ","
            text += "\n"
            textcsv += "\n"
    else:
        print("No doubles found in provided AD groups.")
        text = "No doubles found."
        textcsv = "No doubles found"
    
    return (text,textcsv)

'''
Check for doubles, output to file
'''
import time
start_time = time.time()

run = runItAll()

text,textcsv = run[0],run[1]

if fileName_csv != "":
    with open(fileName_csv,"w") as f:
        f.write(textcsv)

if fileName_out != "":
    with open(fileName_out,"w") as f:
        f.write(text)

print("--- %s seconds ---" % (time.time() - start_time))
