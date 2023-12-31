import pygame
class Timer :
    current=0
    def __init__(self, timeout=1000):
        self.current = pygame.time.get_ticks()
        self.timeout = self.current+timeout
        self.visited=False

    def wait(self):
        return pygame.time.get_ticks()>=self.timeout

    def wait_once(self):
        if self.visited :
            return False
        else :
            result = pygame.time.get_ticks()>=self.timeout
            if result :
                self.visited = True
            return result

    def reset(self,timeout=1000):
        self.__init__(timeout=timeout)