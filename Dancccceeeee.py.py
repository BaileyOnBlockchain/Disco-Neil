import pygame
import math
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dancing Stick Figure with Feet Stuck and Disco Lights")
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Animation variables
time = 0
running = True

# Fixed feet positions
LEFT_FOOT = (370, 450)
RIGHT_FOOT = (430, 450)

# Leg segment lengths
L1 = 60  # Upper leg
L2 = 60  # Lower leg

# Disco lights
lights = [
    ((100, 100), 0),
    ((700, 100), 2),
    ((400, 100), 4),
    ((100, 500), 6),
    ((700, 500), 8),
]

def get_knee(hip, foot, l1, l2, side):
    dx = foot[0] - hip[0]
    dy = foot[1] - hip[1]
    d = math.sqrt(dx**2 + dy**2)
    if d == 0 or d > l1 + l2 or d < abs(l1 - l2):
        return (hip[0] + dx / 2, hip[1] + dy / 2)  # Fallback, but shouldn't happen
    a = (l1**2 - l2**2 + d**2) / (2 * d)
    h = math.sqrt(l1**2 - a**2)
    px = hip[0] + a * (dx / d)
    py = hip[1] + a * (dy / d)
    # Two possible knees
    knee1 = (px + h * (dy / d), py - h * (dx / d))
    knee2 = (px - h * (dy / d), py + h * (dx / d))
    # Choose based on side
    if side == 'left':
        return knee1 if knee1[0] < knee2[0] else knee2
    else:
        return knee1 if knee1[0] > knee2[0] else knee2

def draw_disco_lights(screen, time):
    for pos, phase in lights:
        r = int(127 * (math.sin(time * 5 + phase) + 1))
        g = int(127 * (math.sin(time * 5 + phase + 2 * math.pi / 3) + 1))
        b = int(127 * (math.sin(time * 5 + phase + 4 * math.pi / 3) + 1))
        pygame.draw.circle(screen, (r, g, b), pos, 50)

def draw_stick_figure(screen, time):
    # Clear screen
    screen.fill(BLACK)
    
    # Draw disco lights
    draw_disco_lights(screen, time)
    
    # Calculate animation parameters
    bounce = -math.sin(time * 4) * 20  # Negative for up (smaller y) when sin positive
    sway = math.cos(time * 3) * 30   # Side-to-side sway
    arm_angle = math.sin(time * 3) * 60  # Arm swing
    head_tilt = math.sin(time * 2.5) * 15  # Head tilt
    
    # Base position with sway and bounce
    base_x = 400 + sway
    base_y = 200 + bounce
    
    # Head
    head_pos = (base_x, base_y)
    head_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
    head_surface.fill((0, 0, 0, 0))  # Transparent background
    pygame.draw.circle(head_surface, WHITE, (30, 30), 30)
    rotated_head = pygame.transform.rotate(head_surface, head_tilt)
    head_rect = rotated_head.get_rect(center=(base_x, base_y))
    screen.blit(rotated_head, head_rect)
    
    # Body
    body_top = (base_x, base_y + 30)
    body_bottom = (base_x, base_y + 150)  # Hip
    pygame.draw.line(screen, WHITE, body_top, body_bottom, 5)
    
    # Arms
    # Left arm
    left_arm_end = (
        base_x + math.cos(math.radians(arm_angle + 150)) * 70,
        base_y + 30 + math.sin(math.radians(arm_angle + 150)) * 70
    )
    pygame.draw.line(screen, WHITE, (base_x, base_y + 30), left_arm_end, 5)
    
    # Right arm
    right_arm_end = (
        base_x + math.cos(math.radians(-arm_angle - 150)) * 70,
        base_y + 30 + math.sin(math.radians(-arm_angle - 150)) * 70
    )
    pygame.draw.line(screen, WHITE, (base_x, base_y + 30), right_arm_end, 5)
    
    # Legs with bending knees using IK
    hip = (base_x, base_y + 150)
    
    # Left leg
    left_knee = get_knee(hip, LEFT_FOOT, L1, L2, 'left')
    pygame.draw.line(screen, WHITE, hip, left_knee, 5)
    pygame.draw.line(screen, WHITE, left_knee, LEFT_FOOT, 5)
    
    # Right leg
    right_knee = get_knee(hip, RIGHT_FOOT, L1, L2, 'right')
    pygame.draw.line(screen, WHITE, hip, right_knee, 5)
    pygame.draw.line(screen, WHITE, right_knee, RIGHT_FOOT, 5)

def setup():
    global time
    time = 0

async def main():
    global time, running
    setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update animation
        time += 1 / FPS
        draw_stick_figure(screen, time)
        
        # Update display
        pygame.display.flip()
        await asyncio.sleep(1.0 / FPS)
    
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())