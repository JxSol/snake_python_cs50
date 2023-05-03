import sys
import abc
from collections import defaultdict

import pygame
from random import randrange

import game_objects as go
import settings as stg


class Game(abc.ABC):
    """ Abstract game class. """
    def __init__(
            self,
            caption: str,
            window_width: int,
            window_height: int,
            frame_rate: int,
            back_image_filename: str | None = None,
            background_color: go.ColorValue = (0, 0, 0)
    ):
        """ Game initialization.

        Args:
            caption: str:
                The title of the game window.
            window_width: int:
                Game window width.
            window_height: int:
                Game window height.
            frame_rate: int:
                Game window frame rate.
            back_image_filename: str | None:
                Background image filename.
            background_color: ColorValue:
                Background color value.
        """
        self.back_image = False
        if back_image_filename:
            self.background = pygame.image.load(back_image_filename)
            self.back_image = True
        else:
            self.background = background_color
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        self.score = 0

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.collision_handlers = {}

    def update(self, dt):
        """Update all the objects."""
        for o in self.objects:
            o.update(dt)

    def draw(self):
        """Draw all the objects."""
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        """Event handling."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in stg.KEYS.values():
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
                pygame.event.clear()
                break
            # elif event.type == pygame.KEYUP:
            #     for handler in self.keyup_handlers[event.key]:
            #         handler(event.key)

    @abc.abstractmethod
    def handle_collisions(self):
        """Collision handling."""
        pass

    def update_background(self):
        if self.back_image:
            self.surface.blit(self.background, (0, 0))
        else:
            self.surface.fill(self.background)

    def run(self):
        """ Main game cycle. """
        dt = 0.1
        while not self.game_over:
            self.update_background()

            self.handle_collisions()
            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.update()
            dt = self.clock.tick(self.frame_rate) / 1000

    def finish(self):
        self.game_over = True


class SnakeGame(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snake = go.Snake(
            stg.SNAKE_INIT_X,
            stg.SNAKE_INIT_Y,
            color=stg.RGB['SNAKE'],
            offset=(stg.WINDOW_WIDTH, stg.WINDOW_HEIGHT),
            speed=stg.SNAKE_SPEED,
            length=stg.SNAKE_INIT_LENGTH,
        )
        self.apple = go.Apple(
            randrange(0,
                      stg.WINDOW_WIDTH - stg.GRID_SIZE,
                      stg.GRID_SIZE),
            randrange(0,
                      stg.WINDOW_HEIGHT - stg.GRID_SIZE,
                      stg.GRID_SIZE),
            offset=(stg.WINDOW_WIDTH, stg.WINDOW_HEIGHT),
            color=stg.RGB['APPLE'],
        )
        # Fill objects list
        self.objects.append(self.snake)
        self.objects.append(self.apple)
        # Fill keys handlers
        self.keydown_handlers[stg.KEYS['LEFT']].append(self.snake.head.handle)
        self.keydown_handlers[stg.KEYS['RIGHT']].append(self.snake.head.handle)
        self.keydown_handlers[stg.KEYS['UP']].append(self.snake.head.handle)
        self.keydown_handlers[stg.KEYS['DOWN']].append(self.snake.head.handle)
        # Fill collision handlers
        self.collision_handlers['apple'] = self.get_apple
        self.collision_handlers['wall'] = self.finish

    def get_apple(self):
        while self.snake.colliderect(self.apple.bounds):
            self.apple.respawn()
        self.snake.got_apple = True
        self.score += 1


    def check_apple_snake_collision(self) -> bool:
        for obj in self.objects:
            if isinstance(obj, go.Apple) \
                    and obj.bounds.colliderect(self.snake.head.bounds):
                return True
        return False

    def handle_collisions(self) -> str | None:
        if self.snake.check_collision():
            self.collision_handlers['wall']()
        if self.check_apple_snake_collision():
            self.collision_handlers['apple']()
        return None



if __name__ == '__main__':
    new_game = SnakeGame(
        stg.GAME_NAME,
        stg.WINDOW_WIDTH,
        stg.WINDOW_HEIGHT,
        stg.GLOBAL_FPS
    )
    new_game.run()
