import pygame, math, random, keyboard

pygame.init()

class Boid:
    def __init__(self,x,y,friend=None,enemy=None):
        self.x = x
        self.y = y
        self.friend = friend
        self.enemy = enemy
    
    def step_to_center(self,size,step=0.01):
        deltaX = self.x-(size[0]/2)
        deltaY = self.y-(size[1]/2)

        self.x -= deltaX*step
        self.y -= deltaY*step

    def step_to_friend(self,step=13):
        deltaX=self.x-self.friend.x
        deltaY=self.y-self.friend.y
        magnitude = ((deltaX**2)+(deltaY**2))**0.5

        if magnitude!=0:
            if magnitude> step:
                self.x -= (deltaX/magnitude)*step
            else: 
                self.x -=deltaX
        if magnitude!=0:
            if magnitude> step:
                self.y -= (deltaY/magnitude)*step
            else: 
                self.y -=deltaY
            
    def step_to_enemy(self,step=10):
        deltaX=self.x-self.enemy.x
        deltaY=self.y-self.enemy.y
        magnitude = ((deltaX**2)+(deltaY**2))**0.5

        if magnitude!=0:
            if magnitude> step:
                self.x += (deltaX/magnitude)*step
            else: 
                self.x +=deltaX
        if magnitude!=0:
            if magnitude> step:
                self.y += (deltaY/magnitude)*step
            else: 
                self.y +=deltaY


class BoidsEnv:

    def __init__(self, x_size,y_size, boids, background_color=(37, 22, 5), 
                 trail_color=(106, 60, 36),head_color=(241, 171, 134),magnifier=16):
        self.boids_init = boids.copy()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((x_size,y_size))
        self.x_size = x_size
        self.y_size = y_size
        self.background_color = background_color
        self.trail_color = trail_color
        self.head_color = head_color
        self.magnifier=magnifier
        self.trail_length = 1
        self.trail_stagnant_length = 7
        self.trail_stagnant_thresh = 5


    def get_positions(self, boids):
        # takes in a list of boids and returns a list of tuples of each boid X,Y
        positions = []
        for boid in boids:
            new = (int(boid.x),int(boid.y))
            positions.append(new)
        return positions

    def update_positions(self,boids):
        # updates the boid positions, should be overritten at the instance level. 
        # returns the new positions of the boids
        # https://stackoverflow.com/questions/394770/override-a-method-at-instance-level#394779
        
        old_positions = self.get_positions(boids)
        for boid in boids:
            boid.step_to_center((self.x_size,self.y_size))
        for boid in boids:
            boid.step_to_friend()
        for boid in boids:
            boid.step_to_enemy()
        new_positions = self.get_positions(boids)

        return boids, old_positions, new_positions
    
    def animate(self, old_positions, new_positions):
        self.screen.fill(self.background_color)

        for i in range(len(old_positions)):
            old_position = old_positions[i]
            new_position = new_positions[i]
            
            old_x = old_position[0]
            old_y = old_position[1]
            new_x = new_position[0]
            new_y = new_position[1]

            oldx = max(0,old_x)
            oldy = max(0,self.y_size-old_y)
            newx = max(0,new_x)
            newy = max(0,self.y_size-new_y)

            oldx = min(self.x_size,old_position[0])
            oldy = min(self.y_size,self.y_size-old_position[1])
            newx = min(self.x_size,new_position[0])
            newy = min(self.y_size,self.y_size-new_position[1])



            deltax = oldx-newx
            deltay = oldy-newy
            magnitude = (deltax**2+deltay**2)**0.5

            if magnitude >self.trail_stagnant_thresh:

                normal_vector = (deltax/magnitude,deltay/magnitude)

                trailx = newx+(normal_vector[0]*self.trail_stagnant_length)
                traily = newy+(normal_vector[1]*self.trail_stagnant_length)
                
                
                pygame.draw.line(self.screen, self.trail_color, (trailx, traily), (newx,newy))
            if magnitude >0:
                normal_vector = (deltax/magnitude,deltay/magnitude)

                trailx = newx+(normal_vector[0]*magnitude*self.trail_length)
                traily = newy+(normal_vector[1]*magnitude*self.trail_length)
                
                
                pygame.draw.line(self.screen, self.trail_color, (trailx, traily), (newx,newy))
            self.screen.set_at([newx,newy],self.head_color)
            pygame.draw.circle(self.screen,self.head_color,(newx,newy),1)
        pygame.display.flip()
    
    def new_friend_enemy(self,boids,chance=10):
        
        boids[random.randint(0,len(boids)-1)].friend = boids[random.randint(0,len(boids)-1)]
        boids[random.randint(0,len(boids)-1)].enemy = boids[random.randint(0,len(boids)-1)]
        return boids

    def run(self):
        # has the while True loop for the simulation
        boids = self.boids_init
        pygame.event.pump()
        while not keyboard.is_pressed('q'):
            pygame.event.pump()
            self.clock.tick(60)
            boids, old_positions, new_positions = self.update_positions(boids)
            boids = self.new_friend_enemy(boids)
            self.animate(old_positions,new_positions)

def main():
    boids = []
    size = (2736,1874)
    for i in range(500):
        randx = random.randint(0,size[0])
        randy = random.randint(0,size[1])
        boids.append(Boid(randx,randy))
    for boid in boids:
        boid.friend = boids[random.randint(0,len(boids)-1)]
        boid.enemy = boids[random.randint(0,len(boids)-1)]
    env = BoidsEnv(size[0],size[1],boids)
    env.run()
main()