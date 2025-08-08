import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Tennis court dimensions (scaled)
COURT_WIDTH = 800
COURT_HEIGHT = 400
COURT_X = (SCREEN_WIDTH - COURT_WIDTH) // 2
COURT_Y = (SCREEN_HEIGHT - COURT_HEIGHT) // 2

class TennisScoring:
    def __init__(self):
        self.player1_games = 0
        self.player2_games = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.player1_points = 0
        self.player2_points = 0
        self.is_deuce = False
        self.advantage_player = None
        self.game_over = False
        self.winner = None
        
    def get_point_display(self, points):
        point_map = {0: "0", 1: "15", 2: "30", 3: "40"}
        return point_map.get(points, "40")
    
    def add_point(self, player):
        if self.game_over:
            return
            
        if player == 1:
            self.player1_points += 1
        else:
            self.player2_points += 1
            
        self.check_game_win()
    
    def check_game_win(self):
        # Regular scoring
        if self.player1_points >= 4 or self.player2_points >= 4:
            if abs(self.player1_points - self.player2_points) >= 2:
                # Game won
                if self.player1_points > self.player2_points:
                    self.player1_games += 1
                else:
                    self.player2_games += 1
                
                self.player1_points = 0
                self.player2_points = 0
                self.is_deuce = False
                self.advantage_player = None
                
                self.check_set_win()
            else:
                # Deuce situation
                if self.player1_points >= 3 and self.player2_points >= 3:
                    self.is_deuce = True
                    if self.player1_points > self.player2_points:
                        self.advantage_player = 1
                    elif self.player2_points > self.player1_points:
                        self.advantage_player = 2
                    else:
                        self.advantage_player = None
    
    def check_set_win(self):
        # Standard set win (6 games with 2 game lead, or 7-5)
        if (self.player1_games >= 6 and self.player1_games - self.player2_games >= 2) or \
           (self.player2_games >= 6 and self.player2_games - self.player1_games >= 2):
            
            if self.player1_games > self.player2_games:
                self.player1_sets += 1
            else:
                self.player2_sets += 1
                
            self.player1_games = 0
            self.player2_games = 0
            
            # Check match win (best of 3 sets)
            if self.player1_sets >= 2:
                self.game_over = True
                self.winner = 1
            elif self.player2_sets >= 2:
                self.game_over = True
                self.winner = 2
    
    def get_score_display(self):
        if self.is_deuce:
            if self.advantage_player == 1:
                return "ADV", "40"
            elif self.advantage_player == 2:
                return "40", "ADV"
            else:
                return "DEUCE", "DEUCE"
        else:
            return self.get_point_display(self.player1_points), self.get_point_display(self.player2_points)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-2, 2])
        self.radius = 8
        self.trail = []
        
    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
        # Ball physics - slight gravity and air resistance
        self.dy += 0.1  # gravity
        self.dx *= 0.999  # air resistance
        
        # Court boundaries
        if self.x <= COURT_X or self.x >= COURT_X + COURT_WIDTH:
            self.dx = -self.dx
            
        # Top and bottom court boundaries
        if self.y <= COURT_Y:
            self.dy = abs(self.dy)
        elif self.y >= COURT_Y + COURT_HEIGHT:
            self.dy = -abs(self.dy)
    
    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail)
            radius = int(self.radius * alpha)
            if radius > 0:
                pygame.draw.circle(screen, (255, 255, 0, int(255 * alpha)), 
                                 (int(pos[0]), int(pos[1])), radius)
        
        # Draw ball
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)

class Player:
    def __init__(self, x, y, color, is_player1=True):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.color = color
        self.speed = 5
        self.is_player1 = is_player1
        
    def update(self, keys):
        if self.is_player1:
            if keys[pygame.K_w] and self.y > COURT_Y:
                self.y -= self.speed
            if keys[pygame.K_s] and self.y < COURT_Y + COURT_HEIGHT - self.height:
                self.y += self.speed
            if keys[pygame.K_a] and self.x > COURT_X:
                self.x -= self.speed
            if keys[pygame.K_d] and self.x < COURT_X + COURT_WIDTH // 2 - self.width:
                self.x += self.speed
        else:
            if keys[pygame.K_UP] and self.y > COURT_Y:
                self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < COURT_Y + COURT_HEIGHT - self.height:
                self.y += self.speed
            if keys[pygame.K_LEFT] and self.x > COURT_X + COURT_WIDTH // 2:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] and self.x < COURT_X + COURT_WIDTH - self.width:
                self.x += self.speed
    
    def draw(self, screen):
        # Draw player body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw head
        head_radius = 8
        pygame.draw.circle(screen, (255, 220, 177), 
                         (self.x + self.width // 2, self.y - head_radius), head_radius)
        
        # Draw racket
        racket_x = self.x + self.width + 5 if not self.is_player1 else self.x - 15
        racket_y = self.y + self.height // 2
        pygame.draw.rect(screen, (139, 69, 19), (racket_x, racket_y - 15, 10, 30))
        pygame.draw.circle(screen, BLACK, (racket_x + 5, racket_y - 20), 8, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class MenuItem:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.hovered = False
        
    def draw(self, screen, font):
        color = LIGHT_GRAY if self.hovered else WHITE
        border_color = ORANGE if self.hovered else BLACK
        
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 3)
        
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)

class TennisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Professional Tennis Game")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game states
        self.state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER
        
        # Game objects
        self.player1 = Player(COURT_X + 50, COURT_Y + COURT_HEIGHT // 2, BLUE)
        self.player2 = Player(COURT_X + COURT_WIDTH - 70, COURT_Y + COURT_HEIGHT // 2, RED, False)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.scoring = TennisScoring()
        
        # Menu items
        self.menu_items = [
            MenuItem("NEW GAME", SCREEN_WIDTH // 2 - 100, 300, 200, 60, "new_game"),
            MenuItem("INSTRUCTIONS", SCREEN_WIDTH // 2 - 100, 380, 200, 60, "instructions"),
            MenuItem("QUIT", SCREEN_WIDTH // 2 - 100, 460, 200, 60, "quit")
        ]
        
        self.instructions_back = MenuItem("BACK", 50, SCREEN_HEIGHT - 100, 100, 50, "menu")
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "PLAYING"
                    elif self.state in ["INSTRUCTIONS", "GAME_OVER"]:
                        self.state = "MENU"
                        
                elif event.key == pygame.K_SPACE and self.state == "PLAYING":
                    # Simple ball hitting mechanism
                    player1_rect = self.player1.get_rect()
                    player2_rect = self.player2.get_rect()
                    ball_rect = pygame.Rect(self.ball.x - self.ball.radius, 
                                          self.ball.y - self.ball.radius,
                                          self.ball.radius * 2, self.ball.radius * 2)
                    
                    if player1_rect.colliderect(ball_rect):
                        self.ball.dx = abs(self.ball.dx) + random.uniform(-1, 1)
                        self.ball.dy += random.uniform(-2, 2)
                    elif player2_rect.colliderect(ball_rect):
                        self.ball.dx = -abs(self.ball.dx) + random.uniform(-1, 1)
                        self.ball.dy += random.uniform(-2, 2)
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    
                    if self.state == "MENU":
                        for item in self.menu_items:
                            if item.is_clicked(pos):
                                if item.action == "new_game":
                                    self.start_new_game()
                                elif item.action == "instructions":
                                    self.state = "INSTRUCTIONS"
                                elif item.action == "quit":
                                    return False
                                    
                    elif self.state == "INSTRUCTIONS":
                        if self.instructions_back.is_clicked(pos):
                            self.state = "MENU"
                            
                    elif self.state == "GAME_OVER":
                        # Click anywhere to return to menu
                        self.state = "MENU"
                        
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                
                if self.state == "MENU":
                    for item in self.menu_items:
                        item.hovered = item.is_clicked(pos)
                elif self.state == "INSTRUCTIONS":
                    self.instructions_back.hovered = self.instructions_back.is_clicked(pos)
                        
        return True
    
    def start_new_game(self):
        self.state = "PLAYING"
        self.player1 = Player(COURT_X + 50, COURT_Y + COURT_HEIGHT // 2, BLUE)
        self.player2 = Player(COURT_X + COURT_WIDTH - 70, COURT_Y + COURT_HEIGHT // 2, RED, False)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.scoring = TennisScoring()
    
    def update(self):
        if self.state == "PLAYING":
            keys = pygame.key.get_pressed()
            
            self.player1.update(keys)
            self.player2.update(keys)
            self.ball.update()
            
            # Check for scoring
            if self.ball.x < COURT_X:
                self.scoring.add_point(2)  # Player 2 scores
                self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            elif self.ball.x > COURT_X + COURT_WIDTH:
                self.scoring.add_point(1)  # Player 1 scores
                self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                
            # Check for game over
            if self.scoring.game_over:
                self.state = "GAME_OVER"
    
    def draw_court(self):
        # Court background
        pygame.draw.rect(self.screen, GREEN, (COURT_X, COURT_Y, COURT_WIDTH, COURT_HEIGHT))
        
        # Court lines
        pygame.draw.rect(self.screen, WHITE, (COURT_X, COURT_Y, COURT_WIDTH, COURT_HEIGHT), 3)
        
        # Center line
        pygame.draw.line(self.screen, WHITE, 
                        (COURT_X + COURT_WIDTH // 2, COURT_Y),
                        (COURT_X + COURT_WIDTH // 2, COURT_Y + COURT_HEIGHT), 3)
        
        # Service lines
        service_line_y1 = COURT_Y + COURT_HEIGHT // 4
        service_line_y2 = COURT_Y + 3 * COURT_HEIGHT // 4
        
        pygame.draw.line(self.screen, WHITE,
                        (COURT_X, service_line_y1),
                        (COURT_X + COURT_WIDTH, service_line_y1), 2)
        pygame.draw.line(self.screen, WHITE,
                        (COURT_X, service_line_y2),
                        (COURT_X + COURT_WIDTH, service_line_y2), 2)
        
        # Net
        net_x = COURT_X + COURT_WIDTH // 2
        for i in range(0, COURT_HEIGHT, 10):
            pygame.draw.line(self.screen, WHITE,
                           (net_x - 2, COURT_Y + i),
                           (net_x + 2, COURT_Y + i), 1)
    
    def draw_score(self):
        if self.state != "PLAYING":
            return
            
        # Score background
        score_bg = pygame.Rect(10, 10, 300, 150)
        pygame.draw.rect(self.screen, BLACK, score_bg)
        pygame.draw.rect(self.screen, WHITE, score_bg, 2)
        
        # Current points
        p1_points, p2_points = self.scoring.get_score_display()
        
        # Draw scores
        y_offset = 20
        
        # Sets
        sets_text = f"Sets: {self.scoring.player1_sets} - {self.scoring.player2_sets}"
        sets_surface = self.small_font.render(sets_text, True, WHITE)
        self.screen.blit(sets_surface, (20, y_offset))
        y_offset += 25
        
        # Games
        games_text = f"Games: {self.scoring.player1_games} - {self.scoring.player2_games}"
        games_surface = self.small_font.render(games_text, True, WHITE)
        self.screen.blit(games_surface, (20, y_offset))
        y_offset += 25
        
        # Points
        points_text = f"Points: {p1_points} - {p2_points}"
        points_surface = self.score_font.render(points_text, True, WHITE)
        self.screen.blit(points_surface, (20, y_offset))
        y_offset += 35
        
        # Player names
        p1_text = self.small_font.render("Player 1 (WASD + Space)", True, BLUE)
        p2_text = self.small_font.render("Player 2 (Arrows + Space)", True, RED)
        self.screen.blit(p1_text, (20, y_offset))
        self.screen.blit(p2_text, (20, y_offset + 20))
    
    def draw_menu(self):
        # Background gradient effect
        for y in range(SCREEN_HEIGHT):
            color_value = int(20 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(self.screen, (0, color_value, 0), (0, y), (SCREEN_WIDTH, y))
        
        # Title
        title_surface = self.title_font.render("PROFESSIONAL TENNIS", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Title shadow
        shadow_surface = self.title_font.render("PROFESSIONAL TENNIS", True, BLACK)
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 3, 153))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Menu items
        for item in self.menu_items:
            item.draw(self.screen, self.menu_font)
        
        # Version info
        version_text = self.small_font.render("v1.0 - Professional Edition", True, WHITE)
        self.screen.blit(version_text, (10, SCREEN_HEIGHT - 30))
    
    def draw_instructions(self):
        self.screen.fill((20, 40, 20))
        
        # Title
        title_surface = self.menu_font.render("GAME INSTRUCTIONS", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Instructions text
        instructions = [
            "",
            "CONTROLS:",
            "Player 1 (Blue): WASD keys to move, SPACE to hit ball",
            "Player 2 (Red): Arrow keys to move, SPACE to hit ball",
            "",
            "TENNIS SCORING:",
            "• Points: 0, 15, 30, 40, Game",
            "• Must win by 2 points after deuce (40-40)",
            "• First to 6 games wins the set (must lead by 2)",
            "• First to 2 sets wins the match",
            "",
            "GAMEPLAY:",
            "• Hit the ball when it's near your player",
            "• Ball goes out of bounds = point for opponent",
            "• Try to make strategic shots to win points",
            "",
            "Press ESC to pause during game",
            "",
            "Good luck and have fun!"
        ]
        
        y = 100
        for line in instructions:
            if line:
                color = YELLOW if line.endswith(":") else WHITE
                text_surface = self.small_font.render(line, True, color)
                self.screen.blit(text_surface, (50, y))
            y += 25
        
        # Back button
        self.instructions_back.draw(self.screen, self.small_font)
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        winner_text = f"PLAYER {self.scoring.winner} WINS!"
        winner_surface = self.title_font.render(winner_text, True, YELLOW)
        winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(winner_surface, winner_rect)
        
        # Final score
        score_text = f"Final Score: {self.scoring.player1_sets} - {self.scoring.player2_sets}"
        score_surface = self.menu_font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_surface, score_rect)
        
        # Continue instruction
        continue_text = "Click anywhere to return to menu"
        continue_surface = self.small_font.render(continue_text, True, WHITE)
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(continue_surface, continue_rect)
    
    def draw_paused(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        paused_surface = self.title_font.render("PAUSED", True, YELLOW)
        paused_rect = paused_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(paused_surface, paused_rect)
        
        # Resume instruction
        resume_text = "Press ESC to resume"
        resume_surface = self.small_font.render(resume_text, True, WHITE)
        resume_rect = resume_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(resume_surface, resume_rect)
    
    def draw(self):
        self.screen.fill(DARK_GREEN)
        
        if self.state == "MENU":
            self.draw_menu()
            
        elif self.state == "INSTRUCTIONS":
            self.draw_instructions()
            
        elif self.state in ["PLAYING", "PAUSED", "GAME_OVER"]:
            # Draw game elements
            self.draw_court()
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.ball.draw(self.screen)
            self.draw_score()
            
            if self.state == "PAUSED":
                self.draw_paused()
            elif self.state == "GAME_OVER":
                self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TennisGame()
    game.run()