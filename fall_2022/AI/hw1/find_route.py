import sys

class Input:
    input_fileName = sys.argv[1]
    origin_city = sys.argv[2]
    destination_city = sys.argv[3]
    informed_search = (len(sys.argv) == 5)
    heuristic_fileName = ""

    def __init__(self):
        if(self.informed_search):
            self.heuristic_fileName = sys.argv[4]
    
    def process_heuristic(self,heuristic):
        file = open(self.heuristic_fileName)
        Lines = file.readlines()
        for line in Lines:
            if(line != "END OF INPUT"):
                line = line.split()
                heuristic[line[0]] = line[1]
            else:
                file.close()
                return
    
    def process_inputFile(self, edges, city_idx, num_cities):
        file = open(self.input_fileName)
        Lines = file.readlines()

        for line in Lines:
            if(line == "END OF INPUT"):
                file.close()
                return num_cities
            else:
                line = line.split()
                if line[0] not in city_idx:
                    city_idx[line[0]] = num_cities
                    num_cities += 1
                if line[1] not in city_idx:
                    city_idx[line[1]] = num_cities
                    num_cities += 1
                if line[0] not in edges:
                    edges[line[0]] = [[line[1], line[2]]]
                else:
                    edges[line[0]].append([line[1], line[2]])
    

class Graph:
    num_cities = 0
    city_idx = {}
    edges = {}
    heuristic = {}
    matrix = []

    def build_matrix(self, n):
        self.matrix = [[0]*n for i in range(n)]
        for city in self.edges:
            i = self.city_idx[city]
            for connected_city in self.edges[city]:
                j = self.city_idx[connected_city[0]]
                d = connected_city[1]
                self.matrix[i][j] = int(d)
                self.matrix[j][i] = int(d)

        print(self.matrix)


class Solution:
    g = Graph()
    input = Input()

    def __init__(self):
        self.process_input()
        self.g.build_matrix(self.g.num_cities)

    def process_input(self):
        if(self.input.informed_search):
            self.input.process_heuristic(self.g.heuristic)
        #can't pass by reference as an int in python, so this is a work around to update num_cities
        self.g.num_cities = self.input.process_inputFile(self.g.edges, self.g.city_idx, self.g.num_cities)


s = Solution()



