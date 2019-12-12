from manimlib.imports import *
import numpy as np

def Dmat():
    return VGroup(
        Square(),
        Line(np.array([1,-1,0]), np.array([-1,1,0]))
    )

def ELmat():
    return VGroup(
        Square(),
        Line(np.array([-1,1,0]), np.array([-0.3,0.3,0])),
        Line(np.array([-0.3,0,0]), np.array([0,-0.3,0]))
    )

def Pmat():
    return VGroup(
        Square(),
        Dot(np.array([0.33, 0.66, 0])),
        Dot(np.array([0.66, 0.33, 0])),
        Dot(np.array([-0.33, -0.66, 0])),
        Dot(np.array([-0.66, -0.33, 0]))
    )

def Lmat(color=BLUE):
    Lverts = (np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        Square(color=color),
        Polygon(*Lverts, color=color).set_fill(color, opacity=0.5)
    )

def Umat(color=RED):
    Uverts = (np.array([1, 1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        Square(color=color),
        Polygon(*Uverts, color=color).set_fill(color, opacity=0.5)
    )
