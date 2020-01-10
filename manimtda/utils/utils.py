from manimlib.imports import *
from contextlib import contextmanager

def Grp(*lst):
    vmo = VMobject()
    vmo.add(*lst)
    return vmo

def MoveTo(lst1,lst2):
    return [ApplyMethod(x.move_to,y) for x,y in zip(lst1,lst2)]

def copy_objs(lst):
    return [x.copy() for x in lst]

def CreateMoveToTargetCtxtMgr(scene):
    @contextmanager
    def the_targets_of(*lst):
        lst_t=copy_objs(lst)
        yield tuple(lst_t)
        scene.play(
            *MoveTo(lst, lst_t),
        )
    return the_targets_of

class Seq(VMobject):
    def __init__(self,*lst,**kwargs):
        VMobject.__init__(self, **kwargs)
        self.add(*lst)
        self.lst = lst
    def __call__(self):
        return self.lst
    def anchor_position(self, idx, buff = SMALL_BUFF):
        anchor = self.lst[idx]
        for i in range(idx+1,len(self.lst)):
            self.lst[i].next_to(anchor,RIGHT,buff = buff)
            anchor = self.lst[i]
        anchor = self.lst[idx]
        for i in range(idx-1,-1,-1):
            self.lst[i].next_to(anchor,LEFT, buff = buff)
            anchor = self.lst[i]
        return self
