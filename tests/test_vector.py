import sys
import os

# Add Vectorpy to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from Vectorpy
from Vectorpy.main import Vector  # Importing the class/function from main.py
import pytest


def test_vector_addition():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    result = v1 + v2
    assert result.x == 5 and result.y == 7 and result.z == 9

def test_vector_subtraction():
    v1 = Vector(7, 8, 9)
    v2 = Vector(3, 2, 1)
    result = v1 - v2
    assert result.x == 4 and result.y == 6 and result.z == 8

def test_vector_scalar_multiplication():
    v = Vector(2, -3, 5)
    result = v * 3
    assert result.x == 6 and result.y == -9 and result.z == 15

def test_vector_magnitude():
    v = Vector(3, 4, 0)
    assert v.magnitude() == 5  # √(3² + 4²) = 5

def test_vector_unit_vector():
    v = Vector(3, 4, 0)
    unit = v.unit_vector()
    assert round(unit.x, 2) == 0.6 and round(unit.y, 2) == 0.8

def test_dot_product():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, -5, 6)
    assert v1.dot(v2) == (1*4 + 2*(-5) + 3*6)  # 4 - 10 + 18 = 12

def test_cross_product():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    result = v1.cross(v2)
    assert result.x == -3 and result.y == 6 and result.z == -3  # (i, j, k determinant)

def test_angle_between_vectors():
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    assert v1.angle_with(v2) == 90  # Perpendicular vectors should have 90°

def test_projection():
    v1 = Vector(3, 4, 0)
    v2 = Vector(1, 0, 0)  # Unit vector along x-axis
    proj = v1.projection_on(v2)
    assert round(proj.x, 2) == 3 and proj.y == 0 and proj.z == 0

def test_work_done():
    force = Vector(5, 0, 0)
    displacement = Vector(10, 0, 0)
    assert force.work_done(displacement) == 50  # F ⋅ d = 5 × 10

def test_torque():
    r = Vector(3, 0, 0)
    F = Vector(0, 5, 0)
    result = r.torque(F)
    assert result.x == 0 and result.y == 0 and result.z == 15  # Torque in z-direction
