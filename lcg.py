# Fettet, Louis
# Linear Congruential Generator
# 12/10/12

# "Anyone who considers arithmetical methods of producing random digits is, of
#  of course, in a state of sin."
# - John von Neumann

# "Random numbers should not be generated with a method chosen at random."
# - Donald E. Knuth

# The following is my implementation of a linear congruential generator.
# My first implementation used the same numbers as VAX's MTH$RANDOM, and after
# testing these numbers I generated my own variables with some of the other
# functions below.

def lcg(start, end, last):
    """
    Returns a pseudo-random number using the linear congruential recurrence
    relation.
    On the first iteration, it uses the seed pi, and on every following
    iteration it can use the previously generated number as the next seed.
    """
    if last is None:
        x = 3.141592        # i think pi is a pretty cool irrational number
                            #   ti makes circles and doesn't afraid of anything
    else:
        x = last
    # This next part is really important.  The values we choose for the
    # variables makes the difference between creating the perfect generator
    # or repeating the atrocities of the infamous... RANDU.
    a = 3209867             # the "multiplier"; a-1 is divisible by all prime
                            #   factors of m.
    c = 12493               # the "increment" 
    m = 2**80               # the "modulus"; c and m are pairwise coprime.
    # Finally, we plug in these variables into our LCG equation.
    return start+((a*x+c)%m)%end
       
def noCycleTest():
    """
    Tests to see if a number repeats within 65536 iterations.
    Returns True if no cycle occurs; otherwise returns False.
    """
    dic = {}
    last = 3.141592                 # We again use pi as our starting seed. 
    for i in range(65536):  
        last = lcg(0,1,last)        # The previously generated number is used as
        result = (last)             #   the next starting seed.
        if result in dic:
            return False
        else:
            dic[result] = 1
    return True

def uniformityTest():
    """
    Tests the uniformity of the generator on producing integers between 0 and 9.
    Returns a dictionary with integers 0 through 9 along with the amount of
    times each integer occurs.
    """
    dic = {}
    last = 3.141592
    for i in range(65536):
        last = lcg(0,10,last)   # Generates a number between 0 and 10.
        result = int(last)      # Converts the number to an integer for testing.
        if result in dic:
            dic[result] += 1
        else:
            dic[result] = 1
    return dic

def pokerTest():
    """
    Tests the generator by having it produce 'random' card suits (hearts,
    spades, clubs, and diamonds) over 65536 iterations.
    It's a really horrible implementation.
    Like really horrible.
    I feel bad for anyone who has to read this.
    """
    from collections import Counter
    occur = []
    last = 3.141592
    for i in range(65536):
        seq = {}
        for e in range(5):          # There are 5 cards in a hand.
            last = lcg(0,4,last)
            result = int(last)
            if result == 0:
                result = 'h'        # hearts
            if result == 1:
                result = 'd'        # diamonds
            if result == 2:
                result = 's'        # spades
            if result == 3:
                result = 'c'        # clubs
            if result in seq:
                seq[result] += 1
            if result not in seq:
                seq[result] = 1
        occur.append(seq)
    stringlist=[]           
    for i in occur:                 # This was definitely not the best way to
        string = str(i)             # implement this but I'm tired and stuff.
        stringlist.append(string)   
    finaldic = {}                   
    for i in stringlist:
        if i in finaldic:
            finaldic[i]+=1
        else:
            finaldic[i]=1
    for sequence in finaldic:
        print ('{0:35} {1:5}'.format(sequence,finaldic.get(sequence)))
            

# Below are some things I found, modified, and used in generating my initial
# variables for the LCG... theoretically you could use numbers generated from
# the LCG and plug them into these functions to return new parameters to put
# back into the generator.  Not sure how this would affect the quality of the
# 'randomness', but I think it could definitely improve the security of the
# generator, making it more difficult to 'hack' if this were to be used in
# some kind of game or commercial software.

def factor(n):
    if n == 1:
        return [1]
    i = 2
    limit = n**0.5
    while i <= limit:
        if n % i == 0:
            recur = factor(int(n/i))
            recur.append(i)
            return sorted(recur)
        i += 1
    return [n]

def factorPowers(n):
    d = {}
    for i in (factor(n)):
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return d

def isPrime(n):
    if len(factor(n)) == 1:
        return True
    else: return False

def arePairwiseCoprime(s,t):
    for i in factor(s):
        if i in factor(t):
            return False
    return True

def GCD(s,t):
    s = factor(s)
    t = factor(t)
    while len(s) > 0:
        if max(s) in t:
            return max(s)
        else:
            s.remove(max(s))
    return 1
        
    
