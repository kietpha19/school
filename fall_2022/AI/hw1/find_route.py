import sys

informed_search = 0

def process_input():
    input_fileName = sys.argv[1]
    origin_city = sys.argv[2]
    destination_city = sys.argv[3]
    print(input_fileName)
    print(origin_city)
    print(destination_city)

    if(len(sys.argv) == 4):
        informed_search = 1
        heuristic_fileName = sys.argv[4]

process_input()

print(informed_search)

