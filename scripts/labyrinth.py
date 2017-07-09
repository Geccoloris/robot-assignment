#!python
import numpy as np
import graph

class Labyrinth(object):
    labyrinth_array = []
    labyrinth_graph = []
    size = 0.
    margin = 0.

    def __init__(self, size, margin):
        self.size = size #in cm of one tile
        self.margin = margin
        self.labyrinth_array = np.array(
           [[-1, -1, -1, -1, -1, -1, -1],
            [-1,  1,  0,  2,  0,  3, -1],
            [-1,  0, -1, -1, -1, -1, -1],
            [-1,  4,  0,  5,  0,  6, -1],
            [-1, -1, -1,  0, -1, -1, -1],
            [-1,  7,  0,  8,  0,  9, -1],
            [-1, -1, -1, -1, -1, -2, -1]])
        self.labyrinth_graph = graph.Graph({'1': ['2', '4'],
                '2': ['1', '3'],
                '3': ['2'],
                '4': ['1', '5'],
                '5': ['4', '6', '8'],
                '6': ['5'],
                '7': ['8'],
                '8': ['5', '7', '9'],
                '9': ['8', 'exit']})

    def find_shortest_path(self, start, end):
        return self.labyrinth_graph.find_shortest_path(start,end)

    def numbers_connections(self):
        return np.prod(self.labyrinth_array.shape) - np.count_nonzero(self.labyrinth_array)

    def get_area(self):
        return (self.size-2*self.margin)*(self.size-2*self.margin)*9+(self.numbers_connections()*2+1)*self.margin*(self.size-2*self.margin)

    def get_distance_wall_to_measurement(self, position):
        field = self.get_field_and_coords(position)
        check = [-1,-1] #where to check for a wall
        check_near = False
        error = 0.

        #checking if out of bound
        if field[0]<0 or field[1]<0:
#            print  "negative", self.labyrinth_array[field[2]*2+1,field[3]*2+1], [field[2]*2+1+check[0],field[3]*2+1]
            return -np.min(field[0:2])
        elif field[2]>2:
#            print  "index", field
            return field[0]
        elif field[3]>2:
#            print  "index", field
            return field[1]

        #at what corner of the field is the robot
        if field[0]>self.size/2:
            field[0]=self.size-field[0]
            check[0]+=2
        if field[1]>self.size/2:
            field[1] = self.size-field[1]
            check[1]+=2

        if field[0]>field[1]:
            #is there a wall?
            if self.labyrinth_array[field[2]*2+1,field[3]*2+1+check[1]] == -1:
#                print "y taken", field, self.labyrinth_array[field[2]*2+1,field[3]*2+1], [field[2]*2+1,field[3]*2+1+check[1]]
                error = field[1]
            else:
                #if not, check surrounding later
#                print "checked", field, self.labyrinth_array[field[2]*2+1,field[3]*2+1]
                check_near=True
        elif self.labyrinth_array[field[2]*2+1+check[0],field[3]*2+1] == -1:
#            print  "x taken",field, self.labyrinth_array[field[2]*2+1,field[3]*2+1], [field[2]*2+1+check[0],field[3]*2+1]
            error = field[0]
        else:
#            print "checked", field, self.labyrinth_array[field[2]*2+1,field[3]*2+1]
            check_near = True

        if check_near:
            return np.linalg.norm(field[0:2],2)

        return error

    def get_field_and_coords(self, position):
        #print position[0]
        res = [position[0],position[1],0,0] #pos_x, pos_y, field_x,field_y
        while res[0] > self.size:
            res[0]-=self.size
            res[2]+=1
        while res[1] > self.size:
            res[1]-=self.size
            res[3]+=1
        return res
