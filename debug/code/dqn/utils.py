import traceback
import numpy as np

debug_colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
debug_idxs = 0

def colorstr(*input):
  # Colors a string https://en.wikipedia.org/wiki/ANSI_escape_code, i.e.  colorstr('blue', 'hello world')
  *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])  # color arguments, string
  colors = {
    'black': '\033[30m',  # basic colors
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright_black': '\033[90m',  # bright colors
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
    'end': '\033[0m',  # misc
    'bold': '\033[1m',
    'underline': '\033[4m'}
  return ''.join(colors[x] for x in args) + f'{string}' + colors['end']

def show_debug(info, ptext="[DEBUG]", render_cfg=None, verbose_depth=1, show=True):
  def from_pos(depth=1):
    tmp = frame_summary[-1-depth]
    return f"<{tmp.filename}, line {tmp.lineno}> in {tmp.name} "

  frame_summary = traceback.extract_stack()
  verbose_depth = min(verbose_depth, len(frame_summary)-1)
  if not isinstance(info, tuple):
     info = (info,)
  if render_cfg is None:
    global debug_idxs
    render_cfg = (debug_colors[debug_idxs], 'bold')
    debug_idxs = (debug_idxs + 1) % len(debug_colors)

  s = ""
  for i in range(verbose_depth):
    tmp = ' FROM ' if i == 0 else ' IN   '
    s += colorstr(*render_cfg, f"{ptext+tmp+from_pos(i+1):+<120}") + '\n'
  for i in info:
    s += str(i) + ' '
  s += '\n'
  s += colorstr(*render_cfg, f"{ptext+' END  '+from_pos(1):-<120}")
  if show: print(s)
  return s

def is_iterable(x):
  return isinstance(x, list) or isinstance(x, dict)

def show_iter(x, indent=2, max_width=50):
  string = ""
  indent_str = ' ' * indent
  if is_iterable(x) and len(str(x)) + indent + 2 > max_width:
    if isinstance(x, dict):
      string += '{\n'
      for k, v in x.items():
        string += indent_str + f"{k}: "
        string += show_iter(v, indent=indent+2)
        string += ',\n'
      string += indent_str[:-2] + '}'
    if isinstance(x, list):
      string += '[\n'
      for v in x:
        string += indent_str + show_iter(v, indent=indent+2) + ',\n'
      string += indent_str[:-2] + ']'
  elif isinstance(x, np.ndarray):
    string += f"({x.dtype}) "
    if x.ndim > 1: string += '\n'
    string += str(x)
  else:
    string += str(x)
  return string

def show_time(second):
  s = int(second)
  m = int(second // 60)
  h = int(m // 60)
  ret = ""
  if h: ret += f"{h:02}:"
  ret += f"{int(m%60):02}:{int(s%60):02}"
  return ret

if __name__ == '__main__1':
  print(colorstr('red', "hi"))
  def foo():
    show_debug("hi", verbose_depth=10)
  foo()

if __name__ == '__main__':
  s = show_debug("hi", verbose_depth=10, show=False)
  print(s)
  # a = {'1': [1,2,3], '2': [{'b': 3}, {'a': 2}], '3': np.arange(10).reshape(2, 5), '4': np.arange(3)}
  # # a = {'1': [1,2,3], '2': [{'b': 3}, {'a': 2}], }
  # print(show_iter(a))
