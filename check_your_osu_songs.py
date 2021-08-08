import os
import asyncio
import time
from peace_performance_python.prelude import *

osu_list = []
errs = {}

# Your osu songs
# Will traverse a directory and try to read and calculate all .osu files
OSU_SONGS_PATH = r'D:\osu\songs'


def walk(path):
    dirs = os.listdir(path)
    for pa in dirs:
        p = os.path.join(path, pa)
        if os.path.isdir(p):
            walk(p)
        elif p.endswith('.osu'):
            osu_list.append(p)
            print(f'\r[ {len(osu_list)} ] .osu files founded...', end='')


async def main():
    # Find out .osu files
    print(f'[ Walking ({OSU_SONGS_PATH}) Start... ]')
    walk(OSU_SONGS_PATH)
    print(f'\n[ Walking Done! ]')

    # Ready
    c, total = Calculator(), len(osu_list)
    done = total_dutaion = err_count = ok_count = 0

    # Start
    print('[ Start task ]')
    for f in osu_list:
        try:
            start = time.time_ns()
            c.calculate(await Beatmap(f))
            instant_ms = (time.time_ns() - start) / 1000 / 1000
            total_dutaion += instant_ms
            ok_count += 1
        except Exception as err:
            err_count += 1
            errs[f] = str(err)
        done += 1
        print(
            '\rBeatmap [{}] {}/{}; ok: {}, err: {}; total time: {:.2f}ms, avg: {:.2f}ms'.format(
                f, done, total, ok_count, err_count, total_dutaion, total_dutaion / done
            ), end=''
        )
    print('\n[ All DONE ]\nRaw Errs:')
    print(errs)


if __name__ == '__main__':
    asyncio.run(main())
