
# game.py : Gustav Emrich : 2024/05/13 The program is a small mini golf game were you can shoot a ball around and try to get it in the hole with as few tries as possible.

# Import necessary modules
import pygame
from Ball import Ball  # Assuming Ball class is defined in a separate module
import random
import math

# Define a Wall class to represent obstacles
class Wall:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)  # Create a Rect object for collision detection
        self.image = pygame.transform.scale(image, (width, height))  # Resize the image to match the wall dimensions

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((1200, 800))  # Set the screen size
clock = pygame.time.Clock()  # Initialize clock for controlling frame rate
running = True  # Flag to control the main loop
dt = 0
startpos = ()  # Starting position for mouse click
clicked = False  # Flag to indicate mouse click
ball_radius = 10  # Radius of the ball
background_image = pygame.image.load("grass.jpg").convert()  # Load background image

# Initialize the ball object
ball = Ball(pygame.Vector2(75, screen.get_height() - 75), ball_radius)

# Load wall image
wall_image = pygame.image.load("wall.jpg").convert()

# List to hold wall objects
walls = []

# Counter for the number of tries
tries = 0

# Function to check if a point is inside a circle
def isInside(circle_x, circle_y, radius, x, y):
    return ((x - circle_x) ** 2 + (y - circle_y) ** 2 <= radius ** 2)

# Function to create walls (obstacles)
def create_walls():
    global walls
    walls = []  # Clear existing walls
    min_distance = 18  # Minimum distance between walls
    i = 0
    
    # Create 16 walls
    while i < 16:
        wall_width = random.randint(50, 200)
        wall_height = random.randint(50, 200)
        wall_x = random.randint(0, screen.get_width() - wall_width)
        wall_y = random.randint(0, screen.get_height() - wall_height)
        
        new_wall_rect = pygame.Rect(wall_x, wall_y, wall_width, wall_height)
        overlapping = False
        
        # Check for collision with existing walls
        for wall in walls:
            if new_wall_rect.colliderect(wall.rect):
                overlapping = True
                break
                
        # Check the distance from the new wall to existing ones
        too_close_to_wall = False
        for wall in walls:
            if abs(wall_x - wall.rect.x) < min_distance and abs(wall_y - wall.rect.y) < min_distance:
                too_close_to_wall = True
                break
        
        # Check for collision with the ball
        too_close_to_ball = new_wall_rect.colliderect(pygame.Rect(ball.position.x - ball_radius * 2, ball.position.y - ball_radius * 2, ball_radius * 4, ball_radius * 4))
        
        # Ensure the new wall is not overlapping with existing walls or the ball, and is at least 18 pixels apart from other walls
        if not overlapping and not too_close_to_ball and not too_close_to_wall:
            walls.append(Wall(wall_x, wall_y, wall_width, wall_height, wall_image))
            i += 1

# Function to create bunkers (circular obstacles)
def create_bunkers():
    global bunkers
    bunkers = []  # Clear existing bunkers
    min_distance = 30  # Minimum distance between bunkers
    i = 0
    
    # Create 9 bunkers
    while i < 9:
        radius = random.randint(10, 50)
        bunker_x = random.randint(radius, screen.get_width() - radius)
        bunker_y = random.randint(radius, screen.get_height() - radius)
        
        new_bunker = pygame.Rect(bunker_x, bunker_y, radius*2, radius*2)
        overlapping = False
        
        # Check for collision with existing bunkers
        for bunker in bunkers:
            dx = new_bunker.centerx - bunker.centerx
            dy = new_bunker.centery - bunker.centery
            distance = math.sqrt(dx**2 + dy**2)  # Pythagorean theorem
            if distance < (min_distance + radius):
                overlapping = True
                break
        
        # Ensure the new bunker is not overlapping with existing bunkers
        if not overlapping:
            bunkers.append(new_bunker)
            i += 1

# Function to randomly position the hole
def randomPos():
    global hole_x, hole_y
    # Find an empty space for the hole
    hole_found = False
    while not hole_found:
        hole_x = random.randint(screen.get_width() * 0.75, screen.get_width())
        hole_y = random.randint(0, screen.get_height())
        hole_rect = pygame.Rect(hole_x - 8, hole_y - 8, 16, 16)
        hole_found = True
        for wall in walls:
            if wall.rect.colliderect(hole_rect):
                hole_found = False
                break

# Function to update game state
def update():
    global ball, tries
    ball.position.x += ball.velocity.x
    ball.position.y += ball.velocity.y
    
    # Apply friction to slow down the ball
    if abs(ball.velocity.x) < 0.003:
        ball.velocity.x = 0
    else:
        ball.velocity.x *= 0.99
    if abs(ball.velocity.y) < 0.003:
        ball.velocity.y = 0
    else:
        ball.velocity.y *= 0.99
    
    ball_rect = pygame.Rect(ball.position.x - ball_radius, ball.position.y - ball_radius, ball_radius * 2, ball_radius * 2)  # Create a Rect object for the ball
    
    # Bounce off the walls if the ball reaches the screen boundaries
    if ball_rect.right >= screen.get_width() or ball_rect.left <= 0:
        ball.velocity.x = -ball.velocity.x
        ball.velocity *= 0.9  # Reduce velocity magnitude
        # Move the ball out of the wall
        if ball_rect.right >= screen.get_width():
            ball.position.x = screen.get_width() - ball_radius - 1
        else:
            ball.position.x = ball_radius + 1
    if ball_rect.bottom >= screen.get_height() or ball_rect.top <= 0:
        ball.velocity.y = -ball.velocity.y
        ball.velocity *= 0.9  # Reduce velocity magnitude
        # Move the ball out of the wall
        if ball_rect.bottom >= screen.get_height():
            ball.position.y = screen.get_height() - ball_radius - 1
        else:
            ball.position.y = ball_radius + 1
    
    # Check collision with bunkers
    for bunker in bunkers:
        dstans = (ball.position.x - bunker.centerx) ** 2 + (ball.position.y - bunker.centery) ** 2
        distans = math.sqrt(dstans)
        if distans - bunker.width < 3:
            print(distans)  # Print the distance if the ball is close to a bunker
        if (distans - bunker.width) < 3:
            ball.velocity.x *= 0.9
            ball.velocity.y *= 0.9
    
    # Check collision with walls
    for wall in walls:
        if ball_rect.colliderect(wall.rect):  # Use colliderect method with ball_rect
            # Bounce off the wall
            if ball_rect.centerx < wall.rect.left or ball_rect.centerx > wall.rect.right:
                ball.velocity.x *= -1
                ball.velocity *= 0.8  # Reduce velocity magnitude
                # Move the ball out of the wall
                if ball_rect.centerx < wall.rect.left:
                    ball.position.x = wall.rect.left - ball_radius - 1
                else:
                    ball.position.x = wall.rect.right + ball_radius + 1
            if ball_rect.centery < wall.rect.top or ball_rect.centery > wall.rect.bottom:
                ball.velocity.y *= -1
                ball.velocity *= 0.8  # Reduce velocity magnitude
                # Move the ball out of the wall
                if ball_rect.centery < wall.rect.top:
                    ball.position.y = wall.rect.top - ball_radius - 1
                else:
                    ball.position.y = wall.rect.bottom + ball_radius + 1
    
    # Check if the ball reaches the hole
    if abs(ball.position.x - hole_x) <= 10 and abs(ball.position.y - hole_y) <= 10 and ball.velocity.x < 0.8 and ball.velocity.y < 0.8:
        randomPos()  # Randomly reposition the hole
        tries = 0  # Reset the tries counter
        ball.position = pygame.Vector2(75, screen.get_height() - 75)  # Reset the ball position
        ball.velocity.x *= 0  # Stop the ball
        ball.velocity.y *= 0  # Stop the ball

# Function to draw the strength indicator
def strength_color():
    global ball
    color = "white"
    if abs(ball.position.x - pygame.mouse.get_pos()[0]) > 5 or abs(ball.position.y - pygame.mouse.get_pos()[1]) > 5:
        color = "blue"
    if abs(ball.position.x - pygame.mouse.get_pos()[0]) > 80 or abs(ball.position.y - pygame.mouse.get_pos()[1]) > 80:
        color = "orange"
    if abs(ball.position.x - pygame.mouse.get_pos()[0]) > 150 or abs(ball.position.y - pygame.mouse.get_pos()[1]) > 200:
        color = "red"
    
    # Draw lines to indicate strength
    pygame.draw.line(screen, color, ball.position, pygame.mouse.get_pos())
    pygame.draw.line(screen, color, (ball.position.x - 1, ball.position.y), (pygame.mouse.get_pos()[0] - 1,pygame.mouse.get_pos()[1]))
    pygame.draw.line(screen, color, (ball.position.x - 2, ball.position.y), (pygame.mouse.get_pos()[0] - 2,pygame.mouse.get_pos()[1]))
    pygame.draw.line(screen, color, (ball.position.x + 1, ball.position.y), (pygame.mouse.get_pos()[0] + 1,pygame.mouse.get_pos()[1]))
    pygame.draw.line(screen, color, (ball.position.x + 2, ball.position.y), (pygame.mouse.get_pos()[0] + 2,pygame.mouse.get_pos()[1]))
    pygame.draw.line(screen, color, (ball.position.x, ball.position.y - 1), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] - 1))
    pygame.draw.line(screen, color, (ball.position.x, ball.position.y - 2), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] - 2))
    pygame.draw.line(screen, color, (ball.position.x, ball.position.y + 1), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] + 1))
    pygame.draw.line(screen, color, (ball.position.x, ball.position.y + 2), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] + 2))

# Load ball image
ball_image = pygame.image.load("ball.png").convert_alpha()

# Set the initial positions for the hole and the ball
randomPos()

# Create walls and bunkers
create_walls()
create_bunkers()

# Main game loop
while running:
    update()  # Update game state

    # Draw the game elements
    screen.blit(background_image, (0, 0))  # Draw background image
    for bunker in bunkers:
        pygame.draw.circle(screen, (255, 255, 0), bunker.center, bunker.width)  # Draw bunkers
    for wall in walls:
        screen.blit(wall.image, wall.rect.topleft)  # Draw walls
    pygame.draw.circle(screen, (0, 0, 0), (hole_x, hole_y), 12)  # Draw hole
    screen.blit(ball_image, (ball.position.x - ball_image.get_width() / 2, ball.position.y - ball_image.get_height() / 2))  # Draw ball
    # Display tries counter
    font = pygame.font.Font(None, 36)
    text = font.render(f"Tries: {tries}", True, (255, 255, 255))
    screen.blit(text, (20, 20))

    if clicked:
        strength_color()  # Draw strength indicator

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if isInside(ball.position.x, ball.position.y, 40, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    startpos = pygame.mouse.get_pos()
                    clicked = True
                        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if clicked:
                    clicked = False
                    ball.velocity.x = (ball.position.x - pygame.mouse.get_pos()[0])/25
                    ball.velocity.y = (ball.position.y - pygame.mouse.get_pos()[1])/25
                    tries += 1
        
    pygame.display.flip()  # Update the display

    dt = clock.tick(60)  # Cap the frame rate at 60 FPS

pygame.quit()  # Quit pygame
