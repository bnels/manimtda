import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import combinations
from scipy.spatial import Delaunay
from scipy.spatial import distance
import bats


def get_Rips_filtration(pts, rmax=np.inf):
	pts = np.array(pts)
	simplices = []
	times = []
	n = len(pts)
	dists = squareform(pdist(pts))

	for i in range(n):
		simplices.append([i])
		times.append(0)

	for i in range(n):
		for j in range(i):
			if dists[i,j] <= rmax:
				simplices.append([j,i])
				times.append(dists[i,j])

	for i in range(n):
		for j in range(i):
			for k in range(j):
				tijk = np.max([dists[i,j], dists[i,k], dists[j,k]])
				if tijk <= rmax:
					simplices.append([k, j,i])
					times.append(np.max([dists[i,j], dists[i,k], dists[j,k]]))

	return simplices, times



def unique_edges(faces):
    """
    obtain unique simplices up to dimension dim from faces
    """
    edges = []
    # loop over faces
    for face in faces:
        # loop over dimension
        for s in combinations(face, 2):
            edges.append(np.sort(list(s)))

    edges = np.unique(edges, axis=0)

    return edges


def WeakAlphaFiltration(pts, dist=distance.euclidean, maxdim=2, t0=0.):
    """
    2D weak alpha filtration
    """
    tri = Delaunay(pts)
    edges = unique_edges(tri.simplices)
    fedges = []
    for e in edges:
        fedges.append(bats.FilteredEdge(*e, dist(pts[e[0]], pts[e[1]])))

    F = bats.FlagFiltration(fedges, pts.shape[0], maxdim, t0)
    return F

def RipsFiltration(pts, maxdim=2):
	pts = np.array(pts.T, dtype=np.float, order='F')
	data = bats.DataSet(bats.DenseDoubleMatrix(pts))
	return bats.RipsFiltration(data, bats.Euclidean(), np.inf, maxdim)
