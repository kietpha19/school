import sys
import heapq

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
    
    def process_inputFile(self, edges, city_idx, idx_city, num_cities):
        file = open(self.input_fileName)
        if not file:
            return
        Lines = file.readlines()

        for line in Lines:
            if(line == "END OF INPUT"):
                file.close()
                return num_cities
            else:
                line = line.split()
                if line[0] not in city_idx:
                    city_idx[line[0]] = num_cities
                    idx_city[num_cities] = line[0]
                    num_cities += 1
                if line[1] not in city_idx:
                    city_idx[line[1]] = num_cities
                    idx_city[num_cities] = line[1]
                    num_cities += 1
                if line[0] not in edges:
                    edges[line[0]] = [[line[1], line[2]]]
                else:
                    edges[line[0]].append([line[1], line[2]])
    

class Graph:
    num_cities = 0
    #two hashmaps to map between city and idx in the 2d matrix
    city_idx = {}
    idx_city = {}
    #later use this map to build the 2d matrix - find away to improve this
    edges = {}
    heuristic = {}
    matrix = []

    def build_matrix(self, n):
        self.matrix = [[-1]*n for i in range(n)]
        for city in self.edges:
            i = self.city_idx[city]
            self.matrix[i][i] = 0 #the city map to itself
            for connected_city in self.edges[city]:
                j = self.city_idx[connected_city[0]]
                d = connected_city[1]
                self.matrix[i][j] = int(d)
                self.matrix[j][i] = int(d)
    

    def path_search(self, origin_city, destination):
        #node = [distance, city_name, prev_city_name]
        nodes_expanded = 0
        nodes_generated = 1
        closed = set()
        heap = [] #priority queue - min heap
        heapq.heappush(heap, [0, origin_city, "None"])

        while heap:
            node = heapq.heappop(heap)
            nodes_expanded +=1

            distance = node[0]
            city_name = node[1]
            if(city_name == destination):
                print(nodes_expanded)
                print(nodes_generated)
                return distance
            if city_name not in closed:
                closed.add(city_name)
                i = self.city_idx[city_name]
                #find a way to have this in separated function
                for j in range(self.num_cities):
                    d = self.matrix[i][j]
                    if d > 0:
                        heapq.heappush(heap, [distance + d, self.idx_city[j], city_name])
                        nodes_generated +=1
        
        print(nodes_expanded)
        print(nodes_generated)
        return -1


class Solution:
    g = Graph()
    input = Input()

    def __init__(self):
        self.process_input()
        self.g.build_matrix(self.g.num_cities)
        print(self.g.path_search(self.input.origin_city, self.input.destination_city))

    def process_input(self):
        if(self.input.informed_search):
            self.input.process_heuristic(self.g.heuristic)
        #can't pass by reference as an int in python, so this is a work around to update num_cities
        self.g.num_cities = self.input.process_inputFile(self.g.edges, self.g.city_idx, self.g.idx_city, self.g.num_cities)


s = Solution()



