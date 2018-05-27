class Node(object):
    """
    Tree structure

    Reference: http://stackoverflow.com/questions/3753665/python-tree-structure-and-numerical-codes/3753796#3753796
    """

    byname = {}

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.byname[name] = self
        if parent is None:  # root pseudo-node
            self.code = 0
        else:  # all normal nodes
            self.parent.children.append(self)
            self.code = len(self.parent.children)
