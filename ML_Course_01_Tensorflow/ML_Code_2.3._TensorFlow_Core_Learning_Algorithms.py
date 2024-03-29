# Machine Learning with TensorFlow - Code 2.3. - TensorFlow Core Learning Algorithms


# Hidden Markov Models

# Data
# To create a hidden markov model we need.
# - States
# - Observation Distribution
# - Transition Distribution

# Imports and Setup
# pip install tensorflow_probability==0.8.0rc0 --user --upgrade

import tensorflow_probability as tfp  # we are using a different module from tensorflow this time
import tensorflow as tf

# Weather Model
# We will model a simple weather system and try to predict the temperature on each day given the following information.
# 1. Cold days are encoded by a 0 and hot days are encoded by a 1.
# 2. The first day in our sequence has an 80% chance of being cold.
# 3. A cold day has a 30% chance of being followed by a hot day.
# 4. A hot day has a 20% chance of being followed by a cold day.
# 5. On each day the temperature is normally distributed with mean and standard deviation 0 and 5 on
# a cold day and mean and standard deviation 15 and 10 on a hot day.

# To model this in TensorFlow we will do the following.
tfd = tfp.distributions  # making a shortcut for later on
initial_distribution = tfd.Categorical(probs=[0.2, 0.8])  # refer to point 2 above
transition_distribution = tfd.Categorical(probs=[[0.5, 0.5],
                                                 [0.2, 0.8]])  # refer to points 3 and 4 above
observation_distribution = tfd.Normal(loc=[0., 15.], scale=[5., 10.])  # refer to point 5 above

# the loc argument represents the mean and the scale is the standard devitation

# We've now created distribution variables to model our system and it's time to create the hidden markov model.
model = tfd.HiddenMarkovModel(
    initial_distribution=initial_distribution,
    transition_distribution=transition_distribution,
    observation_distribution=observation_distribution,
    num_steps=7)

# To get the expected temperatures on each day we can do the following.
mean = model.mean()

# due to the way TensorFlow works on a lower level we need to evaluate part of the graph
# from within a session to see the value of this tensor

# in the new version of tensorflow we need to use tf.compat.v1.Session() rather than just tf.Session()
with tf.compat.v1.Session() as sess:  
  print(mean.numpy())
