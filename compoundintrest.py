def calcintrest(base,intrest):
    '''
        Calculates the intrest on a base amount.
        Checks for wrong input
    '''
    try:
        return float(base*intrest)
    except:
        return 0
        
def calcextras(extra,type):
    '''
        Calculates the extras saved in between.
        Checks for wrong input
    '''
    try:
        if type == 'year':
            return extra
        else:
            return extra*12
    except:
        return 0

def calccompound(base=100,intrest=0.01,years=5,periodextra=0,periodtype='year'):
    '''
        expects vars:
        - base (starting amount)
        - intrest (yearly, as float)
        - years (number of years of savings)
        - periodextra (extra amount saved per 'periodtype')
        - periodtype ('month' or 'year'. Everything else will be handled as 'month')
    '''
    try:
        int (base * intrest * years)
        for currentyear in range(years):
            base += calcextras(extra=periodextra,type=periodtype)
            base += calcintrest(base,intrest)
        return '{:02.2f}'.format(base)
    except:
        return ("Error: base should be INT, intrest should be FLOAT, years should be INT")

print(calccompound(base=0,intrest=0.015,years=1,periodextra=1,periodtype='month'))