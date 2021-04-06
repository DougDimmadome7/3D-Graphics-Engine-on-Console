import math
 
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
 
    #TODO: fix the use of list vector and not vector object
    def translate(self, vector: list) -> None:
        """
        Given a vector of type [x,y,z], this method applies the transformation
        to the point in 3-d space.
        """
        assert len(vector) == 3
        self.x += vector[0]
        self.y += vector[1]
        self.z += vector[2]
 
    def distance(self, point2) -> float:
        return math.sqrt((self.x - point2.x)**2 + (self.y - point2.y)**2 + (self.z - point2.z)**2)
 
    def list_form(self) -> list:
        return [self.x, self.y, self.z]
 
    def rotate_about(self, theta_h: float, theta_v: float, P0 = [0,0,0]) -> None:
        """
        Given a point, P0, this method rotates self around that point in either
        the vertical or horizontal plane. 
        """
        theta_h = math.radians(theta_h)
        # Horizontal rotation
 
        x = (self.x - P0[0]) * math.cos(theta_h) + (self.y - P0[1]) * math.sin(theta_h) + P0[0]
        y = -(self.x - P0[0]) * math.sin(theta_h) + (self.y - P0[1]) * math.cos(theta_h) + P0[1]
 
 
    
        self.x = x
        self.y = y
        # Vertical rotation
 
class Vector:
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k
 
    def display(self):
        print("[{}, {}, {}]".format(self.i, self.j, self.k))
 
    def magnitude(self):
        return math.sqrt((self.i**2) + (self.j**2) + (self.k**2))
 
    def cross_product(self, vector2):
        Cx = self.j*vector2.k - self.k*vector2.j
        Cy = self.k*vector2.i - self.i*vector2.k
        Cz = self.i*vector2.j - self.j*vector2.i
 
        return Vector(Cx, Cy, Cz)
 
    def list_form(self) -> list:
        """
        returns the components represented as a list.
        """
        return [self.i, self.j, self.k]
 
class Surface:
    def __init__(self, points: list, brightness = 100):
        """
        This method defines the surface as the linked list above. The points
        are connected from left to right. Ex: points[0] -> points[1]
        """
        assert len(points) >= 3
        self.points = points
        self.brightness = brightness
 
    def plane_eq(self) -> list:
        """
        This generates an equation which the xyz points must sum to. Returns
        a list of form [x coeff, y coeff, z coeff, = const].
        """
 
        # you need a point and a perpendicular line to create a plane. To do this,
        #we will define two vectors then take their cross product.
        P1, P2, P3 = self.points[0], self.points[1], self.points[2]
        vector1 = Vector((P1.x - P2.x), (P1.y - P2.y), (P1.z - P2.z))
        vector2 = Vector((P1.x - P3.x), (P1.y - P3.y), (P1.z - P3.z))
 
        # The vector normal to the plane. This allows us to find the plane's
        #equation
        n = vector1.cross_product(vector2)
        constant = (P1.x*n.i) + (P1.y*n.j) + (P1.z*n.k)
 
        # x(n.i) + y(n.j) + z(n.k) = constant
        return [n.i, n.j, n.k, constant]
 
    def max_mins(self) -> list:
        """
        Returns a list with the max and min on all three axes.
 
        [[max.x, min.x], [max.y, min.y], [max.z, min.x]]
        """
        max_mins = [[float("-inf"), float("inf")],[float("-inf"), float("inf")],[float("-inf"), float("inf")]]
 
        for i in self.points:
            if i.x < max_mins[0][1]:
                max_mins[0][1] = i.x
            elif i.x > max_mins[0][0]:
                max_mins[0][0] = i.x
 
            if i.y < max_mins[1][1]:
                max_mins[1][1] = i.y
            elif i.y > max_mins[1][0]:
                max_mins[1][0] = i.y
 
            if i.z < max_mins[2][1]:
                max_mins[2][1] = i.z
            elif i.z > max_mins[2][0]:
                max_mins[2][0] = i.z   
 
        return max_mins
 
    def find_center(self):
        avg_x, avg_y, avg_z = 0, 0, 0
        num = len(self.points)
        for point in self.points:
            avg_x += point.x
            avg_y += point.y
            avg_z += point.Z
 
        return Point(avg_x/num, avg_y/num, avg_z/num)
 
class Shape:
    def __init__(self, surfaces: list):
        """
        In order for a shape to be valid, it must be solid, and it must not 
        contain any interesecting sides.
        """
        self.surfaces = surfaces
    
    def info(self):
        """
        Prints out the x,y,z coordinates of every point that composes the shape.
        """
        point_list = []
        for i in self.surfaces:
            for point in i.points:
                if point not in point_list:
                    point_list.append(point)
 
        for i in range(len(point_list)):
            print("Point {}:".format(i))
            print("X: {} Y: {} Z: {}".format(point_list[i].x, point_list[i].y, point_list[i].z))
 
    def get_points(self) -> set:
        points = set([])
        for surface in self.surfaces:
            for point in surface.points:
                if point not in points:
                    points.add(point)
        return points
 
    def find_center(self):
        points = self.get_points()
        avg_x, avg_y, avg_z = 0, 0, 0
        num = len(points)
        for point in self.get_points():
            avg_x += point.x
            avg_y += point.y
            avg_z += point.z
 
        return Point(avg_x/num, avg_y/num, avg_z/num)
 
    def rotate(self, theta_h, theta_v) -> None:
        """
        Rotates about its center point
        """
        center = self.find_center()
        for point in self.get_points():
            point.rotate_about(theta_h, theta_v, center.list_form())
 
class Compound_Shape:
    def __init__(self, shapes: list):
        self.shapes = shapes
    

#TODO: Fix the pyramid code
def eq_pyr(length: float, point):
    """
    This function creates an equilateral pyramid, where the center of its
    base resides at the specific point, and the side lengths are passed.
    """
    #create the base points
    across = (math.sqrt(length**2 + (length**2)/4))
    
    P1 = Point((point.x - length/2), (point.y - across), point.z)
    P2 = Point((point.x + length/2), (point.y - across), point.z)
    P3 = Point((point.x),            (point.y + across), point.z)
 
    # higher point
    height = math.sqrt(across**2 - (across**2)/4)
    P4 = Point(point.x, point.y, (point.z + height))
 
    base = Surface([P1, P2, P3])
    slant_sides = []
    point_slide = [P1, P2, P3, P1]
    for i in range(len(point_slide) - 1):
        slant_sides.append(Surface([point_slide[i], P4, point_slide[i+1]]))
    
    slant_sides.append(base)
    return Shape(slant_sides)
 
#TODO: This will draw hourglass base and top side. Be careful
def rectangle_prism(base_center, length: float, width: float, height: float):
    """
    Given a center for the base of a rectangular, as well as the length,
    width, and height of the prism, this function returns the rectangular
    prism object.
    """
 
    base_points = []
    top_points = []
    for i in [.5*length, -.5*length]:
        for j in [.5*width, -.5*width]:
            base_points.append(Point((base_center.x + i), (base_center.y - j), (base_center.z)))
            top_points.append(Point((base_center.x + i), (base_center.y - j), (base_center.z + height)))
 
    base = Surface(base_points)
    top = Surface(top_points)
    l_side1 = Surface([base_points[0], base_points[2], top_points[0], top_points[2]], 100)
    l_side2 = Surface([base_points[1], base_points[3], top_points[1], top_points[3]], 100)
    s_side1 = Surface([base_points[0], base_points[1], top_points[0], top_points[1]], 25)
    s_side2 = Surface([base_points[2], base_points[3], top_points[2], top_points[3]], 25)
 
    return Shape([base, top, l_side1, l_side2, s_side1, s_side2])
 
def flat_rectangle(center, l, w):
    P1 = Point(center.x, center.y - (w*.5), center.z)
    P2 = Point(center.x, center.y + (w*.5), center.z)
    P3 = Point(center.x, center.y - (w*.5), center.z + l)
    P4 = Point(center.x, center.y + (w*.5), center.z + l)
 
    return Shape([Surface([P1,P2,P4,P3])])
 
def steve(center):
    """
    #Creates a MineCraft Steve.
    """
    head =  rectangle_prism(Point(center.x, center.y, center.z+10), 8, 8, 8)
    body =  rectangle_prism(Point(center.x, center.y, center.z-12), 8, 4, 12) #SUS

    arm_r = rectangle_prism(Point(center.x -8, center.y, center.z-12),4,4,12) #x poses are sus
    arm_l = rectangle_prism(Point(center.x +8, center.y, center.z-12),4,4,12)
    leg_r = rectangle_prism(Point(center.x-4, center.y, center.z-24),4,4,12)
    leg_l = rectangle_prism(Point(center.x+4, center.y, center.z-24),4,4,12)

    return [head, body, arm_l, arm_r, leg_l, leg_r]
