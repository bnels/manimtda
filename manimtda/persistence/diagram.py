"""
PersistenceDiagram
"""

from manimlib.imports import *
import numpy as np

class PersistenceDiagram(VGroup):
	def __init__(
		self,
		persistence_pairs,
		dims,
		colors,
		**kwargs
	):
		super().__init__(**kwargs)
		self.persistence_pairs = np.array(persistence_pairs)
		self.dims = np.array(dims)
		self.colors = colors
		self.t = -np.inf # start time
		self.pt_data = []
		self.pts = []
		self.origin = ORIGIN
		self.scale = 1.0

		self.set_limits()

	def shift(self, offset):
		"""
		shift diagram by offset
		"""
		self.origin = self.origin + offset

	def scale_by(self, s):
		"""
		scale by factor s
		"""
		self.scale = self.scale * s


	def add_axes(self):
		# x axis
		xax = Line(self.scale * self.tmin*LEFT + self.origin, self.scale * self.tmax*RIGHT + self.origin, color=BLACK)
		yax = Line(self.scale * self.tmin*DOWN + self.origin, self.scale * self.tmax*UP + self.origin, color=BLACK)
		dax = Line(self.scale * np.array([self.tmin, self.tmin, 0]) + self.origin, self.scale * np.array([self.tmax, self.tmax, 0]) + self.origin, color=DARK_GREY)
		self.add(xax)
		self.add(yax)
		self.add(dax)
		return VGroup(dax, xax, yax)

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
			self.bar = Line(self.scale *np.array([self.tmin, t, 0]) + self.origin, self.scale * np.array([t, t, 0]) + self.origin, color=GREY)
			anim.append(FadeInFrom(self.bar, DOWN))
			anim.extend(self.add_pts(t))
		else:
			bartarg = Line(self.scale * np.array([self.tmin, t, 0]) + self.origin, self.scale* np.array([t, t, 0]) + self.origin, color=GREY)
			anim.append(Transform(self.bar, bartarg))
			anim.extend(self.update_pts(t)) # update existing points
			anim.extend(self.add_pts(t))
		self.t = t
		return anim

	def update_pts(self, t):
		anim = []
		for (data, p) in zip(self.pt_data, self.pts):
			targpt = Dot(self.scale *np.array([data[0], min(data[1], t), 0]) + self.origin, color=data[3])
			anim.append(Transform(p, targpt))
		return anim

	def add_pt(self, p, t, color):
		"""
		keep track of points that have been added:
			birth, death, current time, color
		"""
		self.pt_data.append([p[0], p[1], t, color])
		pt = Dot(self.scale *np.array([p[0], min(p[1], t), 0]) + self.origin, color=color)
		self.pts.append(pt)
		return pt

	def add_pts(self, t):
		"""
		add points to diagram
		"""
		anim = []
		for p, d in zip(self.persistence_pairs, self.dims):
			if self.t < p[0] <= t:
				anim.append(FadeInFrom(self.add_pt(p, t, self.colors[d]), DOWN))
		return anim
