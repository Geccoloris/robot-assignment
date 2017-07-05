#!python
import numpy as np
from numpy.random import *
import labyrinth
import matplotlib.pyplot as plt

class ParticleFilter(object):
    maze = []
    particles = list()
    weights = list()
    mu_movement = 0.
    mu_angle = 0.
    mu_measurement = 0.
    sigma_measrement = 1.
    sigma_movement_x = 1.
    sigma_movement_y = 1.
    sigma_angle = 5.

    def __init__(self, num_particles):
        #init the maze with one square being 30cm, margin 10cm
        self.maze = labyrinth.Labyrinth(30,10)
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
                            self.weights.append(1)
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
                                self.weights.append(1)
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
                                self.weights.append(1.)
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
                                self.weights.append(1)
                            current_pos[1]+=stepsize
                        current_pos[1]=-self.maze.margin+stepsize
                        current_pos[0]+=stepsize
        return
    #  seq = iter(sequence)
    #  x = ones((n, 2), int) * pos                   # Initial position
    #  f0 = seq.next()[tuple(pos)] * ones(n)         # Target colour model
    #  yield pos, x, ones(n)/n                       # Return expected position, particles and weights
    #  for im in seq:
    #    np.add(x, uniform(-stepsize, stepsize, x.shape), out=x, casting="unsafe")  # Particle motion model: uniform step
    #    x  = x.clip(zeros(2), array(im.shape)-1).astype(int) # Clip out-of-bounds particles
    #    f  = im[tuple(x.T)]                         # Measure particle colours
    #    w  = 1./(1. + (f0-f)**2)                    # Weight~ inverse quadratic colour distance
    #    w /= sum(w)                                 # Normalize w
    #    yield sum(x.T*w, axis=1), x, w              # Return expected position, particles and weights
    #    if 1./sum(w**2) < n/2.:                     # If particle cloud degenerate:
    #      x  = x[resample(w),:]                     # Resample particles according to weights

    def plot(self):
        x=[]
        y=[]
        for pos in self.particles:
            x.append(pos.position[0][0])
            y.append(pos.position[0][1])
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
        for pos in self.particles:
            pos.move(translation+np.array([np.random.normal(self.mu_movement, self.sigma_movement_x, 1),
            np.random.normal(self.mu_movement, self.sigma_movement_y, 1)]))
        return

    #angle, dist
    def measurement(self, angle, dist):
        angle = angle/180.*np.pi
        for i in range(len(self.particles)):
            error = self.maze.get_distance_wall_to_measurement(self.particles[i].position+dist*np.array([np.cos(angle+self.particles[i].angle)-np.sin(angle+self.particles[i].angle),
             np.sin(angle+self.particles[i].angle)+np.cos(angle+self.particles[i].angle)]))
            self.weights[i] *= self.normpdf(error)
        return


    def normpdf(self, x):
        var = float(self.sigma_measrement)**2
        denom = (2*np.pi*var)**.5
        num = np.exp(-(float(x)-float(self.mu_measurement))**2/(2*var))
        return num/denom

    def clear(self):
        del self.particles[:]
        return

def resample(weights):
  n = len(weights)
  indices = []
  C = [0.] + [sum(weights[:i+1]) for i in range(n)]
  u0, j = random(), 0
  for u in [(u0+i)/n for i in range(n)]:
    while u > C[j]:
      j+=1
    indices.append(j-1)
  return indices


class Position(object):
    position = np.array([0,0])
    angle = 0

    def __init__(self, translation, angle):
        self.position = np.array(translation),
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
