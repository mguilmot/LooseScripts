'''
    Query AD groups based on arguments given on the commandline
    Ex: AD_QueryGroups.py adgroup* (where adgroup is the part of the name of the AD group you wish to query)
    
    Uses: 
    - pyad:
        pip install https://github.com/zakird/pyad/archive/master.zip
        (Also needs pypiwin32)
'''

import sys
from pyad import *

try:
    groupstring = sys.argv[1]
except IndexError:
    raise IndexError("You should give me an argument like 'Adgr*'")

q = adquery.ADQuery()
q.execute_query(
    attributes = (["CN"]),
    where_clause = "CN = '" + groupstring +"'"
)

for row in q.get_results():
    # prints the group name
    print (row["CN"])