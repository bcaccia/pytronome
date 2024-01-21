import pygame
import time
pygame.init()

my_sound = pygame.mixer.Sound('sounds/MetroBar1.wav')

i = 0

while i < 5: 
	my_sound.play()
	time.sleep(0.07)
	i+= 1
