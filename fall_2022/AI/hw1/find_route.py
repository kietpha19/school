from dis import dis
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
                heuristic[line[0]] = float(line[1])
            else:
                file.close()
                return
    
    def process_inputFile(self, edges):
        num_cities = 0
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
                v1 = line[0]
                v2 = line[1]
                d = float(line[2])
                if v1 not in edges:
                    edges[v1] = [[d, v2]]
                    num_cities +=1
                else:
                    edges[v1].append([d, v2])
                if v2 not in edges:
                    edges[v2] = [[d, v1]]
                    num_cities +=1
                else:
                    edges[v2].append([d, v1])
    

class Graph:
    num_cities = 0
    edges = {}
    heuristic = {}

    def print_route(self, pre_map, original_city, destination):
        path = []
        v = destination
        while v != original_city:
            path.append(v)
            v = pre_map[v][1]
        
        pre_d = 0
        for i in range(len(path)-1, -1, -1):
            v = path[i]
            pre_v = pre_map[v][1]
            d = pre_map[v][0] - pre_d
            pre_d += d
            print(pre_v , "to",  v, ",", d, "km")
        
        

    def print_result(self, route_map, original_city, destination, distance, nodes_popped, nodes_expanded, nodes_generated):
        print("nodes popped: " , nodes_popped)
        print("nodes expanded: " , nodes_expanded)
        print("nodes generated: " , nodes_generated)

        if distance == -1:
            print("distance: infinity")
            print("route: ")
            print("None")
            return
        if distance == 0:
            print(original_city, "to ", original_city, ", 0.0 km")
            return
        
        print("distance: ", distance, "km")
        print("Route: ")
        #print(route_map)
        self.print_route(route_map, original_city, destination)
    
    
    def path_search(self, origin_city, destination):
        #node = [distance, city_name]
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 1
        closed = set()
        pre_map = {}
        heap = [] #priority queue - min heap
        heapq.heappush(heap, [0, origin_city])

        while heap:
            node = heapq.heappop(heap)
            nodes_popped +=1

            distance = node[0]
            city_name = node[1]

            if(city_name == destination):
                self.print_result(pre_map, origin_city, destination, distance, nodes_popped, nodes_expanded, nodes_generated)
                return
            if city_name not in closed:
                closed.add(city_name)
                nodes_expanded +=1
                for node in self.edges[city_name]:
                    d = node[0]
                    v = node[1]
                    new_node = [distance + d, v]
                    heapq.heappush(heap, new_node)
                    nodes_generated +=1
                    if v not in pre_map:
                        pre_map[v] = [distance + d,city_name]
                    else:
                        path = pre_map[v]
                        if distance + d < path[0]:
                            pre_map[v] = [distance + d, city_name]

        distance = -1
        self.print_result(pre_map, origin_city, destination, distance, nodes_popped, nodes_expanded, nodes_generated)
        return


class Solution:
    g = Graph()
    input = Input()

    def __init__(self):
        self.process_input()
        self.g.path_search(self.input.origin_city, self.input.destination_city)
        

    def process_input(self):
        if(self.input.informed_search):
            self.input.process_heuristic(self.g.heuristic)
        #can't pass by reference as an int in python, so this is a work around to update num_cities
        self.g.num_cities = self.input.process_inputFile(self.g.edges)


s = Solution()



