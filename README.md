Modification of the standard snake game.

![game_over](https://github.com/Posurok/Badgers_and_Cats/assets/157339671/c982f0eb-02a8-4e6d-b5c6-af8b17bd8c6d)


Differences compared to the original assignment:
- Graphics have been revamped, resolution increased to 1280 x 1100 pixels.
- A scoring system has been added with a bonus of x1 x2 x3 for
  every 5 cats eaten.
- Added 4 types of different "apples"
  (the number of objects depends on the game's speed):
  
        Green Cat - 30 points and increases speed by "1".
        Red Cat - 20 points and increases speed by "1".  
        Orange Cat - 10 points and increases speed by "1".
        Black-and-White Cat - Slows down speed by "1", increases score bonus by 1.
  
- Added friendly Badger object - 4 pcs., eating a friendly object reduces
  the "snake" by 3 sections.
- Game Over occurs if the snake eats a friendly object and becomes = 0,
  or if the snake eats itself.
- "Badger" and "Black-and-White Cat" objects move randomly by one cell
  (their speed of movement depends on the game's speed).

In the case of eating red, orange, green cats - all cats' positions are
randomized. The cats are generated in new colors.
If you want to change this mechanic, you need to delete the block
(see comments in the code).

In the case of eating a black-and-white cat - there is no change in the
location of other objects, but depending on the game's speed - a new
black-and-white cat is added.

In the case of eating a friendly object - the position of all friendly
objects and cats is randomized.
If you want to change this mechanic, you need to delete the block
(see comments in the code).
