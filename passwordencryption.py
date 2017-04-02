'''
    Functions will
    - generate a password
    - encrypt a password
    - verify an encrypted password.
    
    Prereq
    ------
    - pip install passlib
    
    Algorithm
    ---------
    Choice: pbkdf2, as recommended by NIST:
        http://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf
'''

### Import needed module(s)
import random, string
from passlib.hash import pbkdf2_sha256

### Defining our functions
def genpwd(length=8,chars=string.ascii_uppercase+string.ascii_lowercase+string.digits+"#$%&@!?"):
    '''
    Generates a password. Takes 2 variables:
        length : the length of the generated password
        chars : the characters from which the password is constructed
    '''
    pwd=""
    for i in range(length):
        pwd+=chars[random.randint(0,len(chars)-1)]
    return pwd

def encrypt_pass(password="P@ssw0rd"):
    '''
    Encrypts a given password. Uses the pbkdf2 algorith.
    Uses rounds of 400000, with a salt size of 32.
    Takes 1 variable:
        password
    '''
    return pbkdf2_sha256.hash(password, rounds=400000, salt_size=32)

def check_pass(password="P@ssw0rd",hashstring="$pbkdf2-sha256$200000$tnYupZTSOmdMyZkzpvQ.J4Sw1przfk.p1RrDuHfu/b8$.bl8AmU0RCOkZdkon3Cu6j/nPAdMkI.0MZiNzhRVf78"):
    '''
    Verifies if a password matches a hash.
    Takes 2 variables:
        password
        hashstring
    Uses the pbkdf2 algorithm
    '''
    return pbkdf2_sha256.verify(password, hashstring)




