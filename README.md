# SNAKE GAME
#### Video Demo: https://youtu.be/MGLMSIvrNGM
#### Description: Classic snake game where you need eat apples and grow your snake.
Firstly, I set a deadline for myself to complete the job in 3 days. Initially, I wanted to use the C language to develop the game, but due to the short time, I chose the Python language, specifically the PyGame library.

Next, I created 3 files:

•	The settings file, where I put all constants with some game parameters, such as window size, snake speed and colors;

•	The second file with game objects, contains classes that represent entities in the game, such as snake or apple. It should be noted that here I wrote extra code for the future improvement of the game. So, I got here text object for menu and score counter. As well as additional parameters in snake class for setting graphic sprites.

•	The third and the main file is for basic classes with game cycle and the start of the game. Class Game contains some boring staff from PyGame documentation and class SnakeGame contains parameters specific for my snake game.

#### TODO
- Add score counter
- Add sound
- Add graphics
- Add main menu
- Add "game over"
- Add settings menu
- Add bonuses
- Fix the bug with 180° rotating sometimes
