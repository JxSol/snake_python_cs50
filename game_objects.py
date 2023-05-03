import abc
from random import randrange
from typing import Callable, Tuple, Union, Sequence, NoReturn

import pygame
from pygame import Surface, Color
from pygame.rect import Rect

import settings as stg

# Typehints
RGBAOutput = Tuple[int, int, int, int]
Key = int
ColorValue = Union[
    Color,
    int,
    str,
    Tuple[int, int, int],
    RGBAOutput,
    Sequence[int]
]


class GameObject(abc.ABC):
    """Game object abstract class."""

    def __init__(
            self,
            x: int, y: int,
            color: ColorValue,
            offset: Tuple[int, int],
            w: int = stg.GRID_SIZE, h: int = stg.GRID_SIZE,
            step_size: int = stg.GRID_SIZE,
            speed: int = 0,
            direction: int = 2,
    ):
        """Game object initialization.

        Args:
            x: int:
                Horizontal position of the object.
            y: int:
                Vertical position of the object.
            color: ColorValue:
                Object's color
            offset: Tuple[int, int]:
                Maximal x and y positions.
            w: int (default = GRID_SIZE):
                Object's width.
            h: int (default = GRID_SIZE):
                Object's height.
            step_size: int (default = GRID_SIZE):
                Represents a movement distance in pixels.
            speed: int (default = 0):
                Represents the value of steps per second.
            direction: int (default = 2):
                Direction of the object.

        Directions:
            0: UP,
            1: RIGHT,
            2: DOWN,
            3: LEFT,
        """
        self.bounds = Rect(x, y, w, h)
        self.color = color
        self.offset = offset
        self.speed = speed
        self.direction = direction
        self.step_size = step_size

    @staticmethod
    def get_velocity(direction: int,
                     speed: int,
                     step_size: int = stg.GRID_SIZE
                     ) -> Tuple[int, int]:
        """Returns the velocity vector of the object."""
        dx = round(direction % 2
                   * (-1) ** ((direction % 3) == 0)
                   * step_size)
        dy = round((direction + 1) % 2
                   * (-1) ** ((direction % 3) == 0)
                   * step_size)
        return dx, dy

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    @abc.abstractmethod
    def draw(self, surface: Surface) -> NoReturn:
        """Draw shape of the object to a surface."""
        pass

    def move(self, dx: int, dy: int) -> NoReturn:
        """Change object's coordinates by a given distance."""
        self.bounds = self.bounds.move(dx, dy)

    def update(self, dt: float) -> NoReturn:
        """Update state of the object."""
        if self.speed != 0:
            velocity = self.get_velocity(self.direction, self.speed)
            self.move(*velocity)


class TextObject:
    """ Text object. """

    def __init__(
            self,
            x: int,
            y: int,
            text_func: Callable,
            color: ColorValue,
            font_name: str,
            font_size: int,
    ):
        """ Text object initialization.

        Args:
            x: int:
                x position of the object.
            y: int:
                y position of the object.
            text_func: Callable:
                Text rendering function.
            color: ColorValue:
                Text color.
            font_name: str:
                Font family.
            font_size: int:
                Font size.
        """
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface: Surface, centralized: bool = False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2,
                   self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text: str):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass


class Apple(GameObject):
    """ Represents an apple. """

    def __init__(
            self, x, y,
            offset,
            color=(255, 255, 255),
            lifespan: int = 9999,
            *args, **kwargs,
    ):
        """Apple initialization.

        Args:
            x: int:
                Horizontal position of the object.
            y: int:
                Vertical position of the object.
            offset: Tuple[int, int]:
                Maximal x and y positions.
            color: ColorValue (default white):
                Object's color
            lifespan: int (default = 9999):
                Lifespan of the object

        """
        super().__init__(x, y, offset=offset, color=color, *args, **kwargs)
        self.lifespan = lifespan

    def draw(self, surface: Surface) -> NoReturn:
        """Draw shape of the object to a surface."""
        pygame.draw.circle(
            surface,
            self.color,
            self.center,
            self.width / 2
        )

    def respawn(self) -> NoReturn:
        """Randomly change object's coordinates."""
        self.bounds.x = randrange(0, self.offset[0] - self.width)
        self.bounds.y = randrange(0, self.offset[1] - self.height)


class SnakePart(GameObject):
    """ Abstract class for snake body parts. """

    def __init__(
            self, x, y,
            offset,
            color=(255, 255, 255),
            speed=stg.SNAKE_SPEED,
            direction=1,
            *args, **kwargs,
    ):
        """Snake part initialization.

        Args:
            x: int:
                Horizontal position of the object.
            y: int:
                Vertical position of the object.
            offset: Tuple[int, int]:
                Maximal x and y positions.
            color: ColorValue (default white):
                Object's color
            speed: int (default = SNAKE_SPEED):
                Represents the value of steps per second.
            direction: int (default = 1):
                Direction of the object.
        """
        super().__init__(
            x, y,
            offset=offset,
            color=color,
            speed=speed,
            direction=direction,
            *args, **kwargs
        )

    @abc.abstractmethod
    def draw(self, surface: Surface):
        """Draw shape of the object to a surface."""
        pass


class SnakeHead(SnakePart):
    """ Represents snake head controlled by player. """
    DIRECTIONS = {
        stg.KEYS['UP']: 0,
        stg.KEYS['RIGHT']: 1,
        stg.KEYS['DOWN']: 2,
        stg.KEYS['LEFT']: 3,
    }

    def draw(self, surface: Surface):
        """Draw shape of the object to a surface."""
        pygame.draw.rect(surface, self.color, self.bounds)

    def handle(self, key: Key):
        """Handle input key."""
        if key in (stg.KEYS['LEFT'], stg.KEYS['RIGHT']) \
                and self.direction % 2 != 1 \
                or key in (stg.KEYS['UP'], stg.KEYS['DOWN']) \
                and self.direction % 2 != 0:
            self.direction = self.DIRECTIONS[key]


class SnakeBody(SnakePart):
    """ Represents snake body part. """

    def draw(self, surface: Surface):
        """Draw shape of the object to a surface."""
        pygame.draw.circle(surface, self.color, self.center, self.width / 2)


class SnakeTail(SnakePart):
    """ Represents snake tail. """

    def draw(self, surface: Surface):
        """Draw shape of the object to a surface."""
        all_points = (
            self.bounds.midbottom,
            self.bounds.topleft,
            self.bounds.midleft,
            self.bounds.topright,
            self.bounds.midtop,
            self.bounds.bottomright,
            self.bounds.midright,
            self.bounds.bottomleft,
        )
        points = (
            all_points[self.direction * 2],
            all_points[(self.direction * 2 + 1) % 8],
            all_points[(self.direction * 2 + 3) % 8],
        )
        pygame.draw.polygon(surface, self.color, points)


class Snake:
    """ Collection of the all snake parts. """

    def __init__(
            self, x: int, y: int,
            color: ColorValue,
            offset: Tuple[int, int],
            speed: int,
            direction: int = 1,
            length: int = 0,
    ):
        """Snake constructor.

        Args:
            x: int:
                Horizontal position of the head.
            y: int:
                Vertical position of the head.
            color: ColorValue:
                Snake's color
            offset: Tuple[int, int]:
                Maximal x and y positions.
            speed: int (default = SNAKE_SPEED):
                Represents the value of steps per second.
            direction: int (default = 1):
                Direction of the snake.
            length: int (default = 0):
                Number of body parts besides head and tail.

        """
        self.parts = [
            SnakeHead(x, y, color=color, speed=speed,
                      direction=direction, offset=offset),
            SnakeTail(x, y, color=color, speed=speed,
                      direction=direction, offset=offset)
        ]

        # Add body parts
        for _ in range(length):
            self.parts.insert(1, SnakeBody(
                x, y, color=color, speed=speed,
                direction=direction, offset=offset))
        # Shift body
        for i in range(1, len(self.parts)):
            velocity = GameObject.get_velocity(direction, speed)
            self.parts[i].move(*map(lambda n: -n * i, velocity))

        self.color = color
        self.offset = offset
        self.speed = speed
        self.time = 0
        self.got_apple = False

    @property
    def head(self):
        return self.parts[0]

    def move(self, dt: float):
        """Move snake."""
        tmp_direction = self.head.direction
        tmp_x, tmp_y = self.head.bounds.x, self.head.bounds.y
        self.head.update(dt)
        for part in self.parts[1:]:
            part.bounds.x, tmp_x = tmp_x, part.bounds.x
            part.bounds.y, tmp_y = tmp_y, part.bounds.y
            tmp_direction, part.direction = part.direction, tmp_direction

    def grow(self, dt):
        """Insert additional body part after snake's head."""
        body = SnakeBody(
            self.head.bounds.x,
            self.head.bounds.y,
            color=self.color,
            speed=self.head.speed,
            offset=self.offset,
            direction=self.head.direction
        )
        self.parts.insert(1, body)
        self.head.update(dt)


    def update(self, dt: float) -> NoReturn:
        """Update state of the snake."""
        if self.time > 1 / self.head.speed:
            if self.got_apple:
                self.grow(dt)
                self.got_apple = False
            else:
                self.move(dt)
            self.time = 0
        else:
            self.time += dt

    def draw(self, surface: Surface) -> NoReturn:
        """Draw every part of the snake."""
        for part in self.parts:
            part.draw(surface)

    def handle(self, key: Key) -> NoReturn:
        """Handle input key."""
        self.head.handle(key)

    def check_collision(self) -> bool:
        # Check walls collision
        if self.head.left < 0 \
                or self.head.right > self.offset[0] \
                or self.head.top < 0 \
                or self.head.bottom > self.offset[1]:
            return True

        # Check self collision
        for part in self.parts[1:]:
            if self.head.bounds.colliderect(part.bounds):
                return True

        return False

    def colliderect(self, rect: Rect):
        """Check if snake collide with a given rect."""
        for part in self.parts:
            if part.bounds.colliderect(rect):
                return True
        return False
