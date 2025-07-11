import numpy as np
from scipy import stats


class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return "zdang31"

    def study_group(self):
        return "zdang31"

    def add_evidence(self, data_x, data_y):
        # end recursion when reaching leaf size
        if data_x.shape[0] <= self.leaf_size:
            # 2d fix shape issue. otherwise, (3,) instead of (3,1) will cause mistake for right tree calculation
            values, counts = np.unique(data_y, return_counts=True)
            mode_value = values[np.argmax(counts)]
            tree = np.atleast_2d(np.array(["leaf", mode_value, np.nan, np.nan], dtype=object))
        # end recursion when all values are same
        elif len(np.unique(data_y)) == 1:
            tree = np.atleast_2d(np.array(["leaf", data_y[0], np.nan, np.nan], dtype=object))
        # dnd recursion if all features are constant
        elif np.all(np.std(data_x, axis=0) == 0):
            values, counts = np.unique(data_y, return_counts=True)
            mode_value = values[np.argmax(counts)]
            tree = np.atleast_2d(np.array(["leaf", mode_value, np.nan, np.nan], dtype=object))
        else:
            # randomly select a feature
            index= np.random.randint(0,data_x.shape[1])
            # using median of selected column as split value.
            split_value = np.median(data_x[:, index])
            # slicing left and right tree data
            left_indices = data_x[:, index] <= split_value
            right_indices = data_x[:, index] > split_value
            left_data_x = data_x[left_indices]
            left_data_y = data_y[left_indices]
            right_data_x = data_x[right_indices]
            right_data_y = data_y[right_indices]
            # prevent edge case for empty tree
            if left_data_x.shape[0] == 0 or right_data_x.shape[0] == 0:
                values, counts = np.unique(data_y, return_counts=True)
                mode_value = values[np.argmax(counts)]
                tree = np.atleast_2d(np.array(["leaf", mode_value, np.nan, np.nan], dtype=object))
            else:
                left_tree = self.add_evidence(left_data_x, left_data_y)
                right_tree = self.add_evidence(right_data_x, right_data_y)
                root = np.array([index, split_value, 1, left_tree.shape[0] + 1], dtype=object)
                tree = np.vstack((root, left_tree, right_tree))
        self.tree = tree
        return tree

    def query(self, points):
        arr = np.zeros(points.shape[0])
        for i in range(points.shape[0]):
            node=0
            while self.tree[node][0]!="leaf":
                if points[i][int(self.tree[node][0])]<=self.tree[node][1]:
                    node+=1
                else:
                    node+=self.tree[node][3]
                node=int(node)
            arr[i]=self.tree[node][1]
        return arr



