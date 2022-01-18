import copy
accepted_symbols = ['0','1','2','3','4','5','6','7','8','9','+','-','/','x','(',')']
def token_list(eq):
    tokens = []
    num = ""
    for c in eq:
        if c.isdigit():
            num += c
        else:
            if num != "":
                tokens.append(num)
                num = ""
            tokens.append(c)
    if num != "":
        tokens.append(num)
    return tokens

def symbols_valid(eq): #test if symbols are in the allowed list
    eq_part = [symbol for symbol in eq]
    if all(item in accepted_symbols for item in eq_part):
        return True
    else:
        return False

def operators_valid(eq): #test if the operators are on legal positions
    if eq[0]=='x' or eq[0]=='/' or eq[0]=='+': return False
    if eq[len(eq)-1]=='x' or eq[len(eq)-1]=='/' or eq[len(eq)-1]=='+' or eq[len(eq)-1]=='-': return False
    for i in range(1,len(eq)-1):
        if eq[i].isdigit() and (eq[i-1]==')' or eq[i+1]=='('): return False
        if eq[i]=='x' or eq[i]=='/' or eq[i]=='+':
            if not ((eq[i-1].isdigit() or eq[i-1]==')') and (eq[i+1].isdigit() or eq[i+1]=='(')):
                return False
    return True

def check_for_bracket_pairs(eq_check): #test if the brackets are paired
    eq = copy.deepcopy(eq_check)
    eq = token_list(eq)
    brack1 = 0
    brack2 = 0
    for i in range(len(eq)):
        if eq[i] == '(':
            brack1 = i
            for j in range(i,len(eq)):
                if eq[j] == ')':
                    brack2 = j
                    eq[i] = '1'
                    eq[j] = '1'
                    break;
    for i in range(len(eq)):
        if (eq[i] == '(' or eq[i] == ')'):
            return False
    return True

def is_expression_valid(eq): #run all equation validity tests
    if not (symbols_valid(eq) and operators_valid(eq) and check_for_bracket_pairs(eq)):
        return False
    else:
        return True

def is_symbol_num(token):
    return True if any([x.isdigit() for x in token]) else False

def is_token_negative(token):
    return True if any([x=='-' for x in token]) else False

def find_negative(eq): #support for unitary operators
    eq = copy.deepcopy(eq)
    if eq[0] == '-' and not is_token_negative(eq[1]):
        eq[1] = '-'+eq[1]
        return eq[1:]
    if eq[0] == '-' and is_token_negative(eq[1]):
        eq[1] = eq[1][1:]
        return eq[1:]
    return eq

def solve_parenthesis(eq):
    for i in range(len(eq)):
        if eq[i] == '(' : pos1 = i
        if eq[i] == ')':
            pos2 = i
            return eq[:pos1]+solv_par(eq[pos1+1:pos2])+eq[(pos2+1):]
    return solv_par(eq)

def solv_par(eq):
    eq_last_step = []
    while eq != eq_last_step:
        eq_last_step = eq
        eq = one_op(eq)
    return eq

def solve(eq):
    if not is_expression_valid(eq):
        print(eq)
        return "Invalid Expression"
    eq = token_list(eq)
    eq = find_negative(eq)
    eq_last_step = []
    while eq!= eq_last_step:
        eq_last_step = eq
        eq = solve_parenthesis(eq)
    eq[0] = float(eq[0])
    if eq[0].is_integer():
        return int(eq[0])
    else:
        return eq[0]

def one_op(eq):
    eq = find_negative(eq)
    for i in range(len(eq)):
        if eq[i] == 'x':
            result = float(eq[i-1])*float(eq[i+1])
            return eq[:(i-1)]+[result]+eq[(i+2):]
        if eq[i] == '/':
            result = float(eq[i-1])/float(eq[i+1])
            return eq[:(i-1)]+[result]+eq[(i+2):]
    for i in range(len(eq)):
        if eq[i] == '+':
            result = float(eq[i-1])+float(eq[i+1])
            return eq[:(i-1)]+[result]+eq[(i+2):]
        if eq[i] == '-':
            result = float(eq[i-1])-float(eq[i+1])
            return eq[:(i-1)]+[result]+eq[(i+2):]
    return eq
