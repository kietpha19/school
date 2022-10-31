input_file = open('input_RPN.txt', 'r')
operators = "+-*/"
syntax_error = "syntax errors! not a valid RPN"

#this is scanning phase, scanning to check if there is any invalid character
def check_line(line):
    print(line)
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
    stack = []
    for c in line:
        if '0' <= c <= '9':
            stack.append(float(c))
        else:
            if len(stack) < 2:
                return syntax_error
            operand = c
            n1 = stack.pop()
            n2 = stack.pop()
            n = calculate(n1, n2, operand)
            stack.append(n)
    if len(stack) > 1:
        return syntax_error
    return stack.pop()

while (line := input_file.readline().rstrip()):
        if not check_line(line):
            print(syntax_error)
        else:
            result = parse_RPN(line)
            print(result)
        print("\n")