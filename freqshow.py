import os
import time

import pygame

import controller
import model
import ui


# Application configuration.
SDR_SAMPLE_SIZE = 1024	# Number of samples to grab from the radio.  Should be
						# larger than the maximum display width.

CLICK_DEBOUNCE  = 0.4	# Number of seconds to wait between clicks events. Set
						# to a few hunded milliseconds to prevent accidental
						# double clicks from hard screen presses.

# Font size configuration.
MAIN_FONT = 33
NUM_FONT  = 50

# Color configuration (RGB tuples, 0 to 255).
MAIN_BG        = (  0,   0,   0) # Black
INPUT_BG       = ( 60, 255, 255) # Cyan-ish
INPUT_FG       = (  0,   0,   0) # Black
CANCEL_BG      = (128,  45,  45) # Dark red
ACCEPT_BG      = ( 45, 128,  45) # Dark green
BUTTON_BG      = ( 60,  60,  60) # Dark gray
BUTTON_FG      = (255, 255, 255) # White
BUTTON_BORDER  = (200, 200, 200) # White/light gray
INSTANT_LINE   = (  0, 255, 128) # Bright yellow green.

# Define gradient of colors for the waterfall graph.  Gradient goes from blue to
# yellow to cyan to red.
WATERFALL_GRAD = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 0)]

# Configure default UI and button values.
ui.MAIN_FONT = MAIN_FONT
ui.Button.fg_color     = BUTTON_FG
ui.Button.bg_color     = BUTTON_BG
ui.Button.border_color = BUTTON_BORDER
ui.Button.padding_px   = 2
ui.Button.border_px    = 2


if __name__ == '__main__':
	# Initialize pygame and SDL to use the PiTFT display and touchscreen.
	#os.putenv('SDL_VIDEODRIVER', 'fbcon')
	os.putenv('SDL_FBDEV'      , '/dev/fb1')
	#os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
	#os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
	pygame.display.init()
	pygame.font.init()
	pygame.mouse.set_visible(False)
	# Get size of screen and create main rendering surface.
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	#size = (800,450)
	#screen = pygame.display.set_mode(size)
	# Display splash screen.
	splash = pygame.image.load('freqshow_splash.png')
	screen.fill(MAIN_BG)
	screen.blit(splash, ui.align(splash.get_rect(), (0, 0, size[0], size[1])))
	pygame.display.update()
	splash_start = time.time()
	# Create model and controller.
	fsmodel = model.FreqShowModel(size[0], size[1])
	fscontroller = controller.FreqShowController(fsmodel)
	time.sleep(0.1)
	# Main loop to process events and render current view.
	lastclick = 0
	while True:
		# Process any events (only mouse events for now).
		for event in pygame.event.get():
			print(event.type)
			if event.type is pygame.MOUSEBUTTONDOWN or event.type == 1792:
				#and (time.time() - lastclick) >= CLICK_DEBOUNCE:
				x = event.x * size[0]
				y = event.y * size[1]
				lastclick = time.time()
				print(event)
				#fscontroller.current().click(pygame.mouse.get_pos())
				fscontroller.current().click((x,y))
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				print(pos)
				fscontroller.current().click(pygame.mouse.get_pos())
		# Update and render the current view.
		fscontroller.current().render(screen)
		pygame.display.update()
