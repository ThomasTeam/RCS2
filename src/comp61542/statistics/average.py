
def mean(X):            #return the average of X
    n = len(X)
    if n > 0:
        return float(sum(X)) / float(len(X))
    return 0


def median(X):          # if  it's odd return the middle element; else, return the average of middle two elements 
    n = len(X)
    if n == 0:
        return 0
    L = sorted(X)
    if n % 2:
        return L[n / 2]
    return mean(L[(n / 2) - 1:(n / 2) + 1])

def mode(X):            #return the most occurred element 
    n = len(X)
    if n == 0:
        return []

    d = {}
    for item in X:
        if d.has_key(item):
            d[item] += 1
        else:
            d[item] = 1

    m = []
    mostFrequent=0
    for key in d.keys():
        if d[key]>mostFrequent:
            m=[]
            m.append(key)
            mostFrequent=d[key]
        elif d[key]==mostFrequent:
            m.append(key)
    return m
    #m = (0, 0)
    #for key in d.keys():
    #    if d[key] > m[0]:
    #        m = {}
    #        m[key]= d[key]
    #    elif d[key] == m[1]:
    #        m[key]= d[key]

    #return [m[0]]       