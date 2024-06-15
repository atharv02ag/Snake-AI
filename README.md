# Snake AI game
The project is a snake AI which can learns to play the snake game with time
Two machine learning algorithms have been attempted namely :-
* NEAT (Neuro Evolution of Augmenting Topologies)
* Deep Q-Learning
  
Two seperate branches have been created (neat, DQN) showing the implementation of both algorithms, while the main branch is a vanilla showcase of the game that can be played by a user.
## Deep Q-Learning
### Packages used:-
* pytorch
* matplotlib
* pygame
* numpy

**Inputs** : State of snake as a list of 11 elements, which includes one-hot encoded information about direction of motion, food position relative to snake, and position of nearby boundaries.

**Outputs** : Q values corresponding to each action the snake can take. 3 possible actions are there - to move straight, take left turn or take right turn. The action which corresponds to the maximum Q value is chosen.

**Rewards** : +10 for every time it eats the food. -10 for every time it dies. No reward for just surviving.

## NEAT

### Packages used:-
* neat
* matplotlib
* graphviz
* pyautogui
* pygame
* numpy

**Inputs** : Distances of the snake's head to each boundary, and the length and angle of the snake-head-to-food vector

**Outputs** : Direction suggested by the network. 4 possible actions are there - to move up, right, down or left. Actions absolute to the game reference frame are used rather than relative to the snake.

**Fitness Criteria** : +100 fitness awarded every time an individual eats the food. -10 for when it dies. +0.5 if a move results in the snake getting closer to the food and -0.5 when it does not.
If an individual moves in the direction opposite to its previous direction, -1 fitness awarded.

At the end of each algorithm, a graph is displayed to show the performance of the snakes as games progress.
