import pygame
tile_list=[2,4,8,16,32,64,128,256,512,1024,2048]
def draw_text_in_box(surface, text, font="Arial", color=(0, 0, 0),    fact = 0.5):
    """
    Draws text in a box on the given surface.
    Make sure never exeeding the box's dimensions.
    Make sure to dar in the middle of the box.

    """
    fontsize=0
    my_font=pygame.font.SysFont(font,fontsize)
    text_to_draw = my_font.render(str(text), True, color)
    text_width = text_to_draw.get_width()
    text_height = text_to_draw.get_height()
    while text_width < (surface.get_width()*fact) and text_height < (surface.get_height()*fact):
        fontsize += 1
        my_font = pygame.font.SysFont(font, fontsize)
        text_to_draw = my_font.render(str(text), True, color)
        text_width = text_to_draw.get_width()
        text_height = text_to_draw.get_height()
    my_font = pygame.font.SysFont(font, fontsize-1)
    text_to_draw = my_font.render(str(text), True, color)
    text_width = text_to_draw.get_width()
    text_height = text_to_draw.get_height()
    surfheight=surface.get_height()
    surfwidth=surface.get_width()
    surface.blit(text_to_draw,(surfwidth / 2 - text_width / 2,
                               surfheight/ 2 - text_height / 2))

