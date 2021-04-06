import math
from shapes import Point, Vector, Surface
from lighting import gradient
 
class Ray:
    def __find_components(self, theta_v: float, theta_h: float) -> list:
        """
        Given the horizontal and vertical angle, calculate the vector 
        components such that the magnitude of the vector is 1.
        """
        theta_h = math.radians(theta_h)
        theta_v = math.radians(theta_v)
 
 
        if theta_v > 0:
            z = math.sin(theta_v)
            a = math.cos(theta_v)
        else:
            z = math.cos(math.radians(90) - theta_v)
            a = math.sin(math.radians(90) - theta_v)
 
        if theta_h > 0:
            x = a * math.sin(math.radians(90) - theta_h)
            y = a * math.cos(math.radians(90) - theta_h)
        else:
            y = a * math.sin(theta_h)
            x = a * math.cos(theta_h)
 
        return [x, y, z]
 
    def __init__(self, theta_v: float, theta_h: float, position):
        """
        The ray is a line in 3-d space that is defined as a vector of length 1
        """
        parts = self.__find_components(theta_v, theta_h)
        self.vector = Vector(parts[0], parts[1], parts[2])
        self.position = position  
 
    #TODO: This may not actually be working
    def collision_cor(self, surface, is_eq = False) -> list:
        """
        Returns the x,y,z coordinates where the Ray collides with the 
        """
        # This method works by treating the vector of the Ray as a parametric
        #line equation. This makes determining whether there is a collision
        #much simpler.
        if not is_eq:
            equation = surface.plane_eq()
        else:
            equation = surface
 
        # Distribute the plane coefficients, and separate the constants from
        #the coefficients of T.
 
        consts, coeff = [0,0,0], [0,0,0]
 
        for i in range(3):
            consts[i] = self.position.list_form()[i] * equation[i]
            coeff[i] = self.vector.list_form()[i] * equation[i]
 
        equation[3] -= sum(consts)
        t = equation[3] / sum(coeff) if sum(coeff) != 0 else float("inf")
 
        return [i * t for i in self.vector.list_form()] + [t]
 
    def __will_impact(self, surface, precision = .4) -> bool:
        """
        returns a boolean with whether the ray will impact the surface
        """
        impact = self.collision_cor(surface) #calculate where ray impacts surface
        max_mins = surface.max_mins() #returns the region where the shape is
 
        for i in range(len(max_mins)): 
            # checks if the point of impact is not within allowable range
            if impact[i] > max_mins[i][0] + precision or impact[i] < max_mins[i][1] - precision:
                return False
 
        return True
 
    def closest(self, shapes) -> float:
        """
        Given a set of possible shapes to impact, this finds which surface
        the parametric form of the vector will impact, and returns its 
        brightness to be outputted.
        """
        closest_t = float("inf")
        brightness = 0
 
        for shape in shapes:
            for surface in shape.surfaces:
                if self.__will_impact(surface):
                    if self.collision_cor(surface)[-1] < closest_t:
                        brightness = surface.brightness
                        closest_t = self.collision_cor(surface)[-1]
        return brightness
 
 
class Camera:
    def __init_rays(self, position, h_angle, v_angle, orientation: list, X_len = 237, Y_len = 62):
        """
        generates a list of Rays which will correspond to each pixel on the command
        line.
        """
        rays = []
 
        for i in range(Y_len): #for every pixel row
            for j in range(X_len): #Go across
                r = Ray((v_angle - v_angle*i*2/Y_len) + orientation[0], (-h_angle + h_angle*j*2/X_len) + orientation[1], position)
                rays.append(r)
 
        return rays
 
    def __init__(self, position, h_angle, v_angle, orientation = [0,0], X_len = 237, Y_len = 62, b_coeff = 1):
        assert h_angle < 180
        assert v_angle < 180
        
        self.orientation = orientation
        self.position = position
        self.h_angle = h_angle
        self.v_angle = v_angle
        self.X_len = X_len
        self.Y_len = Y_len
 
        self.rays = self.__init_rays(position, h_angle, v_angle, orientation, X_len, Y_len)
 
    def __create_view(self) -> list:
        """
        returns a grid with the same y values as the console view.
        """
        view = []
        for i in range(self.Y_len):
            view.append([])
        return view
 
    def __display_view(self, view):
        for row in view:
            for item in row:
                print(item, end = '')
 
    def __bright_ascii(self, brightness) -> chr:
        """
        Given a brightness value, this will scale that brightness to an 
        ascii character to output
        """
        return gradient[int(brightness // (100/len(gradient)))]
 
    #TODO: FIX THE SCAN METHOD
    def scan(self, shapes):
        """
        The camera generates a set of rays that correspond with each pixel 
        on the console. The rays are separated out evenly.
        """
        #view = self.__create_view()
        view = ""
        for i in range(len(self.rays)):
            view += self.__bright_ascii(self.rays[i].closest(shapes))
            
        #self.__display_view(view)
        print(view)
 
 
 
 
 
 
