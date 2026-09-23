import itertools
import math
####
# This module is taken from the treeart module on PIP.
#
#
#
####

def find_width(s):
    return max(len(l) for l in s.splitlines())

uni_h, uni_v, uni_tl, uni_tr, uni_br, uni_bl, uni_invt, uni_t, nl = '\u2500\u2502\u256d\u256e\u256f\u2570\u2534\u252c\n'
stripped = uni_h + uni_tl + uni_tr + ' '

def box(s, hpad=0):
    s = str(s)
    w = find_width(s)
    padstr = ' ' * hpad
    res = uni_tl + uni_h * (w + 2 * hpad) + uni_tr + nl
    for l in s.splitlines():
        res += uni_v + padstr + l.rjust(w) + padstr + uni_v + nl
    res += uni_bl + uni_h * (w + 2 * hpad) + uni_br
    return res
    
''' ensure_padded: ensures a multiline string is padded by at least l space on the left and r space on the right '''

def padded_lines(s, pad_l, pad_r):
    r_col, l_col = 0, math.inf
    lines = s.splitlines()
    for line in lines:
        if line.isspace(): continue
        r_col = max(r_col, len(line.rstrip()))
        l_col = min(l_col, len(line) - len(line.lstrip()))
    extra_l = max(pad_l - l_col, 0)
    trim_l = max(l_col - pad_l, 0)
    prefix = ' ' * extra_l
    return [prefix + line[trim_l:].rstrip().ljust(r_col + pad_r) for line in s.splitlines()]

def pad(s, l, r):
    lstr = ' ' * l
    rstr = ' ' * r
    return '\n'.join(lstr + l + rstr for l in s.splitlines())

def find_span(s):
    n = len(s)
    r = len(s.rstrip(stripped))
    l = n - len(s.lstrip(stripped))
    return l, (l + r) // 2, r

def as_lines(s):
    return s.splitlines() if isinstance(s, str) else s
        
def join_horizontal(a, b, prefix=None, lwidth=0, gap=1):
    res = prefix or []
    gap_str = ' ' * gap
    for a_line, b_line in itertools.zip_longest(as_lines(a), as_lines(b), fillvalue=''):
        res.append(a_line.ljust(lwidth) + gap_str + b_line)
    return '\n'.join(res)

def binary_edge(p, a, b, align='upper', gap=False):
    p = str(p)
    
    a_first, *a_rest = a = padded_lines(str(a), 0, 1)
    b_first, *b_rest = b = padded_lines(str(b), 1, 0)
    w_a, w_b = len(a_first), len(b_first)
    (a_l, a_m, a_r), (b_l, b_m, b_r) = find_span(a_first), find_span(b_first)
    
    # |-------xh------|
    # |---xp---|-----wp------|
    # |---------------wt--------------|
    # |-----wa-------| |-------wb-----|
    
    if gap:
        gap_int, gap_str = 1, ' '
    else:
        gap_int, gap_str = 0, ''

    w_gap = 3 if (gap and align != 'center') else 1
    w_p = find_width(p)
    w_t = max(w_a + w_b + w_gap, w_p)
    
    if align == 'lower':
        x_p = (a_r + (w_a + w_gap + b_l)) // 2 - w_p // 2
    else:
        x_p = (a_l + (w_a + w_gap + b_r)) // 2 - w_p // 2
    p = padded_lines(p, x_p, 0)
    
    #        aaaaaaa        bbbbb
    # |-----ar-----|   |-bl-|
    # |---am----|      |--bm--|
    #           |-----z1------|
    #              |--z2----|
    
    if align == 'lower':
        l_line = (a_first[:a_r] + gap_str)
        r_line = (gap_str + b_first[b_l:])
        l_w = b_l + 1 + (w_a - a_r)
        line = l_line + uni_invt.center(l_w, uni_h) + r_line
        p.append(line)
        a, b = a_rest, b_rest
        
    elif align == 'center':
        l_w = b_m + (w_a - a_m) 
        line = (' ' * a_m) + uni_tl + uni_invt.center(l_w, uni_h) + uni_tr
        p.append(line)
        
    elif align == 'upper':
        l_line = (' ' * a_m + uni_tl).ljust(x_p, uni_h)
        r_line = uni_h * (w_a + w_gap + b_m - x_p - w_p) + uni_tr
        if gap:
            l_line = l_line[:-1] + ' '
            r_line = ' ' + r_line[1:]
        skip = len(l_line)
        p[-1] = l_line + p[-1][skip:skip + w_p] + r_line
    return join_horizontal(a, b, prefix=p, lwidth=w_a, gap=w_gap)