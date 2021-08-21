from peace_performance_python.prelude import *
from tests import join_beatmap, HITORIGOTO


# *No longer available by default (compile without `rust_logger` features enabled)*
# Initialize Rust logger (optional)
'''
set_log_level('trace')
init_logger()
'''


def main():
    path = join_beatmap(HITORIGOTO)
    # Load beatmap
    b = Beatmap(path)
    print('\n>>>>> Beatmap:', b)
    print('\n>>>>> Beatmap.hit_objects (0-3):', b.hit_objects[:3])
    print('\n>>>>> Beatmap.timing_points:', b.timing_points)
    print('\n>>>>> Beatmap.difficulty_points (0-3):', b.difficulty_points[:3])
    print('\n>>>>> Beatmap.hit_objects[0].pos:', b.hit_objects[0].pos)
    print('\n>>>>> Beatmap.hit_objects[3].kind:', b.hit_objects[3].kind)
    print('\n>>>>> Beatmap.hit_objects[3].kind.curve_points:',
          b.hit_objects[3].kind.curve_points)

    pos_0 = b.hit_objects[0].pos
    pos_1 = b.hit_objects[1].pos
    print('\n>>>>> Beatmap object(0):', b.hit_objects[0])
    print('\n>>>>> Beatmap object(1):', b.hit_objects[1])
    print('\n>>>>> Beatmap object pos(0):', pos_0)
    print('\n>>>>> Beatmap object pos(1):', pos_1)
    print('\n>>>>> Beatmap object pos(0) length, squared:',
          pos_0.length, pos_0.length_squared)
    print('\n>>>>> Beatmap object pos(0 and 1) distance:', pos_0.distance(pos_1))
    print('\n>>>>> Beatmap object pos(0 and 1) add:', pos_0.add(pos_1))
    print('\n>>>>> Beatmap object pos(0 and 1) sub:', pos_0.sub(pos_1))


if __name__ == '__main__':
    main()
