from manimlib.imports import *
import numpy as np

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

		X = SimplicialComplex(pts,simplices,times, tri_opacity=0.2, color=BLUE) #.move_to(3*RIGHT)

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
