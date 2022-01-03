integers = ['0','1','2','3','4','5','6','7','8','9','n']

def solve_parenthesis(eq):
    for i in range(len(eq)):
        if eq[i] == '(' : pos1 = i
        if eq[i] == ')':
            pos2 = i
            return eq[:pos1]+solv_par(eq[pos1+1:pos2])+eq[(pos2+1):]
    return solv_par(eq)

def op_numbers(eq,i):
    left_bound = len(eq)
    right_bound = 0
    num_l = num_r = ''
    for j in range(i+1,len(eq)):
        if eq[j] in integers :
            num_r = num_r + eq[j]
            if j > right_bound : right_bound = j
        else:
            break;
    for j in reversed(range(0,i)):
        if eq[j] in integers :
            num_l = num_l + eq[j]
            if j < left_bound : left_bound = j
        else:
            break;
    return left_bound,right_bound,num_l[::-1],num_r

def find_negative(eq):
    for i in range(len(eq)):
        if eq[0] == '-':
            return 'n'+eq[(i+1):]
        if eq[i] == '-' and integers.count(eq[i-1]) == 0:
            return eq[:i]+'n'+eq[(i+1):]
    for i in range(len(eq)):
        if eq[i] == 'n' and eq[i+1] == 'n':
            return eq[:i]+eq[(i+2):]
    return eq

def is_product_positive(num_l,num_r):
    if ('n' in num_l) != ('n' in num_r):
        return False
    else:
        return True
    
def without_n(num):
    return num.replace('n','')

def calc_negative(num_l,num_r):
    if ('n' in num_l):
        l_int=int('-'+num_l[1:])
    else:
        l_int=int(num_l)
    if ('n' in num_r):
        r_int=int('-'+num_r[1:])
    else:
        r_int=int(num_r)
    return find_negative(str(l_int-r_int))
    #return l_int,r_int
    
def calc_positive(num_l,num_r):
    if ('n' in num_l):
        l_int=int('-'+num_l[1:])
    else:
        l_int=int(num_l)
    if ('n' in num_r):
        r_int=int('-'+num_r[1:])
    else:
        r_int=int(num_r)
    return find_negative(str(l_int+r_int))
    #return l_int,r_int
    
def mul_div(eq):
    while eq != find_negative(eq):
        eq = find_negative(eq)
    for i in range(len(eq)):
        if eq[i] == 'x':
            lb,rb,num_l,num_r = op_numbers(eq,i)
            if is_product_positive(num_l,num_r):
                return eq[:lb]+str(int(without_n(num_l))*int(without_n(num_r)))+eq[rb+1:]
            else:
                return eq[:lb]+'n'+str(int(without_n(num_l))*int(without_n(num_r)))+eq[rb+1:]
        if eq[i] == '/':
            lb,rb,num_l,num_r = op_numbers(eq,i)
            if is_product_positive(num_l,num_r):
                return eq[:lb]+str(int(int(without_n(num_l))/int(without_n(num_r))))+eq[rb+1:]
            else:
                return eq[:lb]+'n'+str(int(without_n(num_l))/int(without_n(num_r)))+eq[rb+1:]
    return eq

def add_sub(eq):
    while eq != find_negative(eq):
        eq = find_negative(eq)
    for i in range(len(eq)):
        if eq[i] == '+':
            lb,rb,num_l,num_r = op_numbers(eq,i)
            return eq[:lb]+calc_positive(num_l,num_r)+eq[rb+1:]
        if eq[i] == '-':
            lb,rb,num_l,num_r = op_numbers(eq,i)
            return eq[:lb]+calc_negative(num_l,num_r)+eq[rb+1:]
    return eq

def solv_par(eq):
    while eq != mul_div(eq):
        eq = mul_div(eq)
    while eq != add_sub(eq):
        eq = add_sub(eq)
    return eq

def solve(eq):
    while eq != solve_parenthesis(eq):
        eq = solve_parenthesis(eq)
    if 'n' in eq:
        eq = '-'+eq[1:]
    return eq