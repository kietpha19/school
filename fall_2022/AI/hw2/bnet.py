import sys
class Node:
    def __init__(self):
        self.parents = []
        self.table = []
    
    #used to store all probability to the node
    def create_table(self, prob_table):
        l = len(self.parents)
        if len(prob_table) != 2**l:
            print("not enough probability values")
            exit(-1)
        for i in range(2**l):
            self.table.append(prob_table[i])

class Child_node(Node):
    def __init__(self, parents):
        self.parents = parents
        self.table = []
    
    #used to get the conditional probability
    #self value: value of the node itself
    #parent_values: an array of parent's values - has to be in order
    def get_cond_prob(self, self_value, parent_values):
        if len(self.parents) != len(parent_values):
            print("not enough parameter")
            exit(-1)
        
        l = len(parent_values)
        idx = len(self.table) - 1
        for i in range(l):
            if parent_values[i] == True:
                idx -= 2**(l-i-1)

        #print(idx)
        if self_value == True:
            return self.table[idx]
        else:
            return 1 - self.table[idx]

class Root_node(Node):
    def __init__(self):
        self.parents = []
        self.table = []
    
    #since this root node has no parent, it'll will just return the value base on the value of itself
    def get_prob(self, self_value):
        if self_value == True:
            return self.table[0]
        else:
            return 1 - self.table[0]

Burglary = Root_node()
Burglary.create_table([0.001])

Earthquake = Root_node()
Earthquake.create_table([0.002])

Alarm = Child_node([Burglary, Earthquake])
Alarm.create_table([0.95, 0.94, 0.29, 0.001])

JohnCalls = Child_node([Alarm])
JohnCalls.create_table([0.9, 0.05])

MaryCalls = Child_node([Alarm])
MaryCalls.create_table([0.7, 0.01])

# print(Burglary.table)
# print(Earthquake.table)
# print(Alarm.table)
# print(JohnCalls.table)
# print(MaryCalls.table)

#used to compute Joined Probability
def computeProbability(b,e,a,j,m):
    return JohnCalls.get_cond_prob(j,[a])*MaryCalls.get_cond_prob(m,[a])*Alarm.get_cond_prob(a,[b,e])*Burglary.get_prob(b)*Earthquake.get_prob(e)

if len(sys.argv) != 6:
    print("not enough arguments")
    exit(-1)

b,e,a,j,m = True, True, True, True, True
for value in sys.argv:
    if value[0] == 'B':
        if value[1] == 'f':
            b = False
    elif value[0] == 'E':
        if value[1] == 'f':
            e = False
    elif value[0] == 'A':
        if value[1] == 'f':
            a = False
    elif value[0] == 'M':
        if value[1] == 'f':
            m = False
    elif value[0] == 'J':
        if value[1] == 'f':
            j = False

print(computeProbability(b,e,a,m,j))