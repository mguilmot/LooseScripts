'''
Generates an Excel (2010) file from CSV
Uses the openpyxl module : https://openpyxl.readthedocs.io/en/default/
    Install it via 'pip install openpyxl'
'''

### Modules
import csv, openpyxl

### Variables
f_in = "c:\\temp\\in.csv"           # input file
f_out = "c:\\temp\\out.xlsx"        # output file
delimiter=","                       # delititer the csv file uses. Standard = ",". Use "\t" for tab

### Function(s)
def writeXl(f_in=f_in,f_out=f_out,delimiter=delimiter):
    '''
        Converts our CSV file to XLSX format
    '''
    print("Starting conversion from CSV to xlsx")
    print()
    
    # Opening new excel file
    wb = openpyxl.Workbook()
    ws = wb.active

    with open(f_in) as f:
        # Create the excel from csv
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            ws.append(row)
        # Set the column widths
        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
        for col, value in dims.items():
            ws.column_dimensions[col].width = value
    
    # Saving the file
    wb.save(f_out)
    print("Done")
    print()

### Example
# writeXl(f_in="c:\\temp\\meh.csv",f_out="c:\\temp\\meh.xlsx",delimiter="\t")

