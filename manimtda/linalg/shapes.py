from manimlib.imports import *
import numpy as np

def Dmat(color=WHITE):
    return VGroup(
        Square(color=color),
        Line(np.array([1,-1,0]), np.array([-1,1,0]),color=color)
    )

def ELmat(color=WHITE):
    return VGroup(
        Square(color=color),
        Line(np.array([-1,1,0]), np.array([-0.3,0.3,0]),color=color),
        Line(np.array([-0.3,0,0]), np.array([0,-0.3,0]),color=color)
    )

def Pmat(color=WHITE):
    return VGroup(
        Square(color=color),
        Dot(np.array([0.33, 0.66, 0]),color=color),
        Dot(np.array([0.66, 0.33, 0]),color=color),
        Dot(np.array([-0.33, -0.66, 0]),color=color),
        Dot(np.array([-0.66, -0.33, 0]),color=color)
    )

def Lmat(color=BLUE,corner_radius=0.5):
    Lverts = (np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        Square(color=color),
        Polygon(*Lverts, color=color).set_fill(color, opacity=0.5).round_corners(corner_radius)
    )

def Umat(color=RED,corner_radius=0.5):
    Uverts = (np.array([1, 1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        Square(color=color),
        Polygon(*Uverts, color=color).set_fill(color, opacity=0.5).round_corners(corner_radius)
    )
