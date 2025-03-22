import math

class Vector:
    """A class to represent 2D/3D vectors and perform operations on them."""

    def __init__(self, x: float, y: float, z: float=0.0):
        """Initialize a new Vector object."""
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        """String representation of the vector."""
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __add__(self, other):
        """Add two vectors together."""
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        """Subtract one vector from another."""
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float):
        """Multiply the vector by a scalar."""
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def magnitude(self):
        """Calculate the magnitude of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def unit_vector(self):
        """Return the unit vector."""
        mag = self.magnitude()
        return Vector(self.x / mag, self.y / mag, self.z / mag) if mag != 0 else None
    
    def dot(self, other):
        """Calculate the dot product of two vectors."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """Calculate the cross product of two vectors."""
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def angle_with(self, other):
        """Calculate the angle between two vectors."""
        dot_product = self.dot(other)
        magnitude_product = self.magnitude() * other.magnitude()
        angle = math.acos(dot_product / magnitude_product)
        return math.degrees(angle) if magnitude_product != 0 else None
    
    def projection_on(self, other):
        """Calculate the projection of this vector onto another vector."""
        other_unit = other.unit_vector()
        return other_unit * (self.dot(other_unit)) if other_unit else None
    
    def work_done(self, force):
        """Calculate the work done by a force on an object."""
        return force.dot(self)
    
    def torque(self, force):
        """Calculate the torque produced by a force."""
        return self.cross(force)
    
if __name__ == "__main__":
    v1 = Vector(3, 4, 5)
    v2 = Vector(1, 2, 3)
    
    print("Vector 1:", v1)
    print("Vector 2:", v2)
    print("Addition:", v1 + v2)
    print("Dot Product:", v1.dot(v2))
    print("Cross Product:", v1.cross(v2))
    print("Magnitude of v1:", v1.magnitude())
    print("Unit Vector of v1:", v1.unit_vector())
    print("Angle between v1 and v2:", v1.angle_with(v2))
    print("Projection of v1 on v2:", v1.projection_on(v2))
    print("Work done by v1 with v2 as force:", v1.work_done(v2))
    print("Torque with v1 as r and v2 as force:", v1.torque(v2))

