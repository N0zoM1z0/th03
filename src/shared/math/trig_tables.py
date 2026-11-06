"""master.lib public-domain tables, A. Koizuka (1992), from their documented formulas.

Angles use256 steps per turn. Sine values use signed8.8 scale; cosine shares
the sine storage beginning64 angles later. These emit DATA, never instructions.
No target, object, reference source, or native output is an input.
"""
import math


def values():
    return ([round(math.atan(i / 256) * 128 / math.pi) for i in range(256)],
            [round(math.sin(i * math.tau / 256) * 256) for i in range(320)])


def generate():
    atan, sine = values()
    a = ['; public domain: A. Koizuka; atan(n/256)*128/pi, nearest integer.',
         'public AtanTable8,_AtanTable8', '_AtanTable8 label byte', 'AtanTable8 label byte']
    a += ['db ' + ','.join(map(str, atan[i:i+16])) for i in range(0, 256, 16)]
    s = ['; public domain: A. Koizuka; sin(2*pi*n/256)*256, nearest integer.',
         'public _SinTable8,_CosTable8', '_SinTable8 label word']
    for i in range(0, 320, 8):
        if i == 64:
            s.append('_CosTable8 label word')
        s.append('dw ' + ','.join(map(str, sine[i:i+8])))
    return {'generated/atan.inl': ('\n'.join(a)+'\n').encode(),
            'generated/sine.inl': ('\n'.join(s)+'\n').encode()}
