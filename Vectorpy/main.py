import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Vector:
    """A class to represent 2D/3D vectors and perform operations on them."""

    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float):
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
        raise TypeError("Scalar multiplication only supports int or float")

    __rmul__ = __mul__

    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def unit_vector(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Zero vector has no unit vector.")
        return self / mag

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def angle_with(self, other):
        dot_product = self.dot(other)
        magnitude_product = self.magnitude() * other.magnitude()
        if magnitude_product == 0:
            raise ValueError("Cannot compute angle with a zero vector.")
        return math.degrees(math.acos(dot_product / magnitude_product))

    def projection_on(self, other):
        try:
            other_unit = other.unit_vector()
            return other_unit * self.dot(other_unit)
        except ValueError:
            raise ValueError("Cannot project onto a zero vector.")

    def work_done(self, force):
        return force.dot(self)

    def torque(self, force):
        return self.cross(force)


def plot_vectors(vectors, colors=None, labels=None):
    """Visualize 3D vectors with an enhanced, high-resolution UI."""
    
    # High-resolution settings
    fig = plt.figure(figsize=(10, 8), dpi=250)  # High DPI for clarity
    ax = fig.add_subplot(111, projection='3d', facecolor='black')  # Dark mode
    
    origin = [0, 0, 0]

    # Premium Color Palette
    if colors is None:
        colors = ['#FF5733', '#33FF57', '#337BFF', '#FF33A1', '#F4D03F', '#A569BD']

    # Plot vectors with improved styling
    for i, v in enumerate(vectors):
        ax.quiver(origin[0], origin[1], origin[2], v.x, v.y, v.z,
                  color=colors[i % len(colors)], arrow_length_ratio=0.1,
                  linewidth=4, alpha=0.9, linestyle="-")
        ax.text(v.x, v.y, v.z, f'  {labels[i]}' if labels else f'  V{i+1}',
                color=colors[i % len(colors)], fontsize=14, fontweight='bold')

    # Axis limits & dynamic scaling
    max_range = max(max(abs(v.x), abs(v.y), abs(v.z)) for v in vectors) + 2
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    # UI/UX Styling
    ax.set_xlabel('X-axis', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Y-axis', fontsize=14, fontweight='bold', color='white')
    ax.set_zlabel('Z-axis', fontsize=14, fontweight='bold', color='white')
    ax.set_title("3D Vector Visualization", fontsize=16, fontweight='bold', color='white')

    # Grid Enhancements
    ax.grid(True, linestyle="dotted", alpha=0.3, color="white")
    ax.view_init(elev=25, azim=35)  # Better viewing angle

    # **Custom Text Elements**
    plt.figtext(0.75, 0.92, "VectorPy", fontsize=18, fontweight="bold", color="#FFD700", ha="right")  # Gold color
    plt.figtext(0.12, 0.92, "VECTORS", fontsize=18, fontweight="bold", color="white", ha="left")  

    # Save & Show
    plt.savefig("vector_plot.png", bbox_inches='tight', transparent=True)
    print("Plot saved as vector_plot.png. Open it to view the high-quality visualization.")
    plt.show()

if __name__ == "__main__":
    v1 = Vector(40, 40, 40)
    v2 = Vector(60, 0, 0)
    v3 = Vector(0, -10, 0)

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

    # Visualize with enhanced styling
    plot_vectors([v1, v2, v3], labels=["V1", "V2", "V3"])

    # Example usage
    # v1 = Vector(3, 4) # 2D vector     
    # v2 = Vector(1, 2, 3) # 3D vector
    # v3 = Vector(2, -1, 4) # 3D vector
    # plot_vectors([v1, v2, v3], labels=["V1", "V2", "V3"])