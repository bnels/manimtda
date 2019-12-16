from manimlib.imports import *
import numpy as np

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



class PersistenceBarcode(PersistencePairs):
	def __init__(self, pairs, dims=None, spacing=0.5, **kwargs):
		self.pair_count = 0
		self.spacing=spacing
		super().__init__(pairs, dims, **kwargs)


	def add_pair(self, pair, **kwargs):
		self.add(
			Line(
				[pair[0],-self.spacing*self.pair_count,0],
				[pair[1],-self.spacing*self.pair_count, 0],
				**kwargs
			)
		)
		self.pair_count = self.pair_count + 1


	def creation_animations(self,
		start=0,
		end=None,
		run_time=None
	):
		if end is None:
			end = self.tmax()
		if run_time is None:
			run_time = end - start

		print(end, run_time)

		anim = []
		rlen = end - start

		for i, p in enumerate(self.pairs):
			if p[1] > start and p[0] < end:
				bstart = np.maximum(p[0], start)
				bend = np.minimum(p[1], end)
				sratio = (bstart - start)/(rlen)
				eratio = (bend)/(rlen)
				print(p, sratio, eratio, rlen)
				anim.append(ShowCreation(
					self[i],
					rate_func=squish_rate_func(linear, sratio, eratio),
					run_time=run_time)
				)

		return anim
