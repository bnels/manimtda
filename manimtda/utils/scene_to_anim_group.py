from manimlib.imports import *

class GroupingScene(Succession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animations = list(self.animations or [])
        self.time=0

    def wait(self, duration=1):
        self.animations.append(Animation(Mobject(), run_time=duration))
        self.time+=duration
        return

    def play(self, *args, **kwargs):
        animations = self.compile_play_args_to_animation_list(
                *args, **kwargs
            )
        grp = AnimationGroup(*animations)
        self.animations.append(grp)
        self.time+=grp.run_time
        return

    def add(self, *args):
        self.animations.append(FadeIn(*args, run_time=0))

def ScenesToAnimGroup(*classes, **kwargs):
    if len(classes) > 1:
        return AnimationGroup(
            *[ScenesToAnimGroup(cls, **kwargs) for cls in classes]
        )
    clazz = classes[0]
    class SGpScene(GroupingScene, clazz):
        def __init__(self, *a, **kw):
            GroupingScene.__init__(self, *a, **kw)
    instance = SGpScene(**kwargs)
    clazz.construct(instance)
    return Succession(*instance.animations, **kwargs)
