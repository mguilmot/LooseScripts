'''
    Find prime numbers under certain "number"
'''

def find_deviders(number):
    '''
        Helper function to check how many deviders our number has.
        More than 1 = not prime, and we stop.
    '''
    count=0
    for devider in range(number):
        if devider == 0:
            continue
        if number%devider==0:
            count+=1
            if count > 1:
                return 2
    return count

def find_primes(number):
    '''
        Generator, checking if a number is prime.
        If so, return it.
    '''
    try:
        int(number)
    except:
        return "Error. Number should be type INT"

    passcheck=[0,2,4,5,6,8]
    for num in range(number+1):
        if num > 5 and int(str(num)[-1]) in passcheck:
            continue
        if find_deviders(num) < 2:
            yield num

for i in find_primes(100000):
    print(i)
