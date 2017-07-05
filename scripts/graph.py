class Graph:
    graph =  {'1': ['2', '4'],
            '2': ['1', '3'],
            '3': ['2'],
            '4': ['1', '5'],
            '5': ['4', '6', '8'],
            '6': ['5'],
            '7': ['8'],
            '8': ['5', '7', '9'],
            '9': ['8', 'exit']}


    def __init__(self, graph_attr):
        self.graph = graph_attr


    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not self.graph.has_key(start):
            return None
        shortest = None
        for node in self.graph[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
