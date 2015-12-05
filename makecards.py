import os
import sys

FRONTS = {'white': 'white front.png',
          'black': 'black front.png'}
MARGIN = 111  # px, safe-bleed + actual margin (300dpi)
TEXT_WIDTH = 600  # px, 300dpi (card width - 2 * MARGIN)
FONT = 'HelveticaNeue-Bold.otf'
SIZE = 60


def CardAgainstHumanity(text, background_color, back, out):
  modified_text = text.replace("_", "_____")
  if modified_text[-1] != "." and modified_text[-1] != "!" and modified_text[-1] != "?":
    modified_text += "."
  print "Text: %s" % modified_text
  """Writes text onto back, result is in out. color is the background color."""
  text_color = 'white' if background_color == 'black' else 'black'
  text = text.replace('"', '\\"')
  command = ('convert -font %s -pointsize %d -size %dx '
             '-background %s -transparent %s -fill %s "caption:%s" temp.png' % (
                 FONT, SIZE, TEXT_WIDTH, background_color, background_color, text_color, modified_text.strip()))
  os.system(command)
  command = 'composite -geometry +%d+%d "%s" "%s" "%s"' % (
                MARGIN, MARGIN, 'temp.png', back, out)
  os.system(command)


def main():
  usage = 'Usage: %s <black|white> input.txt' % sys.argv[0]
  if len(sys.argv) != 3:
    print >> sys.stderr, usage
    return
  if sys.argv[1] not in ('white', 'black'):
    print >> sys.stderr, usage
    return
  background = sys.argv[1] + ' front.png'

  try:
    outdir = "C:\\Users\\Phil\\OneDrive\\CAH cards\\"
    os.mkdir(outdir)
  except OSError: pass

  print
  with file(sys.argv[2]) as f:
    for card_num, line in enumerate(f):
      outfile = '%s%03d.png' % (sys.argv[1], card_num)
      outfile = os.path.join(outdir, outfile)
      text = line.strip()
      if text.endswith('3'):
        background = sys.argv[1] + ' front pick3.png'
        text = text[:-1]
      elif text.endswith('2'):
        background = sys.argv[1] + ' front pick2.png'
        text = text[:-1]
      else:
        background = sys.argv[1] + ' front.png'
      print '\rCreating %s...' % outfile,
      sys.stdout.flush()
      CardAgainstHumanity(text, sys.argv[1], background, outfile)
      print '\rCreated %d cards!%s' % (card_num+1, ' '*30)

if __name__ == '__main__':
  main()
