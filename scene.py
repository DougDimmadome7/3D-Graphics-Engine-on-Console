from shapes import rectangle_prism, Point, flat_rectangle, eq_pyr, steve
from graphics import Camera
import time, os, shapes
 
class Scene:
    def __init__(self, camera, shapes):
        self.shapes = shapes
        self.camera = camera
 
    def run(self):
        self.camera.scan(self.shapes)
 
    def rotate_anim(self, shape, angle, turns = 1):
        for i in range(360*turns//angle):
            time.sleep(0)
            shape.rotate(angle, 0)
            #os.system("cls")
            self.run()
 
prism = shapes.rectangle_prism(Point(50,0,-10), 10, 10, 30)

scene1 = Scene(Camera(Point(0,0,0),70,70, [0,0], 317, 80), [prism])
scene1.rotate_anim(scene1.shapes[0], 10)
scene1.run()
