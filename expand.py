from math import comb

def expand(s):
    s = s.replace('(','')
    s = s.replace(')','')

    for i in range(len(s)):
        if s[i].isalpha():
            variable = s[i]
            e = i
            if i == 0:
                a = 1
            elif i == 1 and s[i-1] == '-':
                a = -1
            else:
                a = eval(s[:i])
        if s[i] == '^':
            n = eval(s[i+1:])
            b = eval(s[e+1:i])

    final = ''
    c = 0
    z = n

    while n >= 0:
        if n == 1:
            exp = ''
        else:
            exp = '^' + str(n)
        coef = comb(z, c) * (a ** n) * (b ** c)
        if coef != 0:
            if str(coef)[0] == '-':
                if abs(coef) == 1 and n > 0:
                    final += '-' + variable + exp
                elif n > 0:
                    final += str(coef) + variable + exp
                else:
                    final += str(coef)
            else:
                if abs(coef) == 1 and n > 0:
                    final += '+' + variable + exp
                elif n > 0:
                    final += '+' + str(coef) + variable + exp
                else:
                    final += '+' + str(coef)
        n -= 1
        c += 1
    else:
        if final[0] == '-':
            return final
        else:
            return final[1:]