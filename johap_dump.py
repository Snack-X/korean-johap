from PIL import Image
from struct import pack

im = Image.open("gulim16.bmp")
fp = open("gulim16.hex", "wb")

SIZE = 16

def dump_character(i, j):
  data = 0
  for y in range(SIZE):
    for x in range(SIZE):
      pixel = im.getpixel((i * SIZE + x, j * SIZE + y))

      data <<= 1
      if pixel == (0, 0, 0):
        data |= 1

    fp.write(pack(">H", data))
    data = 0

# cho
for j in range(8):
  for i in range(19):
    dump_character(i, j)

  print "#%d done" % (j+1)

print "chosung done"

#jung
for j in range(4):
  for i in range(21):
    dump_character(i, j + 9)

  print "#%d done" % (j+1)

print "jungsung done"

#jong
for j in range(4):
  for i in range(27):
    dump_character(i, j + 14)

  print "#%d done" % (j+1)

print "jungsung done"

im.close()
fp.close()
