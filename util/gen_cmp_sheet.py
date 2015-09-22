from PIL import Image
import sys

def read_file(filename):
    im = Image.open(filename)
    pixels = list(im.getdata())
    w, h = im.size
    return w, h, pixels

def write_file(filename, (w, h, data)):
    im = Image.new("L", (w, h))
    im.putdata(data)
    im.save(filename)

ref_files = sys.argv[1:]
out_files = [n.replace("ref", "out") for n in ref_files]

file_pairs = zip(ref_files, out_files)

is_first = True
tot_width = 0
tot_height = 0
entries_width, entries_height = [0 for i in range(2)]
res = []

for i, (ref_file, out_file) in enumerate(file_pairs):
    if is_first:
        w, h, data = read_file(ref_file)
        tot_width = (800/(w*2))*(w*2)
        entries_width = tot_width/(w*2)
        entries_height = (len(ref_files)+entries_width-1)/entries_width
        tot_height = entries_height * h

        res = [0 for j in range(tot_width*tot_height)]

        is_first = False

    for file_num, f in enumerate((ref_file, out_file)):
        w, h, data = read_file(f)
        entry_x = i % entries_width
        entry_y = i / entries_width
        for y in range(h):
            for x in range(w):
                from_x = x
                from_y = y

                to_x = entry_x*2*w + x
                if file_num == 1:
                    to_x += w
                to_y = entry_y*1*h + y

                res[to_x + to_y * tot_width] = data[x + w * y]

write_file("sheet.png", (tot_width, tot_height, res))

