import numpy as np
import pandas as pd
import graphviz
from Attribute import Attribute

class Node():
    def __init__(self, attribute):
        self.attribute = attribute
        # list of Node object
        self.children = []
        self.label = None # work-around way to indicate this is not a leaf

class Leaf():
    def __init__(self, label):
        self.label = label

class DecisionTreeClassifier():
    def __init__(self, attributes):
        # a set of attributes
        self.attributes = attributes
        self.root = None
        
    # X, y are DataFrame object
    def fit(self, X, y):
        self.root = self.build_tree(X,y)

    # X, y are DataFrame object
    def build_tree(self, X, y):
        # If all samples have the same target value, return a leaf node
        if len(y.unique()) == 1:
            return Leaf(label=y.iloc[0])

        # If there are no attributes left to split on, return a leaf node with the most common target value
        if len(self.attributes) == 0:
            most_common_label = y.mode().iloc[0]
            return Leaf(label=most_common_label)

        # Select the attribute that maximizes information gain
        best_attribute = self.select_attribute(X, y)
        # print(best_attribute.name)

        # Create a new node with the selected attribute
        node = Node(best_attribute)
        
        # Remove the picked attribute out of attibutes list
        self.attributes.remove(best_attribute)

        # Split the data based on the selected attribute
        if node.attribute.is_numeric:
            # Numeric attribute: split the data based on whether it is greater than or equal to the attribute mean value
            thresh = node.attribute.thresh
            X_left = X.loc[X[node.attribute.name] < thresh]
            X_right = X.loc[X[node.attribute.name] >= thresh]
            y_left = y.loc[X[node.attribute.name] < thresh]
            y_right = y.loc[X[node.attribute.name] >= thresh]

            # Recursively build the left and right subtrees
            node.children.append(self.build_tree(X_left, y_left))
            node.children.append(self.build_tree(X_right, y_right))
        else:
            # Nominal attribute: split the data based on the attribute values
            values = node.attribute.values
            for value in values:
                X_subset = X.loc[X[node.attribute.name] == value]
                y_subset = y.loc[X[node.attribute.name] == value]

                # If there are no samples with the current attribute value, create a leaf node with the most common label
                if len(X_subset) == 0:
                    most_common_label = y.mode().iloc[0]
                    node.children.append(Leaf(label=most_common_label))
                else:
                    node.children.append(self.build_tree(X_subset, y_subset))

        return node

    def select_attribute(self, X, y):
        max_gain = -np.inf
        best_attribute = None

        for attribute in self.attributes:
            gain = self.information_gain(attribute, X[attribute.name], y)
            if gain > max_gain:
                max_gain = gain
                best_attribute = attribute

        return best_attribute

    def information_gain(self, attribute, data, y):
        H_y = self.entropy(y)
        
        if attribute.is_numeric:
            # Split the data based on whether it is greater than or equal to the attribute mean value
            thresh = attribute.choose_thresh(data)
            # data_left = data.loc[data[attribute.name] < thresh]
            # data_right = data.loc[data[attribute.name] >= thresh]
            y_left = y.loc[data < thresh]
            y_right = y.loc[data >= thresh]
            
            # Calculate the entropy for each subset
            H_yx_left = self.entropy(y_left)
            H_yx_right = self.entropy(y_right)
            
            # Calculate the conditional entropy and information gain
            H_yx = len(y_left) / len(y) * H_yx_left + len(y_right) / len(y) * H_yx_right
        
        else:
            values = attribute.get_values(data)
            H_yx = 0
            for value in values:
                # data_subset = data.loc[data[attribute.name] == value]
                y_subset = y.loc[data == value]
                H_yx += len(y_subset) / len(y) * self.entropy(y_subset)
        
        return H_y - H_yx

    def entropy(self, y):
        values, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return -np.sum(probs * np.log2(probs))
    
    def predict(self, X_test):
        predictions = []

        # Traverse the decision tree for each row in X_test
        for _, row in X_test.iterrows():
            node = self.root

            # Traverse the tree until we reach a leaf node
            # as long as node is a Node object
            while isinstance(node, Node):
                attribute = node.attribute
                value = row[attribute.name]

                if attribute.is_numeric:
                    if value < attribute.thresh:
                        node = node.children[0]
                    else:
                        node = node.children[1]
                else:
                    child_index = np.where(attribute.values == value)[0][0]
                    node = node.children[child_index]

            # Add the predicted label to the list of predictions
            predictions.append(node.label)

        return predictions

    def accuracy(self, y_pred, y_validate):
        y_pred = np.array(y_pred)
        y_validate = np.array(y_validate)
        correct = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_validate[i]:
                correct += 1
        acc = correct / len(y_pred) * 100
        return acc
    
    def draw_tree(self):
        dot = self.visualize_tree(self.root)
        dot.render("decision tree", view=True)

    def visualize_tree(self, node, dot=None):
        if dot is None:
            dot = graphviz.Digraph()
            dot.attr('node', shape='circle')
    
        if isinstance(node, Leaf):
            dot.node(str(id(node)), label=str(node.label), shape='rectangle')
        else:
            dot.node(str(id(node)), label=node.attribute.name)
            for child in node.children:
                child_id = id(child)
                dot.edge(str(id(node)), str(child_id))
                self.visualize_tree(child, dot)
        
        return dot
