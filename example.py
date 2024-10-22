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



class FiltrationDiagram(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}
	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = RipsFiltration(pts)
		FC2 = bats.FilteredF2ChainComplex(Fbats)
		RFC2 = bats.ReducedFilteredF2ChainComplex(FC2)

		# subcomplex for 0-length gen
		p = RFC2.persistence_pairs(1)[1]
		v =  RFC2.representative(p)
		subcpx0 = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]
		coface0 = [Fbats.complex().get_simplex(p.dim()+1, p.death_ind())]

		ps = RFC2.persistence_pairs(1)
		lens = []
		for p in ps:
			lens.append(p.death() - p.birth())
		i = np.argmax(lens)
		p = ps[i]
		v =  RFC2.representative(p)
		subcpx1 = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]

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

		for t in [0.5, 1.0, 2.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.wait()

		# animate coloring of boundary and face
		SC0 = F.get_subcomplex(subcpx0)
		SCF = F.get_subcomplex(coface0)
		self.play(
			SC0.set_color,
			RED
		)
		self.wait()
		self.play(
			SCF.set_color,
			RED
		)
		self.wait()
		self.play(
			VGroup(SC0, SCF).set_color,
			BLACK
		)
		self.wait()

		# animate coloring of subcomplex
		SC = F.get_subcomplex(subcpx1)
		self.play(
			SC.set_color,
			RED
		)
		self.wait()
		self.play(
			SC.set_color,
			BLACK
		)

		for t in [3.0, 5.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.wait()


class Barcode(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}
	def construct(self):
		pairs = [[0,1], [0,np.inf], [0.75, 1.5]]
		dims = [0, 0, 1]
		colors = [BLUE, RED]
		PD = PersistenceBarcode(pairs, dims, colors, spacing=0.2)

		PD.shift(2*LEFT)
		PD.scale_by(1.5)
		print(PD.tmin, PD.tmax)

		self.play(*PD.step_to(0.5))
		self.wait()
		self.play(*PD.step_to(1.0))
		self.wait()
		self.play(*PD.step_to(np.inf))
		self.wait()

		self.play(
			PD.shift,
			LEFT
		)
		self.wait()


class FiltrationBarcode(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}
	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = RipsFiltration(pts)
		FC2 = bats.FilteredF2ChainComplex(Fbats)
		RFC2 = bats.ReducedFilteredF2ChainComplex(FC2)

		# subcomplex for 0-length gen
		p = RFC2.persistence_pairs(1)[1]
		v =  RFC2.representative(p)
		subcpx0 = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]
		coface0 = [Fbats.complex().get_simplex(p.dim()+1, p.death_ind())]

		ps = RFC2.persistence_pairs(1)
		lens = []
		for p in ps:
			lens.append(p.death() - p.birth())
		i = np.argmax(lens)
		p = ps[i]
		v =  RFC2.representative(p)
		subcpx1 = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]

		PD = barcode_from_bats(Fbats, [BLUE, RED], spacing=0.2)
		PD.shift(5*LEFT + UP)
		PD.scale_by(0.5)

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))

		F = filtration_from_bats(Fbats, pts, color=BLACK)
		F.shift(3*RIGHT)

		t = 0.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		self.play(*anim)
		self.wait()

		for t in [0.5, 1.0, 2.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.wait()

		# animate coloring of subcomplex
		SC = F.get_subcomplex(subcpx1)
		self.play(
			SC.set_color,
			RED
		)
		self.wait()
		self.play(
			SC.set_color,
			BLACK
		)

		for t in [3.0, 5.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.wait()

		PPs = AbstractPairs([2,2], [BLUE, RED]).shift(3*LEFT)
		self.play(Transform(PD, PPs))
		self.wait()

		PD2 = diagram_from_bats(Fbats, [BLUE, RED])
		PD2.shift(5*LEFT + DOWN)
		PD2.scale_by(0.5)
		PD2.step_to(5.0)

		self.play(Transform(PD, PD2))
		self.wait(2)


class Pairs(Scene):
	CONFIG = {
		"camera_config":{"background_color":WHITE},
	}
	def construct(self):
		PD = AbstractPairs([2, 2],[BLUE, RED])
		self.play(ShowCreation(PD))
		self.wait()
