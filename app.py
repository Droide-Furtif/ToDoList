import pygame
import sys
from button_class import *

class App:

    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((486, 981)) # Phone equivalent
        pygame.display.set_caption("To-Do List")
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()

        # App variables
        self.running = True
        self.clock = pygame.time.Clock()

        # Buttons
        self.buttonList = [
            Button(self, "save_button", 364 - 75, 67),
            Button(self, "add_container_button", 122, 67),
        ]
        self.buttonList[0].setImage(pygame.image.load('img/save_icon.png').convert_alpha())
        self.buttonList[1].setImage(pygame.image.load('img/add_cross.png').convert_alpha())

        self.containerList = []
        self.container_list_starting_y = 180

        # Loading images
        self.background_img = pygame.image.load('img/background.png')
        self.background_img = pygame.transform.scale(self.background_img, (self.screenWidth, self.screenHeight +48))
        self.button_background_img = pygame.image.load('img/buttons_background.png')
        self.todo_text_img = pygame.image.load('img/todo_text.png').convert_alpha()


    # Method to read save file
    def start(self):
        with open("appdata/save.txt") as file:
            lines = file.readlines()
            file.close()
            print(lines)
            for line in lines:
                x=int(line[:3])
                y=int(line[3:6])
                checked = True if line[6] == 'T' else False
                text = line[7:-1:]
                self.containerList.append(Container(self, x, y, checked, text))

    # Method to write to save file
    def save(self):
        savelines = []
        # Container code : XXXYYYCtext (x and y as 3 digits; Checked as T or F; and inputted text
        for c in self.containerList:
            check = 'T' if c.checkbox.checked else 'F'
            text = c.text_prompt.text
            print(f"{c.x:03d}{c.y:03d}{check}{text}")
            savelines.append(f"{c.x:03d}{c.y:03d}{check}{text}\n")
        # Write lines to file (overwrite) and closes file
        with open("appdata/save.txt", 'w') as file:
            file.writelines(savelines)
            file.close()

    # App loop
    def loop(self):
        while self.running:
            # Updates all buttons and containers
            for b in self.buttonList:
                b.update()
            for c in self.containerList:
                c.update()
            self.checkEvents()
            self.draw()
            self.clock.tick(30)

    # Draw Method
    def draw(self):
        self.drawBackground()
        for b in self.buttonList:
            b.draw()
        for c in self.containerList:
            c.draw()
        pygame.display.flip()

    # Draws background
    def drawBackground(self):
        self.screen.fill("#000000")
        self.screen.blit(self.background_img, (0,-24))
        self.screen.blit(self.button_background_img, (99, 44))
        self.screen.blit(self.todo_text_img, (203, 58))


    # Event manager
    def checkEvents(self):
        # Pygame Events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

        # Buttons Events
        self.buttonEvents()
    
    # Buttons Events
    def buttonEvents(self):
        for b in self.buttonList:
            if b.isClicked("save_button"):
                print("Writing to save file :")
                self.save()
            if b.isClicked("add_container_button"):
                self.containerList.append(Container(self, 26, len(self.containerList) *65 + 350))