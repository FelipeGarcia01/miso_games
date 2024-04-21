from typing import List


class CAnimation:
    def __init__(self, animations: dict) -> None:
        self.number_frames = animations.get('number_frames')
        self.animations_list: List[AnimationData] = []
        for animation in animations.get('list'):
            data = AnimationData(
                animation.get('name'),
                animation.get('start'),
                animation.get('end'),
                animation.get('framerate'))
            self.animations_list.append(data)
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animations_list[self.current_animation].start


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate


def set_animation(c_a: CAnimation, target: int):
    if c_a.current_animation == target: return
    c_a.time = 0
    c_a.current = target
    c_a.frame = c_a.animations_list[c_a.current].start
