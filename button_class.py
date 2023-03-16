import pygame
import time

def blit_text(surface, text, pos, font, color=pygame.Color('#682b14')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    max_width -= 80
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# BUTTON CLASS PARENT
class Button:
    def __init__(self, app, name, x=0, y=0, w=60,h=60):
        self.app = app
        self.name = name
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x,y,w,h)
        self.image = None
        self.clickedOnce = False
        self.color = 'White'

    def draw(self):
        if self.image is None:
            pygame.draw.rect(self.app.screen, self.color, pygame.Rect(self.x,self.y,self.width,self.height), 4)
        else:
            self.app.screen.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    # Checks if cursor is hovering over button's rect
    def isHovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    # Checks if button is held down
    def isPressed(self):
        return self.isHovered() and pygame.mouse.get_pressed()[0]

    #Checks if button is clicked once, need to release to "reset"
    def isClicked(self, name=""):
        # if given, checks if btn name equals argument given
        if name == "":
            pass
        else:
            if self.name != name:
                return False
        # if pressed, return true once and change clickedOnce to false until not pressed anymore
        if self.isPressed():
            if not self.clickedOnce:
                self.clickedOnce = True
                return True
            else:
                return False
        else:
            self.clickedOnce = False
            return False

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.w = self.width
        self.rect.h = self.height

    def setImage(self, img):
        self.image = img

# CHECKBOX CLASS
class Checkbox(Button):
    def __init__(self, app, x=0, y=0, w=50,h=50):
        super().__init__(app, x , y, w, h)
        self.checked = False
        self.image = pygame.image.load('img/button_border.png').convert_alpha()
        self.check_image = pygame.image.load('img/check.png').convert_alpha()

    def update(self):
        self.rect.y = self.y
        if self.isClicked(self.name):
            self.checked = not self.checked

    def draw(self):
        super().draw()
        if self.checked == True:
            self.app.screen.blit(pygame.transform.scale(self.check_image, (self.width/2, self.height/2)), (self.x+13, self.y+15))
        else:
            pass

class TextInput(Button):
    def __init__(self, app, name="", text="", x=0, y=0, w=354, h=60):
        super().__init__(app, name, x, y, w, h)
        self.text = text
        self.finalText = ""
        self.isActive = False
        self.image = pygame.image.load("img/text_zone.png")
        self.color = 'Green'
        self.background_color = 'Dark Green'
        self.text_color = '#682b14'
        self.font = pygame.font.Font('fonts/prototype.ttf', 20)
        self.txt_surface = self.font.render(self.text, True, self.text_color)
        self.isCorrecting = False

    # Draw Method
    def draw(self):
        super().draw()
        if self.image is None:
            pygame.draw.rect(self.app.screen, self.background_color, pygame.Rect(self.x+4, self.y+4, self.width-8, self.height-8))
        else:
            pass
        #blit_text(self.app.screen, self.text, (self.x + 15, self.y + 4), pygame.font.Font('fonts/prototype.ttf', 18))
        self.app.screen.blit(self.txt_surface, (self.x + 18, self.y + 16))



    # Update Method, set prompt active if hovered, rescale if needed, get input
    def update(self):
        self.isActive = self.isHovered()
        #self.width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = self.width
        self.rect.y = self.y
        self.background_color = '#235443' if self.isActive else 'Dark Green'
        if self.isActive:
            self.getInput()


    # Read input, manage backspace and enter
    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.finalText = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.text_color)

# Basic layout with a checkbox and a text input
class Container:
    def __init__(self, app, x, y, checked = False, text = ""):
        self.app = app
        self.margin = 65
        self.x = x
        self.y = y
        self.checkbox = Checkbox(app, "", self.x, y)
        self.text_prompt = TextInput(app, "", text, self.x+self.checkbox.width -2, y)
        self.checkbox.checked = checked
        self.remove_button = Button(app, "", self.x+250, y, 30, 30)
        self.remove_button_offset = 14
        self.remove_button.setImage(pygame.image.load("img/delete_cross.png").convert_alpha())

    def draw(self):
        self.checkbox.draw()
        self.text_prompt.draw()
        self.remove_button.draw()

    def update(self):
        # Buttons logic
        self.checkbox.update()
        self.text_prompt.update()
        self.remove_button.update()
        if self.remove_button.isClicked():
            self.app.containerList.remove(self)
            self.app.draw()
            time.sleep(0.3)
        # Position update
        for i, c in enumerate(self.app.containerList):
            # if container isn't first in list, move it to match if it isn't 50pxl below the one above
            if c == self and i != 0:
                if self.app.containerList[i-1].y < self.y - self.margin:
                    self.y = self.app.containerList[i-1].y + self.margin
            # if c is first in list, move it if it's not at starting pos (Y350)
            elif c == self and i == 0:
                if self.y > self.app.container_list_starting_y:
                    self.y = self.app.container_list_starting_y
        self.checkbox.y = self.y
        self.text_prompt.y = self.y
        self.remove_button.y = self.y + self.remove_button_offset
        self.remove_button.x = self.x + self.checkbox.width + self.text_prompt.width +2