width, height = 1085, 735
size = width, height
ai_mode = pathfinding = dirty_rects = visuals = stats = False
move_frames = 12
FPS = 60
ppg = 35
__config = None


def init(config):
    global size, width, height, ppg, ai_mode, pathfinding, dirty_rects, move_frames, FPS, visuals, stats, __config
    __config = config
    _set('width')
    _set('height')
    size = width, height
    _set('ppg')
    _set('ai_mode', 'ai')
    pathfinding = ai_mode or (not config['no_pathfinding'])
    _set('dirty_rects')
    _set('move_frames')
    _set('FPS', 'fps')
    _set('visuals', 'no_visuals', True)
    _set('stats', 'no_stats', True)


def _set(prop, alias=None, reverse=False):
    cprop = alias or prop
    val = __config[cprop]
    if type(val) is bool:
        if reverse:
            globals()[prop] = not val
        else:
            globals()[prop] = __config[cprop]
    elif __config[cprop]:
        globals()[prop] = __config[cprop]


def toggle(prop):
    val = globals()[prop]
    if type(val) is bool:
        globals()[prop] = not val
