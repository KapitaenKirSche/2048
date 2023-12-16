import pygame
import config as cfg
from logic import *


def inputLoop():
  #global board, direction, status, running, clickpos_levelselect1
  # Abfrage von Events (Tastendruck / Mausklick)
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if cfg.status == "inGame":
        if event.key == pygame.K_UP:
          cfg.direction = 0

        if event.key == pygame.K_RIGHT:
          cfg.direction = 1

        if event.key == pygame.K_DOWN:
          cfg.direction = 2

        if event.key == pygame.K_LEFT:
          cfg.direction = 3
      elif cfg.status == "home":
        cfg.status = "overworldinit"

      elif cfg.status == "overworldinit":
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

      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        quit()
      if event.key == pygame.K_SPACE:

        pass
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

    if cfg.status == "overworld1":
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button.

          for area in cfg.clickpos_levelselect1:
            if area[0].collidepoint(event.pos):

              if area[1] == "Levelselect2":
                cfg.status = "overworld2"
              elif "Level" in area[1]:
                cfg.status = str(area[1]).lower() + "Init"


def logicLoop():
  '''
  Die Funktion logicLoop ist die Logikschleife des Spiels.
  '''
  #global board, direction, changed, status, width, length, tile_surfaces, boards

  if cfg.status == "homeInit":
    pass
  elif cfg.status == "overworldinit":
    pass
  elif cfg.status == "overworld1":  #in Levelselect Seite 1
    pass
  elif cfg.status == "overworld2":  #in Levelselect Seite2
    pass

  elif cfg.status == "level1Init":
    initLevel(cfg.boards.get("level1"))



  elif cfg.status == "gameInit":  #Erstes mal im Spiel
    #board = buildBoard(width, length, 2)
    cfg.tile_surfaces = setup_tiles(cfg.size, cfg.size)

  elif cfg.status == "inGame":  #aktuell im Spiel
    if bewegung_moeglich_generell(cfg.board) == False:
      cfg.status = "gameOver"
    elif maxWert(cfg.board) == cfg.maxWertTile:
      cfg.status = "sieg"
    if cfg.direction >= 0:  #Wenn Pfeiltaste gedrückt ist
      if bewegungMoeglichSpeziell(cfg.board, cfg.direction) == True:
        cfg.board = move(cfg.board, cfg.direction)
        cfg.board = createRandom(cfg.board)
        cfg.changed = True

    cfg.direction = -1


def drawLoop():
  '''
  Die Funktion drawLoop ist die Zeichnungsschleife des Spiels.
  '''
  #global board, changed, status, window, overworldWidth, overworldHeight, clickpos_levelselect1
  global window
  if cfg.status == "homeInit":
    window = pygame.display.set_mode((cfg.homeWidth, cfg.homeHeight))
    pygame.display.set_caption('Battlemerge-A 2048 Game')
    drawUIHome(window)
    cfg.status = "home"

  elif cfg.status == "home":
    pass
  elif cfg.status == "overworldinit":
    window = pygame.display.set_mode((cfg.overworldWidth, cfg.overworldHeight))
    cfg.status = "overworld1"
  elif cfg.status == "overworld1":
    drawOverworld(window, 1)
  elif cfg.status == "overworld2":
    drawOverworld(window, 2)

  elif cfg.status == "level1Init":
    cfg.status = "gameInit"

  elif cfg.status == "gameInit":
    window = pygame.display.set_mode((cfg.xmax, cfg.ymax))
    cfg.status = "inGame"
  elif cfg.status == "inGame":
    if cfg.changed:
      #konsolenAusgabe(cfg.board)
      cfg.changed = False

      #Zeichnet das Spiel
      drawUIingame(cfg.score, cfg.highscore, window)
      drawBoard(cfg.board, window, tile_surfs=cfg.tile_surfaces)

  pygame.display.flip()


#---------------------------------------------------------------------------------------------#
pygame.init()
# Fenster erzeugen

while cfg.running:
  inputLoop()
  logicLoop()
  drawLoop()
