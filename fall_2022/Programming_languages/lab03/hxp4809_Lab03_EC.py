#name: Hoang Anh Kiet Pham
#ID: 1001904809
#date:
#OS: Mac OS

'''
README NOTES

added operators:
 ^: power
 %: modulo division
 -: unary negative (input must be in correct format, has space between number and operaotr)
 eg: 8 + -7 or -7 + 3

 - my program can also use different bracket such as {}, [], or ()
 - my prgram can also handle number with multiple digit as long as it input as correct format (space in between)
 - notes that if the input enter without space between numbers and operator, it will assume as single digit number
 also notes that the input must be either have space between ALL of them, or have NO space at all; 
 otherwise the program will crash or print out the wrong output. 
 - I didn't have enought time to handle this edge case, right now I'm simply using a work-around method
'''


input_file = open('input_RPN_EC.txt', 'r')
all_operators = "+-*/%^"
left_associate_operators = "+-*/%"
right_associate_operators = "^"

digits = "0123456789"
opened_bracket = "{[("
closed_bracket = "}])"
bracket_map = {
    '}' : '{',
    ']' : '[',
    ')' : '('
}

syntax_error = "syntax errors! not a valid algebra expression"
sematic_error = "sematic errors! can't convert to RPN"
RPN_error = "sematic errors! can't evaluate RPN"


#this is scanning phase, scanning to check if there is any invalid character
def check_line(line):
    if (line[0] not in digits) and (line[0] not in opened_bracket) and (line[0] != '-'):
        return 0
    for i in range(1, len(line)):
        if (line[i] not in digits) and (line[i] not in all_operators) \
        and (line[i] != ' ') and (line[i] not in opened_bracket) and (line[i] not in closed_bracket): 
            return 0
    return 1

def getPrecedence(c):
    if c== '+' or c == '-':
        return 1
    elif c == '*' or c == '/':
        return 2
    elif c == '%':
        return 3
    elif c == '^':
        return 4
    else:
        return -1

#utilize Shunting Yard Algorithm
def convert_to_RPN(line):
    line = line.split(' ')
    if len(line) == 1: #to handle input with no space
        line = [c for c in line[0]]
    RPN = []
    stack = []

    for c in line:
        if (c not in all_operators) and (c not in opened_bracket) and (c not in closed_bracket):
            RPN.append(c)
        elif c in opened_bracket:
            stack.append(c)
        elif c in closed_bracket:
            while stack:
                operand = stack.pop()
                if operand in opened_bracket:
                    if bracket_map[c] != operand: #make sure two brackets are matched
                        return -1.1
                    else:
                        break 
                elif not stack: #since c is a closed bracker, there has to be a opened bracket
                    return -1.1
                else:
                    RPN.append(operand)
        elif c in left_associate_operators:
            while stack and (getPrecedence(c) <= getPrecedence(stack[-1])):
                RPN.append(stack.pop())
            stack.append(c)
        elif c in right_associate_operators:
            stack.append(c)
    
    while stack:
        c = stack.pop()
        if c in opened_bracket:
            return -1.1
        RPN.append(c)
    
    return RPN

def calculate(n1, n2, operand):
    if operand == '+':
        return n1+n2
    if operand == '-':
        return n1-n2
    if operand == '*':
        return n1*n2
    if operand == '/':
        return n1/n2
    if operand == '%':
        return n1%n2
    if operand == '^':
        return n1**n2

def parse_RPN(RPN):
    stack = []
    for c in RPN:
        if (c not in all_operators):
            stack.append(float(c))
        else:
            if len(stack) < 2:
                return RPN_error
            operand = c
            n2 = stack.pop()
            n1 = stack.pop()
            if operand == "/" and n2 == 0:
                return "can't be divided by 0"
            n = calculate(n1, n2, operand)
            stack.append(n)
    if len(stack) > 1:
        return sematic_error
    return stack.pop()

while (line := input_file.readline().rstrip()):
        print("algebra expression: " + line)
        if not check_line(line):
            print(syntax_error)
        else:
            RPN = convert_to_RPN(line)
            if (RPN == -1.1):
                print(sematic_error)
            else:
                print("RPN: " , ' '.join(RPN))
                result = parse_RPN(RPN)
                print("result: " , result)
            
        print("\n")