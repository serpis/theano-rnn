import os
import random 
from PIL import Image

random.seed(1)

def rand():
    r = random.randint(0, 65535)
    return r

def pick_square((x, y, w, h), bw, bh):
    mod_w = w - bw
    mod_h = h - bh

    bx = rand() % (mod_w + 1)
    by = rand() % (mod_h + 1)

    return x+bx, y+by, bw, bh

def pick_20x20(box):
    return pick_square(box, 20, 20)
def pick_16x16(box):
    return pick_square(box, 16, 16)

orig_file = "gray_pigsah.png"
top = (0, 0, 640, 350)

def read_data(filename):
    im = Image.open(filename)
    pixels = list(im.getdata())
    pixels = [float(x)/255.0-0.5 for x in pixels]
    return pixels

def gen_ref16(i, b16):
    x, y, w, h = b16
    res_filename = "../out/test_%d_ref.png" % i
    cmd = "convert %s -crop %dx%d+%d+%d +repage -filter triangle %s" % (orig_file, w, h, x, y, res_filename)
    os.system(cmd)
    return read_data(res_filename)

def gen_ref44(i, b44):
    x, y, w, h = b44
    res_filename = "../out/test_%d_ref.png" % i
    cmd = "convert %s -crop %dx%d+%d+%d +repage -filter triangle %s" % (orig_file, w, h, x, y, res_filename)
    os.system(cmd)
    return read_data(res_filename)

def gen_downscaled(i, j, sb):
    x, y, w, h = sb
    res_filename = "../out/test_%d_down_%d.png" % (i, j)
    cmd = "convert %s -crop %dx%d+%d+%d +repage -filter triangle -resize 4x4 %s" % (orig_file, w, h, x, y, res_filename)
    os.system(cmd)
    return read_data(res_filename)

seq_inputs = []
seq_refs = []

for i in range(1000):
    b = pick_20x20(top)
    b16 = (b[0]+2, b[1]+2, b[2]-4, b[3]-4)
    #b44 = (b[0]+8, b[1]+8, b[2]-16, b[3]-16)
    rs = []
    rs.append(gen_ref16(i, b16))
    #rs.append(gen_ref44(i, b44))
    # duplicate first entry 7 more times, so 8 in total
    for j in range(15):
        rs.append(rs[0])
    seq_refs.append(rs)
    ds = []
    for j in range(16):
        sb = pick_16x16(b)
        ds.append(gen_downscaled(i, j, sb))
    seq_inputs.append(ds)

print "train_inputs  =", seq_inputs[0:800]
print "train_outputs =", seq_refs[0:800]

print "test_inputs  =", seq_inputs[800:1000]
print "test_outputs =", seq_refs[800:1000]
