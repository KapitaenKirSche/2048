from pygame import Surface

from aufgabe1.grafik import draw_text_in_box


def test1(screen: Surface):
    dimensions = [100, 200, 300, 400, 500]
    top = 10
    margin = 10
    for d in dimensions:
        sf1 = Surface((d, d / 4))
        sf1.fill((255, 255, 255))
        draw_text_in_box(sf1, "Hello Pygame World!")
        screen.blit(sf1, (margin, top))
        top = int(top + (d / 4) + margin)

