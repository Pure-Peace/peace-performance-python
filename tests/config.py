BEATMAP_DIR = r'./test_beatmaps/'

# Test beatmaps
PADORU = r'padoru.osu' # super short - 5kb
HITORIGOTO = r'hitorigoto.osu'  # short - 15kb
FREEDOM_DIVE = r'freedom_dive.osu'  # stream medium - 50kb
SOTARKS = r'sotarks.osu'  # jump medium - 68kb
GALAXY_BURST = r'galaxy_burst.osu'  # tech - 102kb
UNFORGIVING = r'unforgiving.osu'  # marathon - 238kb


def join_beatmap(beatmap: str) -> str:
    return BEATMAP_DIR + beatmap
