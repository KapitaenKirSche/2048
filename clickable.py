import pygame


class ClickableSprite(pygame.sprite.Sprite):

  def __init__(self, window, x, y, w, h, color, click_func):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([w, h])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.click_func = click_func
    self.color = color
    self.window = window

  # Wenn der Sprite angeklit wird, wird die Funktion aufgerufen,
  #   # sie ändert die Farbe des Spckrites
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.change_color((255, 255, 0))

  def zeichne(self):
    pygame.draw.rect(self.window, self.color, self.rect)

  def change_color(self, color):
    self.color = color
