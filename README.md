Python Version : 3.10.4

Package            Version
------------------ -----------
asttokens          2.0.5
backcall           0.2.0
certifi            2022.5.18.1
charset-normalizer 2.0.12
cycler             0.11.0
decorator          5.1.1
executing          0.8.3
fonttools          4.33.3
idna               3.3
ipython            8.4.0
jedi               0.18.1
kiwisolver         1.4.2
matplotlib         3.5.2
matplotlib-inline  0.1.3
numpy              1.22.4
opencv-python      4.5.5.64
packaging          21.3
parso              0.8.3
pexpect            4.8.0
pickleshare        0.7.5
Pillow             9.1.1
pip                22.1.2
prompt-toolkit     3.0.29
ptyprocess         0.7.0
pure-eval          0.2.2
pygame             2.1.2
Pygments           2.12.0
pyparsing          3.0.9
python-dateutil    2.8.2
requests           2.27.1
setuptools         59.6.0
six                1.16.0
stack-data         0.2.0
torch              1.11.0+cpu
torchvision        0.12.0+cpu
traitlets          5.2.2.post1
typing_extensions  4.2.0
urllib3            1.26.9
wcwidth            0.2.5


## Project Description:
In this project I created snake game from scratch in which I tried to implement AI Learning. This repository contains two files which can be executed are <b><i>play.py</i></b> which runs the normal snake game where the user can play it and <b><i>run.py</b></i> which are present in folders <b>'Normal Game'</b> and <b>'AI Game'</b> respectively.
For training the AI referenced the youtube playlist named ![Teach AI To Play Snake! Reinforcement Learning With PyTorch and Pygame](https://www.youtube.com/playlist?list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV). The difference from the project done in that video and this one is that the game is created by me which makes the process execution unique.
The AI network is made up of an input layer of 11 values, hidden layer of 256 values and an output layer of 3 values. The input layer which is the state of the snake's head. The first three values of this depicts the danger of an action, the next four values represent which direction the snake is travelling in and last four values depict where the food is in reference to snake's head. The networks output consist of 3 values which represent whether the snake should continue moving forward, take a right turn or take a left turn respectively. To counter the exploration-exploitation deliema we are using epsilon-greedy policy with epsilon decreasing after each game played. We are also restricting the gameplay of the agent till it crashes or it exceed a certain number of steps which is calculated dynamically.
We notice that at first the agent is very bad at moving as it is taking many rnadom steps due to high epsilon value but AI becomes smart and as the number of random actions are dropping with each game so its average score starts increasing. I ran the program till it reached ~1000 Games and in those games it reached the highest score of 22.
![training graph](model_training_plot.png)
The above graph represents how the mean score and current score are changing throughout the gameplay.



Highest Score : 22


