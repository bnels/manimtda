from manimlib.imports import *

class AbstractPairs(VGroup):
	def __init__(self, npairs, colors, **kwargs):
		"""
		create npairs[d] in dimenion d
		{(b_0, d_0), (b_1, d_1), ...}
		"""
		super().__init__(**kwargs)

		self.hdim = []

		for n, c in zip(npairs, colors):
			self.add_dim(n, c)

	def add_dim(self, n, c):
		str = '\{ '
		for i in range(n):
			str = str + "(b_{:d}, d_{:d}),".format(i, i)
		str = str + ' \\dots \}'
		print(str)
		obj = TexMobject(str, color=c)
		d = len(self.hdim)
		if d > 0:
			obj.next_to(self.hdim[d-1], DOWN)

		self.hdim.append(obj)
		self.add(obj)



class PersistencePairs(VGroup):
	def __init__(
		self,
		pairs,
		dims = None,
		**kwargs
	):
		super().__init__(**kwargs)

		self.pairs = pairs
		self.dims = dims
		self.ct = 0

		for p in pairs:
			self.add_pair(p, **kwargs)

	def add_pair(self, pair, **kwargs):
		raise NotImplementedError

	def tmax(self):
		ret = -np.inf
		for p in self.pairs:
			ret = np.maximum(ret, p[1])

		return ret
