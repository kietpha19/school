'''
name: Hoang Anh Kiet Pham
ID: 1001904809
due data: November 30th, 2022
windows 10 , python 3.10.2

this is extra credit, handle escape charater '\' and print output in the formatted way
'''

from collections import deque #use for queue data structure
input_file = open('input_EC.txt', 'r')
special_char = {'{', '}', '\"', '/', "\n"}
q = deque()
depth = 0
s = ""

while 1:
    c = input_file.read(1)
    if not c: break
    
    #as long as the character is not special, we keep adding it to the string
    if c not in special_char:
        s += c
    else: #special character cases
        if c == '\"':
            s += c
            c = input_file.read(1)
            while c != '\"':
                if c == '\\':
                    s+=c
                    c = input_file.read(1)
                s += c
                c = input_file.read(1)
            s+= c
        elif c == "/": #comment out
            s += c
            c = input_file.read(1)
            if c != "/" and c != "*":
                print("syntax error, not recognize \"/\" ")
                exit(-1)
            elif c == "/":
                s+= c
                c = input_file.read(1)
                while c and c != "\n":
                    s += c
                    c = input_file.read(1)
            elif c == "*":
                s+=c
                s = s.strip()
                q.append(s)
                s = ""

                c = input_file.read(1)
                while c and c != "*":
                    s += c
                    c = input_file.read(1)
                if not c:
                    print("syntax error, missing closuse for comment out")
                    exit(-1)
                #handle multiple lines comment
                elif c == "*":
                    s = s.strip()
                    s = s.split('\n')
                    while s:
                        l = s.pop(0)
                        l = l.strip()
                        q.append(l)

                    s = ""
                    s+=c
                    c = input_file.read(1)
                    if c != '/':
                        print("syntax error, not recognize '*' ")
                        exit(-1)
                    else:
                        s+=c
                        q.append(s)
                        s = ""

        elif c == '{': #onpen block
            s = s.strip() #strip leading and tailing blank
            if s: q.append(s) #append all line to the queue
            s = ""
            q.append(c) #append the '{' charater

            # print all the lines of the outer block
            l = q.popleft()
            while l != '{':
                print(str(depth) + (depth+1)*"\t" + l)
                l = q.popleft()
            depth +=1
            print(str(depth) + (depth)*"\t" + l) #print the { charater
        elif c == "}": #closed block
            if depth == 0: #handle error case when extra closed bracket display
                print("syntax error, extra closed bracket } ")
                exit(-1)
            s = s.strip() #strip all new line charater
            if s: q.append(s) #append all line to the queue
            s = ""
            q.append(c) # append the '}' to the queue

            #print all lines of the inner block
            l = q.popleft()
            while l != '}':
                print(str(depth) + (depth+1)*"\t" + l)
                if not q:
                    print("missing closing bracket } ")
                    exit(-1)
                l = q.popleft()
            print(str(depth) + (depth)*"\t" + l)
            depth -=1

        #append the all the line at the end, in case there is comment or something
        if c == "\n" or not c:
            s = s.strip()
            if s: q.append(s)
            s = ""

while q:
    l = q.popleft()
    print(str(depth) + (depth+1)*"\t" + l)


    