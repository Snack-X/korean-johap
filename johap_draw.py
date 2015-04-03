import binascii, sys

fp = open("gulim16.hex", "rb")

CHO_IDX = 0
JUNG_IDX = CHO_IDX + 32 * 19 * 8 # 32 bytes per character, 19 characters per set, 8 sets
JONG_IDX = JUNG_IDX + 32 * 21 * 4 # 32 bytes per character, 21 characters per set, 4 sets

CHO_MAP = [0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1, 2, 4, 4, 4, 2, 1, 3, 0]
JONG_MAP = [0, 2, 0, 2, 1, 2, 1, 2, 3, 0, 2, 1, 3, 3, 1, 2, 1, 3, 3, 1, 1]

def mask_32byte(out, pos):
  fp.seek(pos)
  dat = fp.read(32)

  idx = 0
  for i in dat:
    n = ord(i)

    for j in range(8)[::-1]:
      bit = n >> j & 1

      if bit == 1:
        out[idx] = 1

      idx += 1

  return out

def draw_korean(cho, jung, jong):
  CHO_TYPE = -1
  JUNG_TYPE = -1
  JONG_TYPE = -1

  CHO_TYPE = CHO_MAP[jung]

  if jong != 0:
    if   CHO_TYPE == 0: CHO_TYPE = 5
    elif CHO_TYPE == 1: CHO_TYPE = 6
    elif CHO_TYPE == 2: CHO_TYPE = 6
    elif CHO_TYPE == 3: CHO_TYPE = 7
    elif CHO_TYPE == 4: CHO_TYPE = 7

  JUNG_TYPE = 0 if cho in (0, 16) else 1
  JUNG_TYPE += 2 if jong != 0 else 0

  JONG_TYPE = JONG_MAP[jung]

  out = [0] * 256

  out = mask_32byte(out, CHO_IDX + (32 * 19 * CHO_TYPE) + (32 * cho))

  out = mask_32byte(out, JUNG_IDX + (32 * 21 * JUNG_TYPE) + (32 * jung))

  if jong != 0:
    out = mask_32byte(out, JONG_IDX + (32 * 27 * JONG_TYPE) + (32 * (jong - 1)))

  count = 0
  for i in out:
    count += 1

    if i == 1:
      sys.stdout.write(" *")
    else:
      sys.stdout.write("  ")

    if count % 16 == 0:
      sys.stdout.write("\n")

cho = 0
jung = 0
jong = 1
print unichr(0xac00 + (cho * 21 * 28) + (jung * 28) + jong)
draw_korean(cho, jung, jong)
