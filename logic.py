#Zufallszahlen
import random
import config
import pygame
import copy

#Bewegen-------------------------------------------------------------------------------------
#Nimmt ein Spielfeld als Eingabe und gibt ein Spielfeld zurück, bei dem alle Felder soweit wie möglich in die richtige Richtung bewegt sind.
#Spielfeld(board) ist eine Liste von Listen->Matrix(Tabelle), wobei jedes Element eine Zahl(Zweierpotenz bzw. 0 für leeres Feld) besitzt (0,2,4,8,16,...,2048)

def move_test(board, dir, maxim=-1):
  '''
  Input: board(Matrix, Spielfeld)
         dir(int, Richtung: 0-oben;1-rechts;2-unten;3-links)
         maxim(int, maximale Bewegungen der Felder)
  führt die Bewegung aus, allerdings ohne Punkte zählen.
  Output: board(Matrix, Spielfeld)
  '''
  if dir == 0:
    board = up(board, maxim)
    board = merge(board)
  elif dir == 1:
    board = right(board, maxim)
    board = merge(board)
  elif dir == 2:
    board = down(board, maxim)
    board = merge(board)
  elif dir == 3:
    board = left(board, maxim)
    board = merge(board)
  return board


def move(board, dir, maxim=-1):
  '''
  Input: board(Matrix, Spielfeld)
         dir(int, Richtung: 0-oben;1-rechts;2-unten;3-links)
         maxim(int, maximale Bewegungen der Felder)
  führt die Bewegung aus.
  Output: board(Matrix, Spielfeld)
  '''
  if dir == 0:
    board = up(board, maxim)
    countScore(board)
    board = merge(board)
  elif dir == 1:
    board = right(board, maxim)
    countScore(board)
    board = merge(board)
  elif dir == 2:
    board = down(board, maxim)
    countScore(board)
    board = merge(board)
  elif dir == 3:
    board = left(board, maxim)
    countScore(board)
    board = merge(board)


  stay_floor = config.levels[config.current_level]["stay_on_floor_tiles"]
  for i in stay_floor:
    x=i[0]
    y=i[1]
    if board[y][x]["tile_numb"] <= 0:
      board[y][x]=copy.deepcopy(stay_floor[i])

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
  #copy board
  inp_board=copy.deepcopy(board)

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

        if spalte["fraction"] != "none":
          if inp_board[a_][spaltencount]["tile_numb"] == 0:
            inp_board[a_][spaltencount] = copy.deepcopy(spalte)
            inp_board[a_ + 1][spaltencount] = copy.deepcopy(config.template_tile_dic)


          elif inp_board[a_][spaltencount]["tile_numb"] == spalte["tile_numb"] and inp_board[a_][spaltencount]["fraction"] == spalte["fraction"]:
            inp_board[a_][spaltencount] = copy.deepcopy(spalte)
            inp_board[a_][spaltencount]["tile_numb"] *= -1
            inp_board[a_ + 1][spaltencount] = copy.deepcopy(config.template_tile_dic)

          elif inp_board[a_][spaltencount]["type"] == "wall":
            pass

          elif inp_board[a_][spaltencount]["type"] == "duplicate":
            inp_board[a_][spaltencount]=copy.deepcopy(spalte)
            inp_board[a_][spaltencount]["tile_numb"]*=-1
            inp_board[a_+1][spaltencount]=copy.deepcopy(config.template_tile_dic)

          elif inp_board[a_][spaltencount]["type"]=="halve":
            if spalte["tile_numb"] > 2:
              inp_board[a_][spaltencount] = copy.deepcopy(spalte)
              inp_board[a_][spaltencount]["tile_numb"] = int(0.5*inp_board[a_][spaltencount]["tile_numb"])
              inp_board[a_ + 1][spaltencount] = copy.deepcopy(config.template_tile_dic)
            else:
              inp_board[a_][spaltencount] = copy.deepcopy(spalte)
              inp_board[a_ + 1][spaltencount] = copy.deepcopy(config.template_tile_dic)

          #Gegner-kollision:
          elif inp_board[a_][spaltencount]["fraction"] != spalte["fraction"]:
            if inp_board[a_][spaltencount]["tile_numb"] > spalte["tile_numb"]:
              inp_board[a_+1][spaltencount] = copy.deepcopy(config.template_tile_dic)
            elif inp_board[a_][spaltencount]["tile_numb"] < spalte["tile_numb"]:
              inp_board[a_][spaltencount] = copy.deepcopy(spalte)
              inp_board[a_+1][spaltencount] = copy.deepcopy(config.template_tile_dic)

          else:
            running = False

        else:
          running=False
        if a_ == 0 or maxim_ == 0:
          running = False

      spaltencount += 1
    zeilencount += 1

  return inp_board

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
      if x["tile_numb"] < 0 and x["tile_numb"]!=-1:
        board[i][j]["tile_numb"] = x["tile_numb"] * -2
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
    for j in i:
      if 0 in j:
        beweg_mogl = True

  if beweg_mogl == False:
    if board != up(board, maxim):
      beweg_mogl = True
    elif board != right(board, maxim):
      beweg_mogl = True
    elif board != left(board, maxim):
      beweg_mogl = True
    elif board != down(board, maxim):
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
  if board != move_test(board, dir, maxim):
    beweg_mogl =True

  return beweg_mogl


def biggestTile(board, tile_category="player"):
  '''
  input: board(Spielfeld, Matrix)

  gibt den Wert der höchsten Zelle aus

  return: hoechster(int, höchster Zellenwert)
  '''
  hoechster = 0
  for zeile in board:
    for spalte in zeile:
      if spalte["tile_numb"] > hoechster:
        if spalte["fraction"]==tile_category:
          hoechster = spalte["tile_numb"]
  return hoechster

def check_sieg_feld(cods, board, ziel):
  '''
  input: cods(Tuple, koordinaten des Zielfelds), board(spielfeld,Matrix), ziel(int, Zielbedingung)

  prüft bei dem Modus 'maxTileOnField', ob die Entbedingung erfüllt wird.

  return: float
  '''
  x=cods[0]
  y=cods[1]
  if board[y][x]["tile_numb"] >= ziel:
    return True
  else:
    return False


def createRandom(board, numb=1, chance_enemy=0, chance_duplicate=0, chance_halve=0):
  '''
  Input: board: Spielfeld
         numb: Anzahl wie oft der Prozess wiederholt wird
         chance_enemy:int, Warscheinlichkeit, dass ein neues Tile ein Gegner ist. in Prozent
         chance_duplicate:int, Warscheinlichkeit, dass ein neues Tile eine *2- Platte ist.

  Gibt das Board, mit einer nach Zufall vrteilten Zahl 2 oder 4 an einer leeren Stelle aus
  '''
  for _ in range(numb):
    nullen = []
    blocked=[]
    nullen_in_blocked=[]
    if "blocked" in config.levels[config.current_level]:
      blocked=copy.deepcopy(config.levels[config.current_level]["blocked"])

    for zeile in range(len(board)):
      for spalte in range(len(board[zeile])):
        if board[zeile][spalte]["tile_numb"] == 0:
          if (spalte, zeile) in blocked:
            nullen_in_blocked.append((zeile,spalte))
          else:
            nullen.append((zeile, spalte))

    if nullen==[]:
      nullen=copy.deepcopy(nullen_in_blocked)
    rndm = random.randint(0, len(nullen) - 1)

    insert=copy.deepcopy(config.template_tile_dic)
    insert["tile_numb"]=random.choice([2, 4])
    rndm2=random.randint(1,100)
    if rndm2 <= chance_enemy:
      insert["fraction"] = "enemy"
    elif rndm2 <= chance_enemy+chance_duplicate:
      insert["tile_numb"]=-1
      insert["type"]="duplicate"
    elif rndm2 <= chance_enemy+chance_duplicate+chance_halve:
      insert["tile_numb"]=-1
      insert["type"]="halve"
    else:
      insert["fraction"] = "player"
    board[nullen[rndm][0]][nullen[rndm][1]] = insert

  return board


def buildBoard(x, y, anzahlnewrand=0):
  '''
  input: x(int,laenge x-Achse Matrix),
         y(int,laenge y-Achse Matrix),
         anzahlnewrand(int, gibt an, wieviele neue Zellen zuffällig befüllt werden sollen)

  baut eine Matrix anhand den x- und y Längen auf und füllt mit leeren Feldern, bzw. neuen 2en und vieren, der Anzahl 'anzahlnewrand'

  output:board(Matrix,Spielfeld mit 'anzahlnewrand' zufälligen zweien bzw. vieren)
  '''
  board = []
  for i in range(y):
    board.append([])
    for j in range(x):
      board[i].append(0)
  board = createRandom(board, anzahlnewrand)
  return board

def fillBoardWithDictionarys(board=config.board,aussnahmen={}):
  '''
  füllt ein board mit dem template dictionary, es sei denn eine Koordinate hat schon ein dictionary im außnahme dictionary
  return: Board, befüllt mit dictionarys
  '''
  for y in range(len(board)):
    for x in range(len(board[y])):
      if (x,y) in aussnahmen:
        board[y][x]=copy.deepcopy(aussnahmen[(x, y)])
      else:
        board[y][x]=copy.deepcopy(config.template_tile_dic)



  return board



def countScore(board):
  for i in board:
    for j in i:
      if j["tile_numb"] < -1:
        if j["fraction"] == "player":
          config.score+=j["tile_numb"]*-2
        elif j["fraction"] == "enemy":
          config.score += j["tile_numb"] * 2


#----------------------------------------------------------------------------------------------------------------------#
#Funktionen, die für den status des Spiels verantwortlich sind. Setzten Level aus, initialisieren, etc.


def initLevel(board):
  config.changed = True
  level_int=config.current_level
  level=config.levels[level_int]

  config.size = level["size"]
  config.size_in_between = level["size_in_between"]

  board=fillBoardWithDictionarys(board=board,aussnahmen=level["preset_tiles"])
  config.board = copy.deepcopy(level["board"])
  config.width = len(board[0])
  config.length = len(board)

  config.gamemode=level["gamemode"]
  if config.gamemode == "maxTile":
    config.maxWertTile=level["maxTile"]
  elif config.gamemode == "maxTileOnField":
    config.tile_ziel=level["tile_ziel"]
    for i in level["stay_on_floor_tiles"]:
      if level["stay_on_floor_tiles"][i]["type"]== "sieg-feld":
        config.ziel_feld_cods=i

  config.levelGoalText=level["level_text"]
  config.max_moves_per_move=level["max_moves_per_move"]

  config.yextra_top = config.size + config.size // 2 + 3 * config.size_in_between
  config.xmax = config.width * config.size + config.xextra + config.size_in_between * (
      config.width + 1)
  config.ymax = config.yextra_top + config.length * config.size + config.yextra + config.size_in_between * (
      config.length + 1)


  stay_floor = config.levels[config.current_level]["stay_on_floor_tiles"]
  for i in stay_floor:
    x = i[0]
    y = i[1]
    if board[y][x]["tile_numb"] <= 0:
      config.board[y][x] = copy.deepcopy(stay_floor[i])

  setup_surfaces_ui()
  config.score=0




#Zeichnen---------------------------------------------------------
def drawBoard(board,
              fenster,
              colors=config.colors,
              tile_surfs=config.tile_surfaces):
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
      recty = config.yextra_top + config.size_in_between * y + config.size * (y - 1)
      if tile["tile_numb"] != -1:

        if (str(tile["tile_numb"])+"_"+str(tile["fraction"])) in tile_surfs:
          fenster.blit(tile_surfs[str(tile["tile_numb"])+"_"+str(tile["fraction"])], (rectx, recty))
        else:
          config.tile_surfaces[str(tile["tile_numb"])+"_"+str(tile["fraction"])]=addTileSurf((str(tile["tile_numb"])+"_"+str(tile["fraction"])),config.size,config.size,"assets/fonts/ClearSans-Bold.ttf")
          fenster.blit(config.tile_surfaces[str(tile["tile_numb"]) + "_" + str(tile["fraction"])], (rectx, recty))
      else:
        fenster.blit(tile_surfs[str(tile["tile_numb"]) + "_" + str(tile["type"])], (rectx, recty))




def drawUIingame(fenster, colors=config.colors):
  '''
  Input: score(int, aktuelle Punktezahl), fenster(pygame.window)
  Zeichnet das Spielfeld in das Fenster
  '''
  level_goal_text = config.levelGoalText

  fenster.fill(colors.get("bg"))
  color="0_none"
  config.ui_bg_box.fill(config.colors.get("ui_bg"))
  config.score_txt_box.fill(config.colors.get(color))
  config.score_box.fill(config.colors.get(color))
  config.level_info_box.fill(config.colors.get(color))
  config.level_goal_box.fill(config.colors.get(color))


  draw_text_in_box(config.score_txt_box,"Score",max_fontsize=20)
  draw_text_in_box(config.score_box,str(config.score))
  draw_text_in_box(config.level_info_box,"Level "+str(config.current_level))
  draw_text_in_box(config.level_goal_box,level_goal_text, fact=0.95)

  fenster.blit(config.ui_bg_box,config.ui_bg_pos)
  fenster.blit(config.score_txt_box,config.score_txt_pos)
  fenster.blit(config.score_box, config.score_pos)
  fenster.blit(config.level_info_box, config.level_info_pos)
  fenster.blit(config.level_goal_box, config.level_goal_pos)





def drawUIHome(fenster, colors=config.colors):
  '''
  Zeichnet den Startbildschirm
  '''
  fenster.blit(config.bilder["startscreen"], (0, 0))


def drawOverworld(fenster, site):
  fenster.blit(config.bilder["overworld" + str(site)], (0, 0))
  if int(site) == 1:
    for i in config.clickpos_levelselect1:
      if i[1]!="Levelselect2" and i[1]!="unlock_all":
        if int(i[1][-2:]) <= config.best_level:
          fenster.blit(config.bilder["face1"], (i[0][0]-4,i[0][1]+40))
        else:
          if int(i[1][-2:]) != config.best_level+1:
            fenster.blit(config.bilder["lock"], (i[0][0]+12,i[0][1]+30))



def draw_text_in_box(surface,
                     text,
                     font="Arial",
                     max_fontsize=9999,
                     fraction="none",
                     colors={"color_none": (0, 0, 0),
                             "color_player":(255,255,255),
                             "color_enemy":(0,0,0),
                             "color_white":(244,244,244)},
                     fact=0.85):
  """
  Draws text in a box on the given surface.
  Make sure never exeeding the box's dimensions.
  Make sure to dar in the middle of the box.
  """
  fontsize = 0
  my_font = pygame.font.SysFont(font, fontsize)
  color=colors["color_"+str(fraction)]
  text_to_draw = my_font.render(str(text), True, color)
  text_width = text_to_draw.get_width()
  text_height = text_to_draw.get_height()
  while text_width < surface.get_width() * fact and text_height < surface.get_height() * fact:
    fontsize += 1
    my_font = pygame.font.SysFont(font, fontsize)
    text_to_draw = my_font.render(str(text), True, color)
    text_width = text_to_draw.get_width()
    text_height = text_to_draw.get_height()

  my_font = pygame.font.SysFont(font, min(int(fontsize), int(max_fontsize)) - 1)

  text_to_draw = my_font.render(str(text), True, color)
  text_width = text_to_draw.get_width()
  text_height = text_to_draw.get_height()
  surfheight = surface.get_height()
  surfwidth = surface.get_width()

  surface.blit(text_to_draw, (surfwidth / 2 - text_width / 2,
                             (surfheight / 2 - text_height / 2) + 3))


def konsolenAusgabe(board):
  for i in board:
    print(str(i))
  print("\n\n")


#---------------------------------------------------------------------------------------------------------------------#
#Init Zeichnen
def setup_tiles(width,
                heigth,
                tile_list=config.tile_list,
                colors=config.colors,
                font="assets/fonts/ClearSans-Bold.ttf",
                font_color=(255, 255, 255)):
  tiles = {}

  for tile in tile_list:
    tiles[tile] = addTileSurf(tile,width,heigth,font)

  return tiles

def draw_face_in_tile(surface,img_surf,width=config.width, heigth=config.width):
  scaled_img=pygame.transform.scale(img_surf, (width,width//4))
  surface.blit(scaled_img, (0,width-scaled_img.get_height()))


def setup_surfaces_ui():
  config.ui_bg_box=pygame.Surface((config.xmax, config.yextra_top))
  config.ui_bg_pos=((0,0))

  config.score_txt_box = pygame.Surface((config.size, config.size // 2))
  config.score_txt_pos = (config.size_in_between,config.size_in_between)

  config.score_box = pygame.Surface((config.size, config.size))
  config.score_pos = (config.size_in_between, config.size_in_between*2+config.size // 2)

  config.level_info_box = pygame.Surface(((config.width-1)*config.size+(config.width-2)*config.size_in_between, config.size//2))
  config.level_info_pos = (2*config.size_in_between+config.size, config.size_in_between)

  config.level_goal_box = pygame.Surface(((config.width-1)*config.size+(config.width-2)*config.size_in_between, config.size))
  config.level_goal_pos = (2 * config.size_in_between + config.size, config.size_in_between*2+config.size // 2)


def biggest_or_current_tile(tile):
  tile_numb = int(tile.split("_")[0])
  tile_frac = tile.split("_")[1]
  x=str(min(tile_numb,8192))+"_"+tile_frac
  return x

def addTileSurf(tile, width, heigth, font):
  tile_numb = int(tile.split("_")[0])
  tile_frac = tile.split("_")[1]
  tile_surf = pygame.Surface((width, heigth))
  tile_surf.fill(config.colors[biggest_or_current_tile(tile)])
  if tile_frac == "enemy":
    draw_face_in_tile(tile_surf, config.bilder.get("face_enemy"), width=width, heigth=heigth)
  if tile_frac == "duplicate":
    draw_text_in_box(tile_surf, "*2", font, fraction="white")
  if tile_frac == "halve":
    draw_text_in_box(tile_surf, ":2", font, fraction="white")

  if tile_frac == "sieg-feld":
    scaled_img = pygame.transform.scale(config.bilder.get("sieg-feld"), (width, heigth))
    tile_surf.blit(scaled_img, (0, 0))
  if tile_numb > 0:
    if tile_numb <= 4:
      draw_text_in_box(tile_surf, tile_numb, font, fraction="none")
    else:
      draw_text_in_box(tile_surf, tile_numb, font, fraction=tile_frac)
  else:  # besonderes Tile, z.B. Wand
    pass
  return tile_surf



