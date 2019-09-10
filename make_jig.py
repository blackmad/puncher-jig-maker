#!/usr/bin/python

from fpdf import FPDF
import math
import pint
import os
from fraction_utils import simplify_float


ureg = pint.UnitRegistry()

FiveMM = (5 * ureg.mm).to('inch').magnitude
FirstHoleAt = 0.5
HoleInterval = 0.25

from base_ruler_maker import BaseRulerMaker

class PuncherMaker(BaseRulerMaker):
  def __init__(self, pdf):
    super(PuncherMaker, self).__init__(pdf, 'inch')
    self.pdf.add_font('Arial', '', 'fonts/Arial.ttf', uni=True)
    self.pdf.set_font('Arial')

  # this sets up the cut line, side lines and top/bottom rulers
  def draw_basic_template(self, width, height, bold):
    self.pdf.add_page(orientation='L', format=(height, width))

    self.set_cut_line()
    self.pdf.rect(0, 0, width, height)

    self.draw_ruler(width, height, margin=0, invert=False, bold=bold)
    self.draw_ruler(width, height, margin=FirstHoleAt, invert=True, bold=bold)

  def make_belt_jig(self, height, ignore):
    BeltHoleWidth = 0.5
    width = FirstHoleAt + 2 + FirstHoleAt
    self.draw_basic_template(width, height, bold=False)
    self.set_cut_line()
    self.draw_circle_at_center(FirstHoleAt, height/2, FiveMM)
    self.draw_circle_at_center(width - FirstHoleAt, height/2, FiveMM)

    self.draw_circle_at_center(width/2, height/2, FiveMM)
    self.draw_circle_at_center(width/2 - BeltHoleWidth/2, height/2, FiveMM)
    self.draw_circle_at_center(width/2 + BeltHoleWidth/2, height/2, FiveMM)
    self.set_cut_line()
    self.pdf.rect(width/2 - BeltHoleWidth/2, height/2 - FiveMM/2, BeltHoleWidth, FiveMM)

  def make_jig(self, height, width):
    self.draw_basic_template(width, height, bold=True)

    right_slices = 2
    if (height/3 > FiveMM):
      right_slices = 3
    self.draw_at_slice_right(slices=right_slices, width=width, height=height)

    left_slices = 2
    if (height/4 > FiveMM):
      left_slices = 4
    elif (height/3 > FiveMM) and right_slices != 3:
      left_slices = 3
    self.draw_at_slice_left(slices=left_slices, width=width, height=height)

    size_str = f'{simplify_float(height)}"'
    if (height > 1):
      size_str = ' ' + size_str
    self.draw_string_in_middle(height=height, width=width, string=size_str)

  def draw_ruler(self, width, height, margin = 0, invert=False, bold=False):
    y_start = 0
    y_factor = 0
    if invert:
      y_start = height
      y_factor = height

    x = 0
    x_offset = 0
    x_start = margin
    MaxHeight = 0.1

    # this is to mark special the 1st and 7th holes to emphasize a 2" spacing
    # I like this for most rivets/widths and also it's nice because it means the middle
    # hole is the 4th hole
    special_offset_slice = int(2 / HoleInterval)
    if margin == 0:
      slices = int(width / HoleInterval) + 2
      first_special_slice = int(FirstHoleAt/HoleInterval)
      SpecialSlices = [first_special_slice, first_special_slice + special_offset_slice,
        slices - 2 - first_special_slice, slices - 2 - first_special_slice - special_offset_slice]
    else:
      slices = int((width - margin) / HoleInterval)
      SpecialSlices = [0, special_offset_slice, slices - 2, slices - 10]

    for slice in range(0, slices - 1):
      # this calculates big on 1 inches, medium on 1/2, small on 1/4
      mod = ((x_offset - int(x_offset)) / 0.25) * 0.25
      height = 0
      if (mod == 0):
        height = MaxHeight
      elif (mod == 0.5):
        height = MaxHeight * 0.7
      else:
        height = MaxHeight * 0.4

      # if it's at zero or 1.75, which are intervals I like, make it bold
      if (bold and (slice in SpecialSlices)):
        self.set_thick_engrave_line()
      else:
        self.set_engrave_line()

      x = x_start + x_offset
      self.pdf.line(x, y_start, x, math.fabs(y_factor - height))
      x_offset += HoleInterval


  def draw_at_slice_left(self, slices, width, height):
    for fraction in range(1, slices):
      y = height * fraction / slices
      spacing = 0.25
      # first draw lines on the side
      self.set_engrave_line()
      self.pdf.line(0, y, 0.25, y)

      # now draw circlesg
      self.make_circles_at(x=FirstHoleAt, y=y, size=FiveMM, spacing=spacing, num=int(((width / 2) - FirstHoleAt)/spacing))

  def draw_at_slice_right(self, slices, width, height):
    for fraction in range(1, slices):
      y = height * fraction / slices
      spacing = -0.25
      # first draw lines on the side
      self.set_engrave_line()
      self.pdf.line(width-0.25, y, width, y)

      # now draw circles
      self.make_circles_at(x=width - FirstHoleAt, y=y, size=FiveMM, spacing=spacing, num=int(((width / 2) - FirstHoleAt)/math.fabs(spacing)))


  def draw_circle_at_center(self, x, y, size):
    #self.pdf.ellipse(x + size/2, y - size/2, size, size)
    self.pdf.ellipse(x - (size / 2), y - (size / 2), size, size)

  def make_circles_at(self, x, y, size, spacing, num):
    self.set_cut_line()
    self.pdf.set_draw_color(255, 0, 0)
    for i in range(0, num):
      self.draw_circle_at_center(x, y, size)
      x += spacing


def make_jig_helper(cbname, filename):
  # make 6" hole jigs
  pdf = FPDF(orientation = 'L', unit = 'in')
  maker1 = PuncherMaker(pdf)

  size = initial_size = 0.25
  interval = 0.125
  max_size = 2
  while (size < max_size):
    # add this to the grouped pdf
    cb1 = getattr(maker1, cbname)
    cb1(size, 6)

    # output an individual pdf for this
    pdf2 = FPDF(orientation = 'L', unit = 'in')
    maker2 = PuncherMaker(pdf2)
    cb2 = getattr(maker2, cbname)
    cb2(size, 6)
    pdf2.output('%s_%s' % (size, filename))

    size += interval

  pdf.output(filename)

def make_belt_jigs():
  if not os.path.isdir('output'):
    os.mkdir('output')
  make_jig_helper('make_belt_jig', 'belt_jigs.pdf')
  make_jig_helper('make_jig', 'rivet_jigs.pdf')

if __name__ == '__main__':
  make_belt_jigs()
