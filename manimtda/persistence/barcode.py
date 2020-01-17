from manimlib.imports import *
import numpy as np
import bats

class PersistenceBarcode(VGroup):
	def __init__(
		self,
		persistence_pairs,
		dims,
		colors,
		spacing=0.5,
		ignore_zero=True,
		**kwargs
	):
		super().__init__(**kwargs)
		self.persistence_pairs = np.array(persistence_pairs)
		self.dims = np.array(dims)
		self.colors = colors
		self.t = -np.inf # start time
		self.pt_data = []
		self.bars = []
		self.origin = ORIGIN
		self.scale = 1.0
		self.spacing = spacing
		self.nbars = 0
		self.ignore_zero = ignore_zero

		self.set_limits()

	def shift(self, offset, **kwargs):
		"""
		shift diagram by offset
		"""
		super().shift(offset, **kwargs)
		self.origin = self.origin + offset

	def scale_by(self, s):
		"""
		scale by factor s
		"""
		self.scale = self.scale * s

	def transform_coord(self, c):
		return self.scale * np.array(c) + self.origin

	def add_axes(self):
		pass

	def set_limits(self):
		"""
		set limits of axes
		"""
		inds = np.logical_and(self.persistence_pairs > -np.inf, self.persistence_pairs < np.inf)
		self.tmin = np.min(self.persistence_pairs[inds]) - 0.1
		self.tmax = np.max(self.persistence_pairs[inds]) + 0.1

	def step_to(self, t):
		"""
		step to time t
		"""
		t = min(t, self.tmax)
		anim = []
		if self.t == -np.inf:
			anim.extend(self.add_bars(t))
		else:
			anim.extend(self.update_bars(t)) # update existing points
			anim.extend(self.add_bars(t))
		self.t = t
		return anim

	def update_bars(self, t):
		anim = []
		for (data, b) in zip(self.pt_data, self.bars):
			y = data[4]
			st = self.transform_coord([data[0], y, 0])
			ed = self.transform_coord([min(data[1], t), y, 0])
			targbar = Line(st, ed, color=data[3])
			anim.append(Transform(b, targbar))
		return anim

	def add_bar(self, p, t, color):
		"""
		keep track of points that have been added:
			birth, death, current time, color
		"""
		if self.ignore_zero == True:
			lbar = p[1] - p[0]
			if lbar == 0:
				return
		y = -self.nbars * self.spacing
		self.pt_data.append([p[0], p[1], t, color, y])
		st = self.transform_coord([p[0], y, 0])
		ed = self.transform_coord([min(p[1], t), y, 0])
		bar = Line(st, ed, color=color)
		self.bars.append(bar)
		self.add(bar)
		self.nbars = self.nbars + 1
		return bar

	def add_bars(self, t):
		"""
		add points to diagram
		"""
		anim = []
		for p, d in zip(self.persistence_pairs, self.dims):
			if self.t < p[0] <= t:
				bar = self.add_bar(p, t, self.colors[d])
				if bar is not None:
					anim.append(ShowCreation(bar))
		return anim

def barcode_from_bats(F, colors, **kwargs):
	"""
	create persistence diagram from bats Filtration
	"""
	FC2 = bats.FilteredF2ChainComplex(F)
	RFC2 = bats.ReducedFilteredF2ChainComplex(FC2)
	ps = []
	ds = []
	for d in range(len(colors)):
		for p in RFC2.persistence_pairs(d):
			ds.append(p.dim())
			ps.append([p.birth(), p.death()])
	return PersistenceBarcode(ps, ds, colors, **kwargs)
