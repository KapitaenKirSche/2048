import pygame
import config as cfg
from timer import Timer
from logic import *


def inputLoop():
  #global board, direction, status, running, clickpos_levelselect1
  # Abfrage von Events (Tastendruck / Mausklick)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
    if event.type == pygame.KEYDOWN:

      #status
      if cfg.status == "inGame":
        if event.key == pygame.K_UP:
          cfg.direction = 0

        if event.key == pygame.K_RIGHT:
          cfg.direction = 1

        if event.key == pygame.K_DOWN:
          cfg.direction = 2

        if event.key == pygame.K_LEFT:
          cfg.direction = 3

        if event.key == pygame.K_ESCAPE:
          cfg.status = "gameOverInit"


      #Homescreen
      elif cfg.status == "home":
        cfg.status = "overworldInit"

      #overworld
      elif cfg.status == "overworldInit":
        pass
      elif cfg.status == "overworld1":
        if event.key == pygame.K_RIGHT:
          cfg.status = "overworld2"
      elif cfg.status == "overworld2":
        if event.key == pygame.K_LEFT:
          cfg.status = "overworld1"
        # if event.key == pygame.K_RIGHT:
        #  cfg.status="overworld3"
      elif cfg.status == "overworld3":
        pass


      elif cfg.status == "sieg" or cfg.status == "gameOver":
        cfg.status = "overworldInit"





    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  #linke Maustaste

        if cfg.status == "overworld1":
          for area in cfg.clickpos_levelselect1:
            if area[0].collidepoint(event.pos):

              if area[1] == "Levelselect2":
                cfg.status = "overworld2"
              elif area[1] == "unlock_all":
                cfg.best_level=99
              elif "Level" in area[1]:
                cfg.status = str(area[1]).lower() + "Init"

        elif cfg.status == "overworld2":
          for area in cfg.clickpos_levelselect2:
            if area[0].collidepoint(event.pos):

              if area[1] == "Levelselect1":
                cfg.status = "overworld1"
              elif "Level" in area[1]:
                cfg.status = str(area[1]).lower() + "Init"


def logicLoop():
  '''
  Die Funktion logicLoop ist die Logikschleife des Spiels.
  '''
  #global board, direction, changed, status, width, length, tile_surfaces, boards



  #Status des Spiels--------------------------------------
  #Overworld
  if cfg.status == "homeInit":
    pass
  elif cfg.status == "overworldInit":
    pass
  elif cfg.status == "overworld1":  #in Levelselect Seite 1
    pass
  elif cfg.status == "overworld2":  #in Levelselect Seite2
    pass

  #LevelxInit
  elif "level" in cfg.status:
    if "Init" in cfg.status:
      cfg.current_level=int(cfg.status[5:7])
      if cfg.current_level <= cfg.best_level+1 or cfg.current_level >20:
        initLevel(cfg.levels[cfg.current_level]["board"])
      else:
        if cfg.current_level <= 20:
          cfg.status="overworld1"
        else:
          cfg.status="overworld2"
        cfg.current_level = 0


  elif cfg.status == "gameInit":  #Erstes mal im Spiel (dem richtigen Spiel, nicht homescreen)
    cfg.tile_surfaces = setup_tiles(cfg.size, cfg.size)


  # aktuell im Spiel
  elif cfg.status == "inGame":
    if bewegung_moeglich_generell(cfg.board, cfg.levels[cfg.current_level]["max_moves_per_move"]) == False:
      cfg.status = "gameOverInit"
      cfg.current_level=0

    if cfg.gamemode=="maxTile":
      if biggestTile(cfg.board) == cfg.maxWertTile:
        cfg.status = "siegInit"
    elif cfg.gamemode=="maxTileOnField":
      if check_sieg_feld(cfg.ziel_feld_cods, cfg.board, cfg.tile_ziel):
        cfg.status = "siegInit"


    if cfg.direction >= 0:  #Wenn Pfeiltaste gedrückt ist
      if bewegungMoeglichSpeziell(cfg.board, cfg.direction,maxim=cfg.max_moves_per_move) == True:
        cfg.board = move(cfg.board, cfg.direction,maxim=cfg.max_moves_per_move)
        cfg.board = createRandom(cfg.board,chance_enemy=cfg.levels[cfg.current_level]["chance_enemy_spawn"],chance_duplicate=cfg.levels[cfg.current_level]["chance_duplicate_spawn"], chance_halve=cfg.levels[cfg.current_level]["chance_halve_spawn"])
        cfg.changed = True

    cfg.direction = -1


def drawLoop():
  '''
  Die Funktion drawLoop ist die Zeichnungsschleife des Spiels.
  '''
  global window, timer
  if cfg.status == "homeInit":
    window = pygame.display.set_mode((cfg.homeWidth, cfg.homeHeight))
    pygame.display.set_caption('Battlemerge-A 2048 Game')
    drawUIHome(window)
    cfg.status = "home"

  elif cfg.status == "home":
    pass
  elif cfg.status == "overworldInit":
    window = pygame.display.set_mode((cfg.overworldWidth, cfg.overworldHeight))
    cfg.status = "overworld1"
  elif cfg.status == "overworld1":
    drawOverworld(window, 1)
  elif cfg.status == "overworld2":
    drawOverworld(window, 2)


  elif "level" in cfg.status:
    if "Init" in cfg.status:
      cfg.status = "gameInit"

  elif cfg.status == "gameInit":
    window = pygame.display.set_mode((cfg.xmax, cfg.ymax))
    cfg.status = "inGame"

  elif cfg.status == "inGame":
    if cfg.changed:
      cfg.changed = False

      #Zeichnet das Spiel
      drawUIingame(window)
      drawBoard(cfg.board, window, tile_surfs=cfg.tile_surfaces)

  elif cfg.status == "gameOverInit":
    if cfg.timer_set != True:
      timer=Timer(900)
      cfg.timer_set = True
    else:
      if timer.wait():
        window = pygame.display.set_mode((cfg.goWidth, cfg.goHeight))
        cfg.status = "gameOver"
        cfg.timer_set = False


  elif cfg.status == "siegInit":
    if cfg.timer_set != True:
      timer = Timer(900)
      cfg.timer_set = True
    else:
      if timer.wait():
        window = pygame.display.set_mode((cfg.siegWidth, cfg.siegHeight))
        if cfg.current_level <=20:
          cfg.best_level = max(cfg.best_level, cfg.current_level)
        cfg.current_level = 0
        cfg.status="sieg"
        cfg.timer_set = False


  elif cfg.status == "gameOver":
    window.blit(config.bilder["gameover1"], (0, 0))


  elif cfg.status == "sieg":
    window.blit(config.bilder["win1"], (0, 0))


  pygame.display.flip()


#---------------------------------------------------------------------------------------------#
pygame.init()
# Fenster erzeugen

while cfg.running:
  inputLoop()
  logicLoop()
  drawLoop()
