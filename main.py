import pygame
from config import *
from logic import *


def inputLoop():
  global board, direction, status, running,lvls1
  # Abfrage von Events (Tastendruck / Mausklick)
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if status == "inGame":
        if event.key == pygame.K_UP:
          direction = 0

        if event.key == pygame.K_RIGHT:
          direction = 1

        if event.key == pygame.K_DOWN:
          direction = 2

        if event.key == pygame.K_LEFT:
          direction = 3
      elif status == "home":
        status = "overworldinit"

      elif status=="overworldinit":
        pass
      elif status=="overworld1":
        if event.key == pygame.K_RIGHT:
          status="overworld2"
      elif status=="overworld2":
        if event.key == pygame.K_LEFT:
          status = "overworld1"
        #if event.key == pygame.K_RIGHT:
        #  status="overworld3"
      elif status=="overworld3":
        pass

      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        quit()
      if event.key == pygame.K_SPACE:
        #print("space")
        pass

      if event.type == pygame.MOUSEBUTTONDOWN:
        pass
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()

    #if event.type == pygame.MOUSEBUTTONDOWN:
    #  if event.button == 1:  # Left mouse button.
    #    # Check if the rect collides with the mouse pos.
    #    for area in lvls1:
    #      if area.collidepoint(event.pos):
    #        print(str(area)+" clicked")


def logicLoop():
  '''
  Die Funktion logicLoop ist die Logikschleife des Spiels.
  '''
  global board, direction, changed, status, width, length, tile_surfaces

  if status == "homeInit":
    pass
  elif status == "overworldinit":
    pass
  elif status == "overworld1":#in Levelselect Seite 1
    pass
  elif status == "overworld2":#in Levelselect Seite2
    pass

  elif status == "gameInit":  #Erstes mal im Spiel
    board = initGame(width, length, 2)
    tile_surfaces=setup_tiles(size,size)


  elif status == "inGame":  #aktuell im Spiel
    if bewegung_moeglich_generell(board) == False:
      status = "gameOver"
    elif maxWert(board) == maxWertTile:
      status = "sieg"
    if direction >= 0:  #Wenn Pfeiltaste gedrückt ist
      if bewegungMoeglichSpeziell(board, direction) == True:
        board = move(board, direction)
        board = createRandom(board)
        changed = True

    direction = -1




def drawLoop():
  '''
  Die Funktion drawLoop ist die Zeichnungsschleife des Spiels.
  '''
  global board, changed, status, window, overworldWidth, overworldHeight, lvls1, lvls2
  if status == "homeInit":
    window = pygame.display.set_mode((homeWidth, homeHeight))
    pygame.display.set_caption('Battlemerge-A 2048 Game')
    drawUIHome(window)
    status = "home"

  elif status == "home":
    pass
  elif status == "overworldinit":
    window = pygame.display.set_mode((overworldWidth, overworldHeight))
    status="overworld1"
  elif status == "overworld1":
    drawOverworld(window,1,lvls1)
  elif status == "overworld2":
    drawOverworld(window,2, lvls2)
  elif status == "gameInit":
    window = pygame.display.set_mode((xmax, ymax))
    status = "inGame"
  elif status == "inGame":
    if changed:
      #konsolenAusgabe(board)
      changed = False

      #Zeichnet das Spiel
      drawUIingame(score, highscore, window)
      drawBoard(board, window,tile_surfs=tile_surfaces)

  pygame.display.flip()


#---------------------------------------------------------------------------------------------#
pygame.init()
# Fenster erzeugen

while running:
  inputLoop()
  logicLoop()
  drawLoop()
