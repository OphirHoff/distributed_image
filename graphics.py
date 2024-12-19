import pygame
import io
from PIL import Image
import numpy as np

WINDOW_WIDTH = 50
WINDOW_HEIGHT = 50

X = 1
Y = 0

class ImageLoad:
    def pillow_to_pygame(pil_image):
        """
        Converts a Pillow image object to a Pygame image object.
        
        :param pil_image: A Pillow Image object.
        :return: A Pygame Surface object representing the image.
        """
        # Save the Pillow image to an in-memory byte buffer
        with io.BytesIO() as byte_io:
            pil_image.save(byte_io, format='png')
            byte_io.seek(0)  # Reset pointer to the beginning of the buffer
            pygame_image = pygame.image.load(byte_io)
        return pygame_image

    def load_pic_arr(img_name: str):
        """Load picture from module directory to np array."""
        with Image.open(img_name) as img:
            return np.array(img)
        
    def img_pillow_from_arr(arr: np.ndarray):
        return Image.fromarray(arr)

    def show_img_from_arr(arr: np.ndarray):
        Image.fromarray(arr).show()


class Graphics:

    def __init__(self, size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
        self.size = size
        self.screen = None
        self.bg_obj: pygame.image = None
        self.pieces = None
        self.start_pos = [40, 40]
        self.end_pos = [90, 90]

    def update_bg(self, new_bg: Image):
        self.bg_obj = ImageLoad.pillow_to_pygame(new_bg)

    def set_bg_from_pieces(self):
        
        if len(self.pieces) >= 1 and self.pieces[0]:
            pic_one = (0, 0)
            self.screen.blit(ImageLoad.pillow_to_pygame(self.pieces[0]), pic_one)
        if len(self.pieces) >= 2 and self.pieces[1]:
            pic_two = (self.pieces[0].size[0] + 1, 0)
            self.screen.blit(ImageLoad.pillow_to_pygame(self.pieces[1]), pic_two)
        if len(self.pieces) >= 3 and self.pieces[3]:
            pic_four = (0, self.pieces[0].size[1] + 1)
            self.screen.blit(ImageLoad.pillow_to_pygame(self.pieces[3]), pic_four)
        if len(self.pieces) >= 2 and self.pieces[2]:
            pic_three = (self.pieces[3].size[0], self.pieces[1].size[1])
            self.screen.blit(ImageLoad.pillow_to_pygame(self.pieces[2]), pic_three)


    def start(self):

        pygame.init()
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")

        finish = False
        while not finish:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True

                keys = pygame.key.get_pressed()


                if keys[pygame.K_DOWN]:
                    self.start_pos[Y] += 1
                    self.end_pos[Y] += 1
                elif keys[pygame.K_UP]:
                    self.start_pos[Y] -= 1
                    self.end_pos[Y] -= 1

            
                self.set_bg_from_pieces()
            pygame.display.flip()

        pygame.quit()