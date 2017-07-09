#!python
import numpy as np
from numpy.random import *
import labyrinth
import matplotlib.pyplot as plt
import copy

class ParticleFilter(object):
    maze = []
    particles = list()
#    weights = list()
    mu_movement = 0.
    mu_angle = 0.
    mu_measurement = 0.
    sigma_measrement = 3.8
    sigma_movement_x = 2.
    sigma_movement_y = 2.
    sigma_angle = 5./180*np.pi
    cumulated_weights = [0.]
    resample_ready = False

    def __init__(self, num_particles):
        #init the maze with one square being 30cm, margin 10cm
        self.maze = labyrinth.Labyrinth(30.,10.)
        #determine how to spread the particles
        stepsize = 1.0 #in cm
        particles_per_cm2 = num_particles/16./self.maze.get_area()
        if particles_per_cm2 > 1:
            stepsize = 1./np.sqrt(particles_per_cm2)
        print "Currently we get ", particles_per_cm2, " particles per cm2, making it one particle every", stepsize, "cm)"

        #init the particles
        current_pos = [0,0]
        for field_x in range(3):
            for field_y in range(3):
                current_pos = [self.maze.margin,self.maze.margin]
                #inside field
                while current_pos[0]<=self.maze.size-self.maze.margin:
                    while current_pos[1]<=self.maze.size-self.maze.margin:
                        for i in range(16):
                            self.particles.append(Position([field_x*self.maze.size+current_pos[0],
                            field_y*self.maze.size+current_pos[1]], i*np.pi/8))
                            #self.weights.append(1.)
                        current_pos[1]+=stepsize
                    current_pos[0]+=stepsize
                    current_pos[1]=self.maze.margin

                #connecting fields down/x dir
                current_pos[0]=-self.maze.margin+stepsize
                current_pos[1]=self.maze.margin
                if self.maze.labyrinth_array[field_x*2+2,field_y*2+1] == 0:
                    print "connection down to", self.maze.labyrinth_array[field_x*2+3,field_y*2+1]
                    while current_pos[0]<self.maze.margin:
                        while current_pos[1]<=self.maze.size-self.maze.margin:
                            for i in range(16):
                                self.particles.append(Position([(field_x+1)*self.maze.size+current_pos[0],
                                field_y*self.maze.size+current_pos[1]], i*np.pi/8))
                                #self.weights.append(1)
                            current_pos[1]+=stepsize
                        current_pos[1]=self.maze.margin
                        current_pos[0]+=stepsize

                #connecting exit down
                current_pos[0]=-self.maze.margin+stepsize
                current_pos[1]=self.maze.margin
                if self.maze.labyrinth_array[field_x*2+2,field_y*2+1] == -2:
                    print "connection exit from", self.maze.labyrinth_array[field_x*2+1,field_y*2+1]
                    while current_pos[0]<=0:
                        while current_pos[1]<=self.maze.size-self.maze.margin:
                            for i in range(16):
                                self.particles.append(Position([(field_x+1)*self.maze.size+current_pos[0],
                                field_y*self.maze.size+current_pos[1]], i*np.pi/8))
                                #self.weights.append(1.)
                            current_pos[1]+=stepsize
                        current_pos[1]=self.maze.margin
                        current_pos[0]+=stepsize

                #connecting fields right/y dir
                current_pos[0]=self.maze.margin
                current_pos[1]=-self.maze.margin+stepsize
                if self.maze.labyrinth_array[field_x*2+1,field_y*2+2] == 0:
                    print "connection right to", self.maze.labyrinth_array[field_x*2+1,field_y*2+3]
                    while current_pos[0]<=self.maze.size-self.maze.margin:
                        while current_pos[1]<self.maze.margin:
                            for i in range(16):
                                self.particles.append(Position([(field_x)*self.maze.size+current_pos[0],
                                (field_y+1)*self.maze.size+current_pos[1]], i*np.pi/8))
                                #self.weights.append(1)
                            current_pos[1]+=stepsize
                        current_pos[1]=-self.maze.margin+stepsize
                        current_pos[0]+=stepsize
        return

    def plot(self):
#        mx = 0self.
#        for i in range(len(self.cumulated_weights)-2):
#            if self.cumulated_weights[i+1]-self.cumulated_weights[i] > mx:
#                mx = self.cumulated_weights[i+1]-self.cumulated_weights[i]
        x=[]
        y=[]
        i=0
        for pos in self.particles:
#            if self.cumulated_weights[i+1]-self.cumulated_weights[i]>0.9*mx:
            x.append(pos.position[0])
            y.append(pos.position[1])

        plt.scatter(x,y)
        plt.show()
        return

    def movement_angle_deg(self, angle):
        for pos in self.particles:
            pos.turn_deg(angle+np.random.normal(self.mu_angle, self.sigma_angle, 1))
        return

    def movement_angle_rad(self, angle):
        for pos in self.particles:
            pos.turn_rad(angle+np.random.normal(self.mu_angle, self.sigma_angle/180*np.pi, 1))
        return

    def movement_position(self, translation):
        i=0
        for pos in self.particles:
            pos.move(translation+np.array([np.random.normal(self.mu_movement, self.sigma_movement_x, 1),
            np.random.normal(self.mu_movement, self.sigma_movement_y, 1)]))
            i+=1
        return

    #angle, dist
    def measurement(self, angle, dist):
        if dist >20:
            self.resample_ready = False
            return False
        angle = angle/180.*np.pi
        for i in range(len(self.particles)):
            error = self.maze.get_distance_wall_to_measurement(self.particles[i].position+
            dist*np.array([np.cos(angle+self.particles[i].angle)-np.sin(angle+self.particles[i].angle),
             np.sin(angle+self.particles[i].angle)+np.cos(angle+self.particles[i].angle)]))
            if self.particles[i].position[0] < 0 or self.particles[i].position[1] < 0 or self.particles[i].position[0] > self.maze.size*3 or self.particles[i].position[1] > self.maze.size*3:
#                self.weights[i] = 0
                self.cumulated_weights.append(self.cumulated_weights[-1]+0)
            else:
#                self.weights[i] *= self.normpdf(error)
                self.cumulated_weights.append(self.cumulated_weights[-1]+self.normpdf(error))
#            if i%1004==0:
#                print error, self.particles[i].position[0], self.cumulated_weights[-1]
        self.resample_ready = True
        return True


    def normpdf(self, x):
        var = float(self.sigma_measrement)**2
        denom = (2*np.pi*var)**.5
        num = np.exp(-(float(x)-float(self.mu_measurement))**2/(2*var))
        return num/denom

    def clear(self):
        del self.particles[:]
        return

    def resample(self):
        if not self.resample_ready:
            return False
        n = len(self.cumulated_weights)-1
        step = self.cumulated_weights[-1]/n
        print "Started resampling", n
        particles_tmp = list()
#        weights_tmp = list()
#        max_weight = np.max(self.weights)
        j = 0
        for u in [(i*step) for i in range(n)]:
            while u > self.cumulated_weights[j]:
                j+=1
            particles_tmp.append(copy.deepcopy(self.particles[j-1]))
#            weights_tmp.append(self.weights[j-1]/max_weight)
        del self.particles[:]
#        del self.weights[:]
        del self.cumulated_weights[:]
        self.particles = particles_tmp
#        self.weights = weights_tmp
        self.cumulated_weights = [0.]
        self.resample_ready = False
        return True


class Position(object):
    position = np.array([0.,0.])
    angle = 0

    def __init__(self, translation, angle):
        self.position = np.array(translation, dtype=np.float64)
        self.angle = angle

    #first the movement then the rotation
    def turn_deg(self, angle):
        self.angle += float(angle)/180*np.pi
        return

    def turn_rad(self, angle):
        self.angle += angle
        return

    def move(self, translation):
        self.position += (translation[0]*np.array([np.cos(self.angle),np.sin(self.angle)])+translation[1]*np.array([-np.sin(self.angle),np.cos(self.angle)]))
        return
