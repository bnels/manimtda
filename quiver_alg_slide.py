from manimlib.imports import *
from manim_reveal import SlideScene
from manimtda.linalg.shapes import *
from manimtda.utils import *



class LEUPFact(VMobject):
    def __init__(self,A,Arr,put_on_arrow,mat_buff,**kwargs):
        self.L = Lmat(corner_radius=0.1)
        self.U = Umat(corner_radius=0.1)
        self.EL = ELmat(color=BLACK)
        self.P = Pmat(color=BLACK)

        lst = [self.L, self.EL, self.U, self.P]

        VMobject.__init__(self, **kwargs)
        self.add(*lst)

        self.lst = lst
        self.Arr = Arr
        self.A = A
        self.put_on_arrow = put_on_arrow
        self.mat_buff=mat_buff

    def position(self):
        mats=Grp(*self.lst)
        self.put_on_arrow(mats,self.Arr)
        self.P.next_to(self.A,RIGHT,buff = self.mat_buff)


    def __call__(self):
        return self.lst

    def make_target(self):
        [Lt, ELt, Ut, Pt] = copy_objs(self.lst)
        Seq(Lt, ELt, Ut, Pt).anchor_position(1,self.mat_buff)
        self.put_on_arrow(Grp(Lt, ELt, Ut, Pt),self.Arr)
        self.target=[Lt, ELt, Ut, Pt]

    def play_factorize(self,scene):
        self.make_target()
        scene.play(
            ShowCreation(self.L),
            ShowCreation(self.U),
            ShowCreation(self.P),
        )
        scene.play(
            *MoveTo(self.lst, self.target),
            FadeOut(self.A)
        )




class QuiverAlg(SlideScene):
    CONFIG={
        "camera_config":{"background_color":WHITE},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):
        title = TextMobject("Quiver Algorithm",color=BLACK)
        title.shift(2.5 * UP)
        self.add(title)

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        # Make quiver
        tA = TexMobject("\\cdot",color=BLACK)
        tB = TexMobject("\\cdot",color=BLACK)
        tC = TexMobject("\\cdot",color=BLACK)

        tArr = TexMobject("\\xleftarrow{\\makebox[1cm]{}}",color=BLACK);
        tArr2 = tArr.copy()
        put_on_arrow =lambda x,Ar: x.next_to(Ar,TOP,buff=SMALL_BUFF)

        # Position elements of quiver
        Grp(tA,tArr,tB,tArr2,tC).scale(2)
        Seq(tA,tArr,tB,tArr2,tC).anchor_position(2)

        # Add quiver
        self.play(FadeIn(Grp(tA,tArr,tB,tArr2,tC)))
        self.play()
        self.slide_break()

        # create two matrices and put on arrows
        A = Square(color=BLACK)
        A2 = Square(color=BLACK)
        Grp(A,A2).scale(0.2)
        put_on_arrow(A,tArr)
        put_on_arrow(A2,tArr2)
        self.play(FadeIn(Grp(A,A2)))
        self.slide_break()

        # factorize A1
        fact1=LEUPFact(A,tArr,put_on_arrow,SMALL_BUFF)
        fact1.scale(0.2)
        fact1.position()
        fact1.play_factorize(self)
        self.slide_break()

        # Matrix pass U,P
        [L,EL,U,P] = fact1()
        with the_target_of(L,EL,U,P,A2) as (Lt,ELt,Ut,Pt,A2t):
            Seq(Ut,Pt,A2t)\
                .anchor_position(0)\
                .next_to(tArr2,TOP,buff=SMALL_BUFF)

            Seq(Lt,ELt)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
        self.slide_break()

        #Multiply UPA2
        with the_target_of(U,P,A2) as [Ut,Pt,A2t]:
            put_on_arrow(A2t,tArr2)
            Ut.move_to(A2t)
            Pt.move_to(A2t)
        self.play(
             FadeOut(U),
             FadeOut(P)
        )
        self.slide_break()
        lel1 = Seq(L,EL)

        # Factorize A2
        fact2=LEUPFact(A2,tArr2,put_on_arrow,SMALL_BUFF)
        fact2.scale(0.2)
        fact2.position()
        fact2.play_factorize(self)
        self.slide_break()

        # Matrix pass UP
        [L,EL,U,P] = fact2()
        self.play(
             FadeOutAndShift(U,2*RIGHT),
             FadeOutAndShift(P,2*RIGHT)
        )
        lel2 = Seq(L,EL)
        with the_target_of(L,EL) as (Lt,ELt):
            Seq(Lt,ELt)\
                .anchor_position(0)\
                .next_to(tArr2,TOP,buff=SMALL_BUFF)
        self.slide_break()

        ###--BACKWARD PASS--

        #Matrix pass L2
        L1,EL1 = lel1()
        L2,EL2 = lel2()
        with the_target_of(L1,EL1,L2,EL2) as (L1t,EL1t,L2t,EL2t):
            Seq(L1t,EL1t,L2t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
            Seq(EL2t)\
                .anchor_position(0)\
                .next_to(tArr2,TOP,buff=SMALL_BUFF)
        self.slide_break()

        # commute
        with the_target_of(L1,EL1,L2) as (L1t,EL1t,L2t):
            Seq(L1t,L2t,EL1t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
        self.slide_break()

        # multiply
        with the_target_of(L1,EL1,L2) as (L1t,EL1t,L2t):
            Seq(L1t,EL1t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
            L2t.move_to(L1t)

        self.play(
             FadeOut(L2)
        )
        self.slide_break()

        # matrix pass L1
        self.play(
             FadeOutAndShift(L1,2*LEFT),
        )
        with the_target_of(EL1) as [EL1t]:
            Seq(EL1t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)

        self.wait(1);


def make_quiver(lenq=10):
    dot = TexMobject("\\cdot",color=BLACK)
    tArr = TexMobject("\\xleftarrow{\\makebox[1cm]{}}",color=BLACK);

    dots = []
    arrows = []
    quiver = []
    for i in range(lenq-1):
        new_dot = dot.copy()
        new_arr = tArr.copy()

        dots+= [new_dot]
        arrows += [new_arr]
        quiver += [ new_dot, new_arr]

    new_dot = dot.copy()

    dots+= [new_dot]
    quiver += [ new_dot]

    return dots,arrows,quiver


class FullQuiverAlg(SlideScene):
    CONFIG={
        "camera_config":{"background_color":WHITE},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):
        title = TextMobject("Quiver Algorithm",color=BLACK)
        title.shift(2.5 * UP)
        self.add(title)

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        #Some constants
        lenq=7
        scale_fac=2
        arrow_buff=SMALL_BUFF/5
        mat_buff=SMALL_BUFF
        # Make quiver

        dots,arrows,quiver=make_quiver(lenq)
        put_on_arrow =lambda x,Ar: x.next_to(Ar,TOP,buff=arrow_buff)

        qu=Seq(*quiver)
        qu.anchor_position(len(quiver)//2)
        qu.scale(2/scale_fac)
        self.add(qu)

        #make matrices
        As=[]
        for i in range(lenq-1):
            A = Square(color=BLACK)
            As += [A]
            A.scale(0.2/scale_fac)
            put_on_arrow(A,arrows[i])

        self.play(FadeIn(Grp(*As)))
        self.slide_break()

        #forward pass
        facts=[]
        lels = []
        for i in range(lenq-1):
            # factorize
            fact1=LEUPFact(As[i],arrows[i],put_on_arrow,mat_buff)
            fact1.scale(0.2/scale_fac)
            fact1.position()
            fact1.play_factorize(self)
            facts +=[fact1]
            #self.slide_break()

            # Matrix pass U,P
            [L,EL,U,P] = fact1()
            if i<lenq-2 :
                with the_target_of(L,EL,U,P,As[i+1]) as (Lt,ELt,Ut,Pt,A2t):
                    s= Seq(Ut,Pt,A2t)
                    s.anchor_position(0,mat_buff)
                    put_on_arrow(s,arrows[i+1])

                    s2 = Seq(Lt,ELt)
                    s2.anchor_position(0,mat_buff)
                    put_on_arrow(s2,arrows[i])
                lel1 = Seq(L,EL)
                lels+=[lel1]
                #self.slide_break()
            else:
                self.play(
                     FadeOutAndShift(U,2*RIGHT),
                     FadeOutAndShift(P,2*RIGHT)
                )
                lel2 = Seq(L,EL)
                lels+=[lel2]
                with the_target_of(L,EL) as (Lt,ELt):
                    s=Seq(Lt,ELt)
                    s.anchor_position(0,mat_buff)
                    put_on_arrow(s,arrows[i])
                #self.slide_break()

            #Multiply UPA2
            if i<lenq-2 :
                with the_target_of(U,P,As[i+1]) as [Ut,Pt,A2t]:
                    put_on_arrow(A2t,arrows[i+1])
                    Ut.move_to(A2t)
                    Pt.move_to(A2t)
                self.play(
                     FadeOut(U),
                     FadeOut(P)
                )
            #self.slide_break()

        self.slide_break()
        # Backward pass
        for i in range(lenq-2,-1,-1):
            # Matrix pass L2
            if i>0:
                L1,EL1 = lels[i-1]()
                L2,EL2 = lels[i]()
                with the_target_of(L1,EL1,L2,EL2) as (L1t,EL1t,L2t,EL2t):
                    s=Seq(L1t,EL1t,L2t)
                    s.anchor_position(0,mat_buff)
                    put_on_arrow(s,arrows[i-1])
                    s2=Seq(EL2t)
                    s2.anchor_position(0,mat_buff)
                    put_on_arrow(s2,arrows[i])
                #self.slide_break()

                # commute
                with the_target_of(L1,EL1,L2) as (L1t,EL1t,L2t):
                    s=Seq(L1t,L2t,EL1t)
                    s.anchor_position(0)
                    put_on_arrow(s,arrows[i-1])
                #self.slide_break()

                # multiply
                with the_target_of(L1,EL1,L2) as (L1t,EL1t,L2t):
                    s=Seq(L1t,EL1t)
                    s.anchor_position(0,mat_buff)
                    put_on_arrow(s,arrows[i-1])
                    L2t.move_to(L1t)

                self.play(
                     FadeOut(L2)
                )
                #self.slide_break()
            else:
                # matrix pass L1
                L1,EL1 = lels[i]()
                self.play(
                     FadeOutAndShift(L1,2*LEFT),
                )
                with the_target_of(EL1) as [EL1t]:
                    s=Seq(EL1t)
                    s.anchor_position(0,mat_buff)
                    put_on_arrow(s,arrows[i])

        self.slide_break()
        self.wait(2)
