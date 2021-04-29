# Lego Mindstorms EV3: Machine Learning
## Number Prediction
This project uses a Lego model, created with the 
[Mindstorms EV3 robotics kit (31313)](https://www.lego.com/en-gb/product/lego-mindstorms-ev3-31313), to predict which 
wooden number (0 to 9) has been placed on a platform beneath a light sensor supplied with the kit.
This is achieved by creating a machine learning model from the light reflectivity readings of each number as they
rotate beneath the sensor.


The Lego model comprises a rotating platform on which wooden numeric characters are placed. Mounted above the platform is an
EV3 Light Sensor which measures the reflectivity of the number, and it's background, as it rotates through a specified 
number of rotations. The platform is covered with aluminium foil to provide an improved reflective background for the
number and greater range of reflectivity values returned by the sensor. The raw results of each rotation are captured
in a CSV file of 'Angle of Rotation' vs 'Reflectivity' values

Build instructions, technical details and a video demonstration of the project can be found at the 
[Datapiquing](https://www.datapiquing.com) website

![Lego Mindstorms EV3 Model](./images/EV3ReflectivityPlatform.png)

## Implementation

> main.py

This is a python script that needs to be downloaded to an EV3 brick running 
[pybricks micropython](https://education.lego.com/en-gb/downloads/mindstorms-ev3/software). It has 2 functions:
- rotate the platform, measure reflectivity & angle of rotation at specified time intervals and log the results to a CSV file
- display and speak the predicted number returned by the machine learning model

A number of experimental variables can be passed as arguments to the script including:
- number of rotations
- speed of rotation
- sensor measurement interval
- motor port
- colour sensor port 
- touch sensor port
- target value (number)
- log filename
- predicted value 
  
Default values have been set for all if none are specified.

### Connecting to the EV3 brick via SSH
The '**collect**' and '**predict**' [Jupyter Notebooks](https://jupyter.org) below communicate with the EV3 brick via SSH.
There are several online resources explaining how to do this:
- [Connecting to Ev3dev using SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/)
- [Reusing SSH Connections](https://www.ev3dev.org/docs/tutorials/reusing-ssh-connections/)
- [Setup RSA key for SSH](https://muddlinthrough.com/tag/mindstorms/)
- [Mindstorms EV3 Revisited](https://muddlinthrough.com/tag/mindstorms/)

> 01_collect.ipynb

A notebook that when executed on a PC, connected to an EV3 brick, does the following:
- prompts the user to place each number (0 to 9) on the platform for analysis
- executes '**main.py**' on the EV3 brick to log reflectivity vs angle of rotation to a CSV file
- returns a CSV file for each number to the '**raw_data**' folder

> 01_clean.ipynb

Restructures each CSV file into a format suitable for machine learning, concatenates them into a single file 
and saves it to the '**clean_data**' folder as '**training_dataset.csv**'

> 03_analyse.ipynb

Generate plots of '**reflectivity vs angle of rotation**' for all numbers

> 04_train.ipynb

Use the '**training_dataset**' to train a machine learning model (**K-Nearest Neighbour**) and save it to the '**ml_model**' 
folder. Determine the accuracy of the model

> 05_predict.ipynb

A notebook that when executed on a PC, connected to an EV3 brick, does the following:
- prompts the user to place a number on the lego platform for the machine learning to predict
- executes '**main.py**' on the EV3 brick to log reflectivity vs angle of rotation to a CSV file
- transfer the CSV file from the EV3 brick to the PC
- process the raw data - clean and categorise into rotation buckets
- predict the number using the machine learning model created from the training dataset
- display an image of the predicted number on the PC
- display and speak the predicted value on the EV3 brick
- plot graphs of rotation vs reflectivity (including mean and median plots) in the notebook
