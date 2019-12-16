import numpy as np
from scipy.spatial.distance import pdist, squareform

def get_Rips_filtration(pts, tmax=np.inf):
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
			if dists[i,j] <= tmax:
				simplices.append([j,i])
				times.append(dists[i,j])

	for i in range(n):
		for j in range(i):
			for k in range(j):
				tijk = np.max([dists[i,j], dists[i,k], dists[j,k]])
				if tijk <= tmax:
					simplices.append([k, j,i])
					times.append(np.max([dists[i,j], dists[i,k], dists[j,k]]))

	return simplices, times
