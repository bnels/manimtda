from manimlib.imports import *
import numpy as np
import bats

# import manimtda
from manimtda import *

class LEUP(Scene):
	def construct(self):
		title = TextMobject("LEUP Factorization")
		self.play(
			Write(title),
		)
		self.wait()

		A = Square()
		self.play(
			FadeOut(title),
			ShowCreation(A)
		)
		self.wait()

		L = Lmat()
		U = Umat()
		EL = ELmat()
		P = Pmat().shift(2.25*RIGHT)
		self.play(
			ShowCreation(L),
			ShowCreation(U),
			ShowCreation(P),
		)

		self.wait()

		self.play(
			FadeIn(EL),
			ApplyMethod(L.shift, 2.25*LEFT),
			ApplyMethod(U.shift, 2.25*RIGHT),
			ApplyMethod(P.shift, 2.25*RIGHT),
			FadeOut(A)
		)

		self.wait(2)


class TriComplex(ThreeDScene):
	def construct(self):
		triangles = get_triangles()

		tri1 = [triangles[i] for i in range(16) if i not in (5, 10)]

		X0 = create_0skel(tri1)
		X1 = create_1skel(tri1)
		X2 = create_2skel(tri1)

		self.play(
			ShowCreation(X0),
		)
		self.play(
			ShowCreation(X1),
		)
		self.play(
			ShowCreation(X2)
		)
		self.play(
			FadeOut(X0),
			FadeOut(X1),
			run_time=0.1
		)

		rad = 2.5
		vshift=0.5
		hshift=-0.5
		shift = np.array([4, 0, 0])
		scale = np.array([[1, 0, 0.00], [0, 1, 0.00], [0, 0, 0]])
		curve = np.array([[0.04, -0.03, 0], [-0.03, 0.05, 0], [0, 0, 0]])
		# to_manifold(p, shift=shift, scale=scale, curve=curve)

		self.play(
			X2.apply_function,
			lambda p: to_sphere(p, rad=rad, shift=shift, hshift=hshift),
			run_time=3,
		)


		subcpx = [triangles[i] for i in (5, 10)]
		S2 = create_2skel(subcpx, color=RED)

		self.play(
			ShowCreation(S2)
		)

		self.play(
			S2.apply_function,
			lambda p: to_sphere(p, rad=rad, shift=shift, hshift=hshift),
			run_time=3,
		)

		# S2.color = BLUE
		# S2.init_colors().set_fill(BLUE, opacity=0.5)
		self.play(
			S2.set_color,
			BLUE
		)

		self.wait(2)


def gen_circle(n=10, r=3):
	theta = [2*np.pi * i/n for i in range(n)]
	pts = [[r*np.cos(t), r*np.sin(t), 0] for t in theta]
	return np.array(pts)


class Rips(Scene):
	def construct(self):
		pts = gen_circle(n=10)
		#print(pts.shape)
		pts = pts + np.random.normal(0, 0.2, size=pts.shape)


		simplices, times = get_Rips_filtration(pts, rmax=5.0)

		X = SimplicialFiltration(pts,simplices,times, tri_opacity=0.2, color=BLUE) #.move_to(3*RIGHT)

		anim = []
		maxt = X.last_time()
		for t in X.time_steps():
			#print(t)
			Xt = X.step_to(t)
			anim.append(FadeIn(
				Xt,
				rate_func=squish_rate_func(linear, t/(t+1), 1),
				run_time=t+1)
			)
			# anim.append(*self.compile_play_args_to_animation_list(
			# 	Xt.set_color,
			# 	BLUE,
			# 	rate_func=squish_rate_func(linear, (t+1)/(t+2), 1),
			# 	run_time=t+2
			# )
			# )

		self.play(*anim)
		self.wait(3)
		rad = 2.5
		vshift=0.5
		hshift=-0.5
		shift = np.array([2, 0, 0])
		self.play(
			X.apply_function,
			lambda p: to_sphere(p, rad=rad, shift=shift, vshift=vshift, hshift=hshift),
			run_time=3,
		)
		self.wait(2)

		self.play(FadeOut(X), run_time=3)
		self.wait(2)


class Barcode(Scene):
	def construct(self):
		pairs = [
		[0,3],
		[0,1],
		[1,2],
		[2,3],
		]
		BC = PersistenceBarcode(pairs, spacing=0.25, color=RED)
		self.play(
			*BC.creation_animations()
		)
		self.wait(2)


def gen_circle2(n, r=1.0):
    theta = np.linspace(0, 2*np.pi*(1 - 1./n), n)
    pts = np.array([r*np.cos(theta), r*np.sin(theta)],  dtype=np.float, order='F')
    return pts.T


def Transform_circle_radii(cs, r, **kwargs):
	"""
	transform each circle in cs to have radius r
	"""
	pts = [c.arc_center for c in cs]
	cs1 = [Circle(radius=r, arc_center=p, **kwargs) for p in pts]
	return [Transform(c0, c1) for c0, c1 in zip(cs, cs1)]

from itertools import combinations
from scipy.spatial import Delaunay
from scipy.spatial import distance

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


class GrowBalls(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}

	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = RipsFiltration(pts)

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))

		F = filtration_from_bats(Fbats, pts, color=BLACK)

		circle_opts = {"color":BLUE, "fill_opacity":0.2}
		ds = [Circle(radius=0.05, arc_center=p, color=BLACK, fill_opacity=1.0) for p in pts]
		self.play(
			*(FadeIn(d) for d in ds)
		)
		cs = [Circle(radius=0.1, arc_center=p, **circle_opts) for p in pts]
		self.play(
			*(FadeIn(c) for c in cs)
		)
		self.wait()
		# cs1 = [Circle(color=BLUE, radius=1.5, fill_opacity=0.2, arc_center=p) for p in pts]
		t = 0.5
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.wait()

		t = 1.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.wait()

		t = 2.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.wait()

		t = 3.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.wait()

		t = 5.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.wait()



		self.play(
			*(FadeOut(c) for c in cs)
		)



class Diagram(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}
	def construct(self):
		pairs = [[0,1], [0,np.inf], [0.75, 1.5]]
		dims = [0, 0, 1]
		colors = [BLUE, RED]
		PD = PersistenceDiagram(pairs, dims, colors)

		PD.shift(2*LEFT)
		PD.scale_by(1.5)
		print(PD.tmin, PD.tmax)

		ax = PD.add_axes()
		self.play(ShowCreation(ax))
		self.wait()

		self.play(*PD.step_to(0.5))
		self.wait()
		self.play(*PD.step_to(1.0))
		self.wait()
		self.play(*PD.step_to(np.inf))
		self.wait()


def diagram_from_bats(F, colors):
	"""
	create persistence diagram from bats
	"""
	FC2 = bats.FilteredF2ChainComplex(F)
	RFC2 = bats.ReducedFilteredF2ChainComplex(FC2)
	ps = []
	ds = []
	for d in range(len(colors)):
		for p in RFC2.persistence_pairs(d):
			ds.append(p.dim())
			ps.append([p.birth(), p.death()])
	return PersistenceDiagram(ps, ds, colors)



class FiltrationDiagram(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}
	def construct(self):
		pts = gen_circle2(10, r=2.5)
		pts = pts + np.random.normal(scale=0.15, size=pts.shape)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = RipsFiltration(pts)
		FC2 = bats.FilteredF2ChainComplex(Fbats)
		RFC2 = bats.ReducedFilteredF2ChainComplex(FC2)
		p = RFC2.persistence_pairs(1)[0]
		v =  RFC2.representative(p)
		subcpx = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]

		PD = diagram_from_bats(Fbats, [BLUE, RED])
		PD.shift(5*LEFT + DOWN)
		PD.scale_by(0.5)

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))

		F = filtration_from_bats(Fbats, pts, color=BLACK)
		F.shift(3*RIGHT)

		t = 0.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		self.play(*anim)
		ax = PD.add_axes()
		self.play(ShowCreation(ax))
		self.wait()

		for t in [0.5, 2.0, 3.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.wait()

		# animate coloring of subcomplex
		SC = F.get_subcomplex(subcpx)
		self.play(
			SC.set_color,
			RED
		)
		self.wait()
		self.play(
			SC.set_color,
			BLACK
		)


		for t in [4.0, 5.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.wait()
