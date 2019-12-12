from manimlib.imports import *
import numpy as np

# import manimtda
from manimtda.linalg import *

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
