from dis import dis
import sys
import heapq

# this is the class to handle all input files
class Input:
    input_fileName = sys.argv[1]
    origin_city = sys.argv[2]
    destination_city = sys.argv[3]
    informed_search = (len(sys.argv) == 5) # if the heuristic file is passed as one of the argument
    heuristic_fileName = ""

    #automatically trigger if informed search
    def __init__(self):
        if(self.informed_search):
            self.heuristic_fileName = sys.argv[4]
    
    #basically scan line by line to store the heuristic value into a hasmap
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
    
    '''
    edges is representation of graph, using hashmap with key is the vertext,
    and value is and array of [distance, connected_vertex]
    '''
    def process_inputFile(self, edges):
        num_cities = 0
        file = open(self.input_fileName)
        if not file:
            return
        Lines = file.readlines()

        for line in Lines:
            if(line == "END OF INPUT"):
                file.close()
                return num_cities #number of cities in the graph
            else:
                line = line.split()
                v1 = line[0]
                v2 = line[1]
                d = float(line[2])
                #add vertex 1 to edges if hasn't discover or update its edges if already discovered
                if v1 not in edges:
                    edges[v1] = [[d, v2]]
                    num_cities +=1
                else:
                    edges[v1].append([d, v2])
                #same for vetex 2
                if v2 not in edges:
                    edges[v2] = [[d, v1]]
                    num_cities +=1
                else:
                    edges[v2].append([d, v1])
    

#representation of graph, included components: number of cities, the edges (hashmap of lists), heuristic (hashmap of heuristic value)
class Graph:
    num_cities = 0
    edges = {}
    heuristic = {}

    #using the previous city map to backtracking and print out the route form original city to destination
    def print_route(self, pre_map, original_city, destination):
        path = [] #used to stored backtracking route
        v = destination #act like a pointer, use to backtrack until see the original city

        #loop for backtracking
        while v != original_city:
            path.append(v)
            v = pre_map[v][1]
        
        #loop for print out the route
        pre_d = 0
        for i in range(len(path)-1, -1, -1):
            v = path[i]
            pre_v = pre_map[v][1]
            d = pre_map[v][0] - pre_d
            pre_d += d
            print(pre_v , "to",  v, ",", d, "km")
        
        
    #print basic info about the graph search process
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
        #calling the print route
        self.print_route(route_map, original_city, destination)
    
    #searching route/path form origin_city to destination
    def path_search(self, origin_city, destination, informed_search):
        #handle wrong city's name
        if origin_city not in self.edges:
            print("there is no city name: ", origin_city)
            return
        if destination not in self.edges:
            print("there is no city name: ", destination)
            return

        #node = [distance, city_name]
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 1
        closed = set()
        pre_map = {}
        heap = [] #priority queue - min heap
        if(informed_search):
            heapq.heappush(heap, [self.heuristic[origin_city], origin_city])
        else:
            heapq.heappush(heap, [0, origin_city])

        while heap:
            node = heapq.heappop(heap)
            nodes_popped +=1

            city_name = node[1]
            if(informed_search):
                distance = node[0] - self.heuristic[city_name]
            else:
                distance = node[0]

            #if find the solution
            if(city_name == destination):
                self.print_result(pre_map, origin_city, destination, distance, nodes_popped, nodes_expanded, nodes_generated)
                return
            if city_name not in closed:
                closed.add(city_name)
                nodes_expanded +=1

                #scan over the node successors
                for node in self.edges[city_name]:
                    v = node[1] #vertex/city
                    d = node[0] #distance

                    #creating new node
                    if(informed_search):
                        new_node = [distance + d + self.heuristic[v], v]
                    else:
                        new_node = [distance + d, v]

                    #push that new node into the min heap
                    heapq.heappush(heap, new_node)
                    nodes_generated +=1

                    #update the pre_map for backtracking later
                    #node = [distance, pre city name]
                    if v not in pre_map:
                        pre_map[v] = [distance + d,city_name]
                    else:
                        pre_node = pre_map[v]
                        if distance + d < pre_node[0]:
                            pre_map[v] = [distance + d, city_name]

        #if couldn't find any route
        distance = -1
        self.print_result(pre_map, origin_city, destination, distance, nodes_popped, nodes_expanded, nodes_generated)
        return


class Solution:
    g = Graph()
    input = Input()

    def __init__(self):
        self.process_input()
        self.g.path_search(self.input.origin_city, self.input.destination_city, self.input.informed_search)
        

    def process_input(self):
        if(self.input.informed_search):
            self.input.process_heuristic(self.g.heuristic)
        #can't pass by reference as an int in python, so this is a work around to update num_cities
        self.g.num_cities = self.input.process_inputFile(self.g.edges)


#main
s = Solution()



