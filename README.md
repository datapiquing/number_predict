# Lego Mindstorms EV3: Machine Learning
## Number Prediction
This project uses a Lego model, created with the Mindstorms EV3 robotics kit (31313), to predict which wooden number 
(0 to 9) has been placed on a platform beneath a light sensor supplied with the kit.
This is achieved by creating a machine learning model from the light reflectivity readings of each number as they
rotate beneath the sensor.

Build instructions for the Lego model can be found at the [Datapiquing](https://www.datapiquing.com) website

![Lego Mindstorms EV3 Model](/images/EV3ReflectivityPlatform.png)

The model comprises a rotating platform on which wooden numeric characters are placed. Mounted above the platform is an
EV3 Light Sensor which measures the reflectivity of the number, and it's background, as it rotates through a specified 
number of rotations. The platform is covered with aluminium foil to provide an improved reflective background for the
number and greater range of reflectivity values returned by the sensor. The raw results of each rotation are captured
in a CSV file of 'Angle of Rotation' vs 'Reflectivity' values