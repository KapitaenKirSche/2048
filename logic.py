#Zufallszahlen
import random
import config
import pygame

#Bewegen-------------------------------------------------------------------------------------
#Nimmt ein Spielfeld als Eingabe und gibt ein Spielfeld zurück, bei dem alle Felder soweit wie möglich in die richtige Richtung bewegt sind.
#Spielfeld(board) ist eine Liste von Listen->Matrix(Tabelle), wobei jedes Element eine Zahl(Zweierpotenz bzw. 0 für leeres Feld) besitzt (0,2,4,8,16,...,2048)


def move(board, dir, maxim=-1):
  '''
  Input: board(Matrix, Spielfeld)
         dir(int, Richtung: 0-oben;1-rechts;2-unten;3-links)
         maxim(int, maximale Bewegungen der Felder)
  führt die Bewegun aus. 
  Output: board(Matrix, Spielfeld)
  '''
  if dir == 0:
    board = up(board, maxim)
  elif dir == 1:
    board = right(board, maxim)
  elif dir == 2:
    board = down(board, maxim)
  elif dir == 3:
    board = left(board, maxim)
  return board


def left(board, maxim=-1):
  board = rotateRight(board)
  board = up(board, maxim)
  board = rotateRight(board, 3)
  return board


def right(board, maxim=-1):
  board = rotateRight(board, 3)
  board = up(board, maxim)
  board = rotateRight(board)
  return board


def up(board, maxim=-1):
  '''
  board: Spielfeld
  max: Maximale Zahl, die Spielfeld bewegt wird, -1=unendlich

  return: Spielfeld, bewegt nach oben
  '''

  inp_board = []
  for x in range(len(board)):
    inp_board.append([])
    for i in board[x]:
      inp_board[x].append(i)

  zeilencount = 0
  for zeile in inp_board:
    spaltencount = 0
    for spalte in zeile:
      maxim_ = maxim
      a_ = zeilencount
      if zeilencount == 0 or maxim == 0:
        running = False
      else:
        running = True

      while running:
        a_ -= 1
        maxim_ -= 1
        if inp_board[a_][spaltencount] == 0:
          inp_board[a_][spaltencount] = spalte
          inp_board[a_ + 1][spaltencount] = 0

        elif inp_board[a_][spaltencount] == spalte:
          inp_board[a_][spaltencount] = spalte * -1
          inp_board[a_ + 1][spaltencount] = 0

        else:
          running = False
        if a_ == 0 or maxim_ == 0:
          running = False
      spaltencount += 1
    zeilencount += 1

  return merge(inp_board)


def down(board, maxim=-1):
  board = rotateRight(board, 2)
  board = up(board, maxim)
  board = rotateRight(board, 2)
  return board


def rotateRight(board, anzahl=1):
  '''
  Eingabe board: das Spielfeld
  Gibt das 90 Grad gedrehte board zurück
  '''
  for _ in range(anzahl):
    rotatedBoard = []
    for x in range(len(board[0])):
      rotatedBoard.append([])
      for i in range(len(board)):
        rotatedBoard[x].append(0)

    y = 0

    lengthy = len(board) - 1
    lengthx = len(board[0]) - 1
    for zeile in board:
      x = 0
      for spalte in zeile:
        rotatedBoard[x][lengthy - y] = spalte
        x += 1
      y += 1
    board = rotatedBoard

  return board


def merge(board):
  '''
  input board: Spielfeld
  verdoppelt alle Felder, wo zwei gleiche Zahlen aufeinander treffen
  return: umgewandeltes board
  '''
  for i in range(len(board)):
    for j in range(len(board[i])):
      x = board[i][j]
      if x < 0:
        board[i][j] = x * -2
  return board


#Andere Logik------------------------------------------------------------
def bewegung_moeglich_generell(board, maxim=-1):
  '''
  input: board(matrix, Spielfeld)

  prüft, ob der Spieler eine mögliche Bewegung machen kann

  output: beweg_mogl(bool, gibt an ob eine Bewegung mgl. ist)
  '''
  beweg_mogl = False
  for i in board:
    if 0 in i:
      beweg_mogl = True
  if beweg_mogl == False:
    if board != up(board, maxim):
      beweg_mogl = True
    elif board != right(board, maxim):
      beweg_mogl = True

  return beweg_mogl


def bewegungMoeglichSpeziell(board, dir, maxim=-1):
  '''
  input: board(matrix, Spielfeld)
         dir(int, Richtung: 0-oben;1-rechts;2-unten;3-links)
         maxim(int, maximale Bewegungen der Felder)

  prüft, ob der Spieler eine mögliche Bewegung in die speziell gefragte Richtung machen kann

  output: beweg_mogl(bool, gibt an ob eine Bewegung mgl. ist)
  '''
  beweg_mogl = False
  if dir == 0:
    if board != up(board, maxim):
      beweg_mogl = True
  elif dir == 1:
    if board != right(board, maxim):
      beweg_mogl = True
  elif dir == 2:
    if board != down(board, maxim):
      beweg_mogl = True
  elif dir == 3:
    if board != left(board, maxim):
      beweg_mogl = True

  return beweg_mogl


def maxWert(board):
  '''
  input: board(Spielfeld, Matrix)

  gibt den höchsten Zellenwert aus

  return: höchster(int, höchster Zellenwert)
  '''
  hoechster = 0
  for zeile in board:
    for spalte in zeile:
      if spalte > hoechster:
        hoechster = spalte
  return hoechster


def createRandom(board, numb=1):
  '''
  Input: board: Spielfeld
         numb: Anzahl wie oft der Prozess wiederholt wird

  Gibt das Board, mit einer nach Zufall verteilten Zahl 2 oder 4 an einer leeren Stelle aus
  '''
  for _ in range(numb):
    nullen = []
    for zeile in range(len(board)):
      for spalte in range(len(board[zeile])):
        if board[zeile][spalte] == 0:
          nullen.append((zeile, spalte))
    rndm = random.randint(0, len(nullen) - 1)
    board[nullen[rndm][0]][nullen[rndm][1]] = random.choice([2, 4])
  return board


def buildBoard(x, y, anzahlnewrand=0):
  '''
  input: x(int,laenge x-Achse Matrix),
         y(int,laenge y-Achse Matrix),
         anzahlnewrand(int, gibt an, wieviele neue Zellen zuffällig befüllt werden sollen)

  baut eine Matrix anhand den x- und y Längen auf und füllt mit leeren Feldern

  output:board(Matrix,Spielfeld mit zwei zufälligen zweien bzw. vieren)
  '''
  board = []
  for i in range(y):
    board.append([])
    for j in range(x):
      board[i].append(0)
  board = createRandom(board, anzahlnewrand)
  return board


def initGame(x, y, anzahlnewrand):

  return buildBoard(x, y, anzahlnewrand)


#Zeichnen---------------------------------------------------------
def drawBoard(board, fenster, colors=config.colors,tile_surfs=config.tile_surfaces):
  '''
  input: board(matrix, das Spielfeld), fenster(pygame window, in welchem fenster das Spielfeld gemalt werden soll)

  malt das Spielfeld ins Fenster, nicht aber die UI
  '''
  y = 0
  for row in board:
    y += 1
    x = 0
    for tile in row:
      x += 1
      rectx = config.size_in_between * x + config.size * (x - 1)
      recty = config.size_in_between * y + config.size * (y - 1)
      fenster.blit(tile_surfs[tile], (rectx, recty))



def drawUIingame(score, highscore, fenster, colors=config.colors):
  '''
  Input: score(int, aktuelle Punktezahl), highscore(int, beste Punktezahl)
  Zeichnet das Spielfeld in das Fenster
  '''
  fenster.fill(colors.get("bg"))
  pygame.draw.rect(fenster, (50, 50, 50), (config.ui_down_rect))


def drawUIHome(fenster, colors=config.colors):
  '''
  Zeichnet den Startbildschirm
  '''
  fenster.blit(config.bilder["startscreen"], (0, 0))

def drawOverworld(fenster,site,areas,s=config.s):
  fenster.blit(config.bilder["overworld"+str(site)], (0, 0))
  #for i in areas:
    #pygame.blit(s,i)



def konsolenAusgabe(board):
  for i in board:
    print(str(i))
  print("\n\n")


#-------------------------------
def draw_text_in_box(surface, text, font="Arial", color1=(0, 0, 0),color2=(255,255,255),fact=0.85):
  """
  Draws text in a box on the given surface.
  Make sure never exeeding the box's dimensions.
  Make sure to dar in the middle of the box.
  """
  fontsize = 0
  my_font = pygame.font.SysFont(font, fontsize)
  text_to_draw = my_font.render(str(text), True, color1)
  text_width = text_to_draw.get_width()
  text_height = text_to_draw.get_height()
  while text_width < surface.get_width()*fact and text_height < surface.get_height()*fact:
    fontsize += 1
    my_font = pygame.font.SysFont(font, fontsize)
    text_to_draw = my_font.render(str(text), True, color1)
    text_width = text_to_draw.get_width()
    text_height = text_to_draw.get_height()
  my_font = pygame.font.SysFont(font, fontsize - 1)
  if int(text) <=4:
    color=color1
  else:
    color=color2
  text_to_draw = my_font.render(str(text), True, color)
  text_width = text_to_draw.get_width()
  text_height = text_to_draw.get_height()
  surfheight = surface.get_height()
  surfwidth = surface.get_width()
  if text !=0:
    surface.blit(text_to_draw, (surfwidth / 2 - text_width / 2, (surfheight / 2 - text_height / 2)+3))


def setup_tiles(width, heigth, tile_list=config.tile_list, colors=config.colors, font="assets/fonts/ClearSans-Bold.ttf",font_color=(255,255,255)):
  tiles = {}
  for tile in tile_list:
    tile_surf = pygame.Surface((width, heigth))
    tile_surf.fill(colors.get(tile))
    draw_text_in_box(tile_surf, tile, font)
    tiles[tile]=tile_surf

  return tiles