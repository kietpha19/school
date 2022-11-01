#name: Hoang Anh Kiet Pham
#ID: 1001904809
#date: 
#OS: Mac OS

input_file = open('input_RPN.txt', 'r')
operators = "+-*/"
syntax_error = "syntax errors! not a valid RPN"
sematic_error = "sematic errors! can't evaluate RPN"

#this is scanning phase, scanning to check if there is any invalid character
def check_line(line):
    if line[0] < '0' or  '9' < line[0]:
        return 0
    for i in range(1, len(line)):
        if (line[i] < '0' or  '9' < line[i]) and (line[i] not in operators) and line[i] != ' ':
            return 0
    return 1

def calculate(n1, n2, operand):
    if operand == '+':
        return n1+n2
    if operand == '-':
        return n1-n2
    if operand == '*':
        return n1*n2
    if operand == '/':
        return n1/n2

def parse_RPN(line):
    line = line.split(' ')
    if len(line) == 1:
        line = [c for c in line[0]] # to handle if input without space
    stack = []
    for c in line:
        if c not in operators:
            stack.append(float(c))
        else:
            if len(stack) < 2:
                return sematic_error
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
        RPN = line.split(' ')
        if len(RPN) == 1:
            RPN = [c for c in RPN[0]]
        print("RPN: " + ' '.join(RPN))
        if not check_line(line):
            print(syntax_error)
        else:
            result = parse_RPN(line)
            print("result: " , result)
        print("\n")