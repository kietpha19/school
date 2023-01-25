from collections import deque
input_file = open('input.txt', 'r')
special_char = {'{', '}', '\"', '/', "\n"}
q = deque()
depth = 0
s = ""

while 1:
    c = input_file.read(1)
    if not c: break
    
    if c not in special_char:
        s += c
    else:
        if c == '\"':
            s += c
            c = input_file.read(1)
            while c != '\"':
                s += c
                c = input_file.read(1)
            s+= c
        elif c == "/":
            s += c
            c = input_file.read(1)
            if c != "/":
                print("syntax error, not recognize \"/\" ")
                exit(-1)
            else:
                s+= c
                c = input_file.read(1)
                while c and c != "\n":
                    s += c
                    c = input_file.read(1)
        elif c == '{':
            s = s.strip()
            if s: q.append(s)
            s = ""
            q.append(c)
            
            l = q.popleft()
            while l != '{':
                print(str(depth) + (depth+1)*"\t" + l)
                l = q.popleft()
            depth +=1
            print(str(depth) + (depth)*"\t" + l)
        elif c == "}":
            if depth == 0:
                print("syntax error, extra closed bracket } ")
                exit(-1)
            s = s.strip()
            if s: q.append(s)
            s = ""
            q.append(c)
            l = q.popleft()
            while l != '}':
                print(str(depth) + (depth+1)*"\t" + l)
                if not q:
                    print("missing closing bracket } ")
                    exit(-1)
                l = q.popleft()
            print(str(depth) + (depth)*"\t" + l)
            depth -=1
  
        if c == "\n" or not c:
            s = s.strip()
            if s: q.append(s)
            s = ""

while q:
    l = q.popleft()
    print(str(depth) + (depth+1)*"\t" + l)


    