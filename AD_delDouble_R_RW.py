'''
    After finding the doubles, we read them from the CSV file
    
    Wrote it because I needed it, removing users from hundreds of AD groups.
    If you want to use this script, you will probably need to adapt it to your needs.
    Running this script might be safe: set dryRun to True!
    
    Prereq: expects a CSV file in this format:
    
    adgroup1,adgroup2,aduser1, <-- last comma is important
    script will remove aduser1 from adgroup1
    
    If you only want to provide 1 adgroup to remove from, you should adapt :
    
    rowData.append(row[0]) <-- stays
    rowData.append(row[2:-1]) <-- becomes rowData.append(row[1:-1])
     
    Modules needed:
    pywin32 for your specific Python version:
        https://sourceforge.net/projects/pywin32
    pyad by Zakir Durumeric:
        pip install https://github.com/zakird/pyad/archive/master.zip
        Documentation on pyad webpage: https://zakird.com/pyad/index.html
'''

### Modules we need
import os, csv, time
from pyad import *

### Variables
fileName = "c:\\temp\\out.csv"              # File containing the data
csvDelimiter = ","                          # Delimiter in the CSV file
csvHeader = False                           # Does the CSV file contain a header line
start_time = time.time()                    # Obvious
dryRun = False                              # Do you want to test what will happen == True

### Check if input file(s) exists
if (os.path.isfile(fileName))==False:
    raise FileExistsError ("Make sure %s exists" % fileName)

### Functions
def spitData(fileName=fileName,csvDelimiter=csvDelimiter,csvHeader=csvHeader):
    '''
        Reads the CSV data
        Returns the data in list format: [[adgroup],[member,member,member]]
    '''
    
    with open(fileName) as f:
        reader = csv.reader(f,delimiter=csvDelimiter)
        for num, row in enumerate(reader):
            rowData = []
            if num == 0 and csvHeader == True:
                continue
            else:
                rowData.append(row[0])
                rowData.append(row[2:-1])
                yield rowData

def delMember(member,group):
    '''
        Removes the AD user from the AD group
        Expects the member and group in str format
        Returns a str
    '''
    try:
        usrObj = pyad.aduser.ADUser.from_cn(member)
        grpObj = pyad.adgroup.ADGroup.from_cn(group)
        grpObj.remove_members(usrObj)
        return "Removed: " + member + " from " + group
    except:
        return "Error with " + member + " in " + group

def delMember_dryRun(member,group):
    '''
        If you want to test what would happen. For testing CSV
    '''
    return "Removed: " + member + " from " + group
        
groupData = (groupData for groupData in spitData())

for information in groupData:
    group = information[0]
    members = information[1]
    print("Group: ",group)
    for member in members:
        print(delMember(member=member,group=group))
    print()

print("Execution time: --- %s seconds ---" % '{:02.2f}'.format((time.time() - start_time)))

