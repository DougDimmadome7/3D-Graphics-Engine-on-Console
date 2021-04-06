# 3D-Graphics-Engine-on-Console
BETA VERSION! This is a work in progress graphics engine for the command prompt written in python. It is slow and can sometimes produce strange artifacts, but I figured someone may like to use it for inspiration.

# Use
  Your console MUST be 317 characters wide and 81 characters tall by default. If you are running at different dimensions, which is highly likely, you should 
change them or change the camera object's arguments to fit your dimensions. The higher width and height are there to create a higher resolution image. To run an example
scene, run scene.py, which has a rotating column.

# Design
  The program uses a simple ray tracing algorithm, where each character space on the command console is given a ray, and that ray is projected outwards. If the ray hits
a surface, the brightness of that surface is printed onto the console.
