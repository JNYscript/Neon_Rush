import pygame

#set up the initial pygame window
pygame.init()
screen = pygame.display.set_mode([900,600])

#set background color
background = pygame.Surface(screen.get_size())
background.fill([204,255,229])
screen.blit(background, (0,0))

#Pull in the image to the program
my_image = pygame.image.load("google_logo.png")

#copy the image pixels to the screen
screen.blit(my_image, [x, y])

#Display changes
pygame.display.flip()

keys = {'right':False, 'up':False, 'left':False, 'down':False}
x = 0
y = 0
#set up pygame event loop
running = True
while running:
    screen.blit(my_image, [x, y])
    pygame.display.flip()
    for event in pygame.event.get():
        print event
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print "QUITTING NOW..."
                pygame.time.delay(2000)
                running = False
            if event.key == pygame.K_h:
                print "HELLO!"
                pygame.time.delay(2500)
                running = False
            if event.key == pygame.K_c:
                print "To move the original Google logo, use the arrow keys. To move the second logo, use the WASD keys."
            if event.key == pygame.K_RIGHT:
                keys['right'] = True
            if event.key == pygame.K_UP:
                keys['up'] = True
            if event.key == pygame.K_DOWN:
                keys['down'] = True
            if event.key == pygame.K_LEFT:
                keys['left'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                keys['right'] = False
            if event.key == pygame.K_UP:
                keys['up'] = False
            if event.key == pygame.K_DOWN:
                keys['down'] = False
            if event.key == pygame.K_LEFT:
                keys['left'] = False

        x = 0
        y = 0

        if keys['right']:
            x += 10
        if keys['up']:
            y += 10
        if keys['down']:
            y -=10
        if keys['left']:
            x -=10

pygame.quit()