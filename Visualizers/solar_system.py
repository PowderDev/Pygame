import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50) 
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
  AU = 149.6e6 * 1000
  G = 6.67428e-11
  SCALE = 230 / AU #* 1 AU ~= 100px
  TIMESTEP = 3600*24 #* 1 Day
  
  def __init__(self, name, x, y, radius, color, mass):
      self.name = name
      self.x = x
      self.y = y
      self.radius = radius
      self.color = color
      self.mass = mass
      
      self.is_sun = False
      self.distance_to_sun = 0
      self.orbit = []
      
      self.x_vel = 0
      self.y_vel = 0
      
      
  def draw(self, win):
    x = self.x * self.SCALE + WIDTH / 2
    y = self.y * self.SCALE + HEIGHT / 2

    if len(self.orbit) > 2:
      updated_points = []
      for point in self.orbit:
        x, y = point
        x = x * self.SCALE + WIDTH / 2
        y = y * self.SCALE + HEIGHT / 2
        updated_points.append((x, y))
        
      pygame.draw.lines(win, self.color, False, updated_points, 2)
    
    pygame.draw.circle(win, self.color, (x, y), self.radius)
    
  
  def attraction(self, other):
    other_x , other_y = other.x, other.y
    distance_x = other_x - self.x
    distance_y = other_y - self.y
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    if other.is_sun:
      self.distance_to_sun = distance
      
    force = self.G * self.mass * other.mass / distance**2
    theta = math.atan2(distance_y, distance_x)
    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force

    return force_x, force_y
  
  def update_position(self, planets):
    total_fx = total_fy = 0
    
    for planet in planets:
      if self == planet:
        continue
      
      fx, fy = self.attraction(planet)
      total_fx += fx
      total_fy += fy
      
    self.x_vel += total_fx / self.mass * self.TIMESTEP
    self.y_vel += total_fy / self.mass * self.TIMESTEP

    self.x += self.x_vel * self.TIMESTEP
    self.y += self.y_vel * self.TIMESTEP
    self.orbit.append((self.x, self.y))

def main():
  run = True
  clock = pygame.time.Clock()
  FPS = 60
  
  sun = Planet("Sun", 0, 0, 50, YELLOW, 1.98892 * 10**30)
  sun.is_sun = True
  
  earth = Planet("Earth", -1 * Planet.AU, 0, 26, BLUE, 5.9742 * 10**24)
  earth.y_vel = 29.783 * 1000
  
  mars = Planet("Mars", -1.524 * Planet.AU, 0 ,22, RED, 6.39 * 10**23)
  mars.y_vel = 24.07 * 1000
  
  mercury = Planet("Mercury", 0.387 * Planet.AU, 0 ,16, DARK_GREY, 3.3 * 10**23)
  mercury.y_vel = -47.4 * 1000
  
  venus = Planet("Venus", 0.723 * Planet.AU, 0 ,22, WHITE, 4.8685 * 10**24)
  venus.y_vel = -35.02 * 1000
  
  
  planets = [sun, earth, mars, mercury, venus]
  
  def draw():
    WIN.fill((0, 0, 0))
    
    for i, planet in enumerate(planets):
      if not planet.is_sun:
        planet.update_position(planets)
      planet.draw(WIN)
      if not planet.is_sun:
        distance_text = FONT.render(f"{planet.name}: {round(planet.distance_to_sun/1000)} km", 1, WHITE)
        WIN.blit(distance_text, (WIN.get_width() - ( distance_text.get_width() + 30 ), -40 + 30 * (i + 1)))
    
    pygame.display.update()
  
  while run:
    clock.tick(FPS)
    draw()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        
        
  pygame.quit()
  

main()


def fib (num):
  if num == 1 or num == 2:
    return 1
  
  last = fib(num - 1)
  second_last = fib(num - 2)
  return last + second_last

print(fib(13))