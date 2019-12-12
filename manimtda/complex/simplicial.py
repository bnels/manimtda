"""
Simplicial Complexes for manim
"""
from manimlib.imports import *

def get_points(triangles):
    trinp = np.array(triangles).reshape(-1,3)
    pts = np.unique(trinp, axis=0)
    return pts

def get_edges(triangles):
    es = []
    for t in triangles:
        es.append([t[0], t[1]])
        es.append([t[0], t[2]])
        es.append([t[1], t[2]])
    es = np.array(es)
    return np.unique(es, axis=0)




def create_PointCloud(points, color=BLUE):
    return VGroup(
        *[Dot(p, color=color) for p in points]
    )

def create_0skel(triangles, color=BLUE):
    pts = get_points(triangles)
    return create_PointCloud(pts, color=color)

def create_1skel(triangles, color=BLUE):
    pts = get_points(triangles)
    es = get_edges(triangles)
    return VGroup(
        *[Dot(p, color=color) for p in pts],
        *[Line(e[0], e[1], color=color) for e in es]
    )

def create_2skel(triangles, color=BLUE):
    pts = get_points(triangles)
    return VGroup(
        *[Dot(p, color=color) for p in pts],
        *[Polygon(*t, color=color).set_fill(color, opacity=0.5) for t in triangles]
    )

def get_triangles():
    x1 = np.sqrt(3)/3
    x2 = 2*x1
    x3 = 3*x1
    # hexagon
    p = np.array([
    [-x1, 2, 0],
    [x1, 2, 0],
    [-x2, 1, 0],
    [0, 1, 0],
    [x2, 1, 0],
    [-x3, 0, 0],
    [-x1, 0, 0],
    [x1, 0, 0],
    [x3, 0, 0],
    [-x2, -1, 0],
    [0, -1, 0],
    [x2, -1, 0],
    [-x1, -2, 0],
    [x1, -2, 0]
    ])
    return [
    [p[0], p[2], p[3]],
    [p[0], p[1], p[3]],
    [p[1], p[3], p[4]],
    [p[2], p[5], p[6]],
    [p[2], p[3], p[6]],
    [p[6], p[3], p[7]],
    [p[3], p[4], p[7]],
    [p[4], p[7], p[8]],
    [p[5], p[6], p[9]],
    [p[6], p[9], p[10]],
    [p[i] for i in (6,7,10)],
    [p[i] for i in (7,10,11)],
    [p[i] for i in (7,8,11)],
    [p[i] for i in (9,10,12)],
    [p[i] for i in (10,12,13)],
    [p[i] for i in (10,11,13)],
    ]

def to_manifold(p,
    shift=np.array([1,0,0]),
    scale=np.array([[0.9,0.1,0], [0.1,0.9,0], [0,0,0]]),
    curve=np.array([[0, 0, 0], [0,0,0], [0,0,0]])
    ):
    c = np.multiply(p, curve.dot(p))
    return shift + scale.dot(p) + c

def to_sphere(p, rad=10.0, shift=np.array([0,0,0]), hshift=0, vshift=0):
    x = (p[0] + hshift)/rad
    y = (p[1] + vshift)/rad
    return shift + rad*np.array([np.cos(y)*np.sin(x), np.sin(y), np.cos(y)*np.cos(x) - 1])
