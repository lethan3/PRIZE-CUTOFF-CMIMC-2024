import json
import argparse
import pygame
import random

parser = argparse.ArgumentParser(description="Blotto Swarm local visualizer CLI")

parser.add_argument("--file", "-f", type=str, required=True, help="Path to match file")
args = parser.parse_args()

pygame.init()
Screen = pygame.display.set_mode((904, 804))
pygame.display.set_caption("Blotto Swarm Visualizer")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

f = open(args.file)
data = json.load(f)

you = data["you"]
opp = you^1
print("You are: " + str(you))


def get_soldiers(game_num, day_num, index):
    return data["history"][game_num]["history"][day_num]["board"][you][index], data["history"][game_num]["history"][day_num]["board"][opp][index]

def get_score(game_num, day_num):
    return data["history"][game_num]["history"][day_num]["score"][you], data["history"][game_num]["history"][day_num]["score"][opp]

def get_castles(game_num, day_num):
    if day_num == 0:
        return get_score(game_num, day_num)
    return get_score(game_num, day_num)[0] - get_score(game_num, day_num - 1)[0], get_score(game_num, day_num)[1] - get_score(game_num, day_num - 1)[1]

class Board:
    def __init__(self, x, y, width, height, rows, cols, bg_color=(255, 255, 255), border_color=(0, 0, 0), border_width=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(x + j * width / cols, y + i * height / rows, width // cols, height // rows, bg_color, border_color, border_width) for j in range(cols)] for i in range(rows)]
        self.game_num = 0
        self.pos_num = 0
        self.border_width = border_width
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_patch = pygame.Rect(202, 202, 500, 400)
        self.cell_to_index = {}
        #### Fill cell to index ####
        curidx = 0
        for j in range(9):
            self.cell_to_index[(0,j)] = curidx
            curidx += 1
        for i in range(1, 8):
            self.cell_to_index[(i,cols-1)] = curidx
            curidx += 1
        for j in range(7, -1, -1):
            self.cell_to_index[(rows-1,j)] = curidx
            curidx += 1
        for i in range(6, 0, -1):
            self.cell_to_index[(i,0)] = curidx
            curidx += 1
        

    def show(self):
        for row in self.cells:
            for cell in row:
                cell.show()

        pygame.draw.rect(Screen, self.border_color, self.border_patch, self.border_width)

    def __getitem__(self, index):
        return self.cells[index]
    
    def update(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].texts = []
                if (i,j) in self.cell_to_index:
                    index = self.cell_to_index[(i,j)]
                    soldiers = get_soldiers(self.game_num, self.pos_num, index)
                    self.cells[i][j].add_text((str(soldiers[0]),"blue"))
                    self.cells[i][j].add_text((str(soldiers[1]),"orange"))
                    if index % 3 == 0:
                        if soldiers[0] > soldiers[1]:
                            self.cells[i][j].set_bg_color("green2")
                        elif soldiers[1] > soldiers[0]:
                            self.cells[i][j].set_bg_color("red2")
                        else:
                            self.cells[i][j].set_bg_color("yellow2")
        
        self.cells[2][3].add_text("Game #" + str(self.game_num + 1))
        self.cells[2][3].set_font_size(24)
        self.cells[2][4].add_text("Day #" + str(self.pos_num))
        self.cells[2][4].set_font_size(24)
        self.cells[3][3].add_text("Score:")
        self.cells[3][3].set_font_size(24)
        self.cells[3][4].add_text((str(get_score(self.game_num, self.pos_num)[0]),"green2"))
        self.cells[3][5].add_text((str(get_score(self.game_num, self.pos_num)[1]),"red2"))
        self.cells[4][3].add_text("Castles:")
        self.cells[4][3].set_font_size(24)
        self.cells[4][4].add_text((str(get_castles(self.game_num, self.pos_num)[0]),"green2"))
        self.cells[4][5].add_text((str(get_castles(self.game_num, self.pos_num)[1]),"red2"))



    


class Cell:
    def __init__(self, x, y, width, height, bg_color=(255, 255, 255), border_color=(0, 0, 0), border_width=1, font_size=36):
        self.x = x
        self.y = y
        self.texts = []
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.width = width
        self.height = height
        self.font_size = font_size

    def show(self):
        pygame.draw.rect(Screen, self.bg_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(Screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)
        for i,text_color in enumerate(self.texts):
            #center the text in the cell
            if type(text_color) == str:
                text = text_color
                color = (0,0,0)
            else:
                text,color = text_color
            font = pygame.font.Font(None, self.font_size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // (len(self.texts)+1) + i * self.font_size))
            Screen.blit(text_surface, text_rect)
    
    def add_text(self, text):
        self.texts.append(text)

    def set_bg_color(self, color):
        self.bg_color = color
    
    def set_bdr_color(self, color):
        self.border_color = color

    def set_font_size(self, size):
        self.font_size = size
    







########### SETUP ############
game_num = 0
pos_num = 0
auto_play = False
bd = Board(2, 2, 900, 800, 8, 9, bg_color="bisque", border_color="dark slate blue", border_width=1)
for y in range(8):
    bd[y][0].set_bg_color("light steel blue")
    bd[y][8].set_bg_color("light steel blue")
    if((y)%3 == 0): bd[y][0].set_bg_color("RoyalBlue1")
    if((y+8)%3 == 0): bd[y][8].set_bg_color("RoyalBlue1")

for x in range(9):
    bd[0][x].set_bg_color("light steel blue")
    bd[7][x].set_bg_color("light steel blue")
    if((0+x)%3 == 0): bd[0][x].set_bg_color("RoyalBlue1")
    if((7+x)%3 == 0): bd[7][x].set_bg_color("RoyalBlue1")

for y in range(2,6):
    for x in range(2,7):
        bd[y][x].set_bdr_color("bisque")

hold_left_time = 0
hold_right_time = 0
tick_count = 0

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and hold_left_time > 10 and tick_count%5 == 0:
        pos_num -= 1
    if keys[pygame.K_RIGHT] and hold_right_time > 10 and tick_count%5 == 0:
        pos_num += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_num += 1
            if event.key == pygame.K_DOWN:
                game_num -= 1
            if event.key == pygame.K_LEFT:
                pos_num -= 1
                hold_left_time = 0
            if event.key == pygame.K_RIGHT:
                pos_num += 1
                hold_right_time = 0
            if event.key == pygame.K_r:
                pos_num = 0
            if event.key == pygame.K_l:
                pos_num += 10
            if event.key == pygame.K_j:
                pos_num -= 10
            if event.key == pygame.K_SPACE:
                auto_play = not auto_play
    
    hold_right_time += 1
    hold_left_time += 1

    game_num = max(min(game_num, len(data["history"]) - 1), 0)
    pos_num = max(min(pos_num, len(data["history"][game_num]["history"]) - 1), 0)
    bd.game_num = game_num
    bd.pos_num = pos_num
    
    #bd[0][0].set_bg_color((random.randint(0,255), 0, 0))
    bd.update()
    bd.show()
    
    pygame.display.flip()
    clock.tick(60)
    tick_count += 1
    tick_count %= 60
    


bd = [["" for i in range(9)] for j in range(8)]
def on_key_press(keysym):
  global game_num
  global pos_num
  if keysym == "Up":
    game_num += 1
  if keysym == "Down":
    game_num -= 1
  if keysym == "Left":
    pos_num -= 1
  if keysym == "Right":
    pos_num += 1
  game_num = max(min(game_num, 4), 0)
  pos_num = max(min(pos_num, 99), 0)
  for y in range(9):
    index = y
    if(index % 3 == 0):
      bd[0][y] = "|" + str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index]) + "|"
    else:
      bd[0][y] = str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index])
  for x in range(8):
    index = x + 8
    if(index % 3 == 0):
      bd[x][8] = "|" + str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index]) + "|"
    else:
      bd[x][8] = str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index])
  for y in range(9):
    index = 23 - y
    if(index % 3 == 0):
      bd[7][y] = "|" + str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index]) + "|"
    else:
      bd[7][y] = str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index])
  for x in range(1, 8):
    index = 30 - x
    if(index % 3 == 0):
      bd[x][0] = "|" + str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index]) + "|"
    else:
      bd[x][0] = str(j["history"][game_num]["history"][pos_num]["board"][you][index]) + "-" + str(j["history"][game_num]["history"][pos_num]["board"][opp][index])
  


bd.on_key_press = on_key_press
on_key_press("")
bd.show()
