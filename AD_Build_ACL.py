'''
    Building access list based on AD groups
    First version, working with log files as output, then reading them to build the ACL
    Will adapt later with lists and dicts
'''

import os, csv, time, random, shutil
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from pyad import *

### Vars
fileName = "c:\\temp\in.txt"                            # Filename containing the AD groups we should check
fileName_csv = "c:\\temp\out.csv"                       # Output CSV filename
fileName_xl = "c:\\temp\\out.xlsx"                      # Output Excel filename
start_time = time.time()                                # Start time
suffixignore="-share"                                   # Suffix of AD groups we should ignore
header_row = ['Access List','User ID']                  # Header row1 for our CSV file
header_row2 = ["Group description","Group name"]        # Header row2 for our CSV file
delimiter = ","                                         # Delimiter for our CSV file
lstUsers=[]                                             # Placeholder
dictAllUsers = {}                                       # Placeholder

def genFolderName(num=18):
    '''
        Generates a foldername to store our temporary log files in.
        Folder will be deleted after use.
    '''
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    folderName = "_"
    for i in range(num):
        ran = random.randint(0,len(chars)-1)
        folderName += chars[ran]
    return folderName

folderName = "c:\\temp\\" + str(genFolderName())

# Create folder if it does not exist yet
if not os.path.isdir(folderName):
    os.makedirs(folderName)

def countLenItems(lst):
    t=0
    for c in lst:
        t += len(c)
    return t
    
def countLines(fileName=fileName):
    '''
        Counting the lines in our log files
    '''
    c = 0
    with open(fileName) as f:
        for l in f:
            line = l.strip("\n")
            if line.startswith("#") or len(line)<2:
                continue
            else:
                c += 1
    return c    
    
def printmsg(text="",lines=False):
    '''
        Simple function to print the text we want as output.
    '''
    c = len(text)
    l = c*"-"
    if lines == True:
        return text + "\n" + l + "\n"
    else:
        return "\n" + text + "\n"

def readFile(fileName=fileName,suffixignore=suffixignore):
    '''
        Reads the input file, returns them 1 by 1
        Empty lines and lines starting with # are ignored
    '''
    
    with open(fileName) as f:
        for l in f:
            line = l.strip("\n").lower()
            if (line.startswith("#") or len(line)<2) or (suffixignore!="" and line.endswith(suffixignore)) or (suffixignore!="" and line.endswith(suffixignore.lower())):
                continue
            else:
                yield line

def retLogFiles():
    '''
        Returns the logfiles in our folderName\*
    '''
    for part in os.walk(folderName+"\."):
        for file in part:
            if len(file) <2:
                continue
            elif isinstance(file,list):
                for filepart in file:
                    if len(filepart)<2 or os.stat(folderName+"\\"+filepart).st_size == 0:
                        continue
                    else:
                        yield filepart
            else:
                if os.path.isdir(file):
                    continue
                else:
                    yield file

def retUserName(user="Administrator"):
    try:
        userObj = pyad.aduser.ADUser.from_cn(user)
        return userObj.get_attribute("displayName")[0]
    except:
        return ""

def writeCsv(fileName_csv=fileName_csv,delimiter=delimiter,header_row=header_row,header_row2=header_row2,folderName=folderName,dictAllUsers=dictAllUsers):
    '''
        Writes the desired information to CSV file.
    '''
    
    print(printmsg(text="Reading logfiles to generate CSV"))

    with open(fileName_csv,"w") as f:
        writer = csv.writer(f,delimiter=delimiter,dialect="excel",lineterminator="\n")
        
        print(printmsg(text="Generating CSV file."))
        
        # Print header row
        writer.writerow(header_row)
        print(printmsg(text="Getting display names."))
        for user in header_row:
            displayName = retUserName(user)
            if displayName != "":
                header_row2.append(displayName)
        writer.writerow(header_row2)
        # Reading logfiles 1 by 1
        for fn in retLogFiles():
            file = folderName + "\\" + fn
            linetxt = [""] * 2
            #usersinfile = [""] * (countLines(file)-1)
            usersinfile = [""] * len(dictAllUsers)
            for num,line in enumerate(readFile(file)):
                if num == 0:
                    # This is our group description
                    linetxt[0] = line
                    linetxt[1] = fn[:-4]
                else:
                    # These are our users
                    username = line
                    userlocation = dictAllUsers[username.upper()]
                    usersinfile[userlocation]="X"
            writer.writerow(linetxt+usersinfile)
            
        print(printmsg(text="Done. Check " + fileName_csv + " for output."))

def writeLog(groupName,lstUsers=lstUsers):
    '''
        Writes 1 file per AD group as text file.
        Writes:
        - description
        - members (1 per line)
        If no members: file = empty
    '''
    grpObj = pyad.adgroup.ADGroup.from_cn(groupName)
    grpMembers = pyad.adgroup.ADGroup.get_members(grpObj)
    members = [str(member).split(",")[0][12:] for member in grpMembers]
    with open(folderName + "\\" + groupName + ".txt","w") as f:
        if len(members)>0:
            desc = grpObj.get_attribute("description")[0]
            if len(desc)<2:
                desc="No description"
            f.write(desc)
            f.write("\n")
        for member in members:
            if member not in lstUsers:
                lstUsers.append(member)
            f.write(member)
            f.write("\n")

def writeXl(fileName_csv=fileName_csv,fileName_xl=fileName_xl,delimiter=delimiter,folderName=folderName):
    '''
        Converts our CSV file to XLSX format
    '''
    
    numRows = 0
    
    print(printmsg(text="Converting CSV to XLSX"))
    
    wb = openpyxl.Workbook()
    ws = wb.active

    with open(fileName_csv) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            ws.append(row)

        # Setting max width
        dims = {}
        for row in ws.rows:
            numRows += 1
            for cell in row:
                if cell.value:
                    dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
        for col, value in dims.items():
            ws.column_dimensions[col].width = value
        
        # Sorting our columns
        lstCol = list(dims.keys())
        lstCol.sort(key=lambda item: (len(item),item))
        
        # Setting formatting
        print(printmsg(text="Setting formatting in XLSX"))
        for colNum,col in enumerate(lstCol):
            # Running over columns
            if colNum > 1:
                # column width = 3
                ws.column_dimensions[col].width = 3
            for rowNum in range(numRows):
                # Running over rows
                curCell = ws[str(col.upper()) + str(rowNum+1)]
                curCell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                if colNum > 1:
                    # We do not touch the first two columns, borders are already set
                    if rowNum < 2:
                        # Formatting should be: vertical text + all border + center
                        curCell.alignment = Alignment(horizontal='center',text_rotation=90)
                    else:
                        # Formatting should be : all borders + center
                        curCell.alignment = Alignment(horizontal='center')
                
    wb.save(fileName_xl)

    print(printmsg(text="Done. Check " + fileName_xl + " for output."))
    
# Start of our script       
print(printmsg(text="Writing log files with members.",lines=True))

# Writing our temporary log files to folderName
for line in readFile():
    writeLog(line)
    print("Writing",line)
print(printmsg(text="Done."))

# Create dictionary with theire number alphabetically, and add them to our header
allUsers = sorted(lstUsers)

# Since we will not add everything we'll need a puppy integer following our list
puppy = 0
for user in allUsers:
    if not user.startswith("="):
        dictAllUsers[user]=puppy
        header_row.append(user)
        puppy += 1

# Writing our output files
writeCsv()
writeXl()

# Wrapping up
shutil.rmtree(folderName, ignore_errors=True)
print(printmsg(text="Deleting our temporary log files.\nDone."))

# Print execution time
print("Execution time: --- %s seconds ---" % '{:02.2f}'.format((time.time() - start_time)))
print()

