# Snake-AI2
Python implementation of Snake controlled by a Convolutional NN using Tensorflow/Keras

The sample has a trained model for 7x7 game with 4 randomly place obstacle and 3 randomly place rewards of 25, 16 and 9.

### The model

##### Input:
3d matrix of dimension ( 2 x width + 1) x (2 x height + 1) x 3
All the data is relative to head of the snake, that's why the matrix needs to be much larger than the area of the screen.
I did some test with absolute coordinates but the result where not good even if it can still learn where it is and not die.
The first matrix contains the snake information. The values are 0 if empty then 1 for the tail then 2 for next one and so on and the head as a value of the length of the snake.
The second matrix contains the walls. 0 if empty, 1 if it is a wall. The edges of the screen are considered walls.
The third matrix contains the rewards. 0 if empty and value of the reward if not.

##### Hidden layers:
First Layer is 32 3x3 filters CNN with RELU activation.
Second Layer is 64 3x3 filters CNN with RELU activation.
Third Layer is 64 3x3 filters CNN with RELU activation.
Last Layer is 64 nodes FFNN with RELU activation.

##### Output:
4 for each directions

### Result:
Trained in 7x7 space since the neural network has a lot more nodes than in the previous project I kept it small so it does not take days to train. It gets pretty good result in less than a hour and close to optimal after a few hours.
It averages a score of 660, the maximum possible should be about 900. 

In the same environment as the first project so only one reward and no obstacles, it averages a score of 960, the maximum being 1100. So much better results than the first project and there are only few scenario it cannot handle properly.

