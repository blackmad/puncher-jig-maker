#!/usr/bin/python

from fpdf import FPDF
import math
import pint

ureg = pint.UnitRegistry()

FiveMM = (5 * ureg.mm).to('inch').magnitude
FirstHoleAt = 0.5
HoleInterval = 0.25

import unicodedata

def simplify_float(number):
    vf = "VULGAR FRACTION "
    vulgars = {0.125 : unicodedata.lookup(vf + "ONE EIGHTH"),
               0.2   : unicodedata.lookup(vf + "ONE FIFTH"),
               0.25  : unicodedata.lookup(vf + "ONE QUARTER"),
               0.375 : unicodedata.lookup(vf + "THREE EIGHTHS"),
               0.4   : unicodedata.lookup(vf + "TWO FIFTHS"),
               0.5   : unicodedata.lookup(vf + "ONE HALF"),
               0.6   : unicodedata.lookup(vf + "THREE FIFTHS"),
               0.625 : unicodedata.lookup(vf + "FIVE EIGHTHS"),
               0.75  : unicodedata.lookup(vf + "THREE QUARTERS"),
               0.8   : unicodedata.lookup(vf + "FOUR FIFTHS"),
               0.875 : unicodedata.lookup(vf + "SEVEN EIGHTHS")}

    decimal = int(number)
    if number == decimal:
        return str(decimal)

    vulgar = vulgars.get(number - decimal)
    if vulgar:
        if decimal == 0:
            return vulgar
        return "%d%s" % (decimal, vulgar)
    return "%.1f" % number

class PuncherMaker():
  def __init__(self, pdf):
    self.pdf = pdf

  # this sets up the cut line, side lines and top/bottom rulers
  def draw_basic_template(self, width, height, bold):
    self.pdf.add_page(orientation='L', format=(height, width))

    self.set_cut_line()
    self.pdf.rect(0, 0, width, height)

    self.draw_ruler(width, height, margin=0, invert=False, bold=bold)
    self.draw_ruler(width, height, margin=FirstHoleAt, invert=True, bold=bold)

  def make_belt_jig(self, height):
    BeltHoleWidth = 0.5
    width = FirstHoleAt + 2 + FirstHoleAt
    self.draw_basic_template(width, height, bold=False)
    self.set_cut_line()
    self.draw_circle_at_center(FirstHoleAt, height/2, FiveMM)
    self.draw_circle_at_center(width - FirstHoleAt, height/2, FiveMM)

    #self.draw_circle_at_center(width/2, height/2, FiveMM)
    #self.draw_circle_at_center(width/2 - BeltHoleWidth/2, height/2, FiveMM)
    #self.draw_circle_at_center(width/2 + BeltHoleWidth/2, height/2, FiveMM)
    self.pdf.set_line_width((0.001 * ureg.point).to('inch').magnitude)
    self.pdf.rect(width/2 - BeltHoleWidth/2, height/2 - FiveMM/2, BeltHoleWidth, FiveMM)

  def make(self, width, height):
    self.draw_basic_template(width, height, bold=True)

    if (height/3 > FiveMM):
      self.draw_at_slice_right(slices=3, width=width, height=height)
    else:
      self.draw_at_slice_right(slices=2, width=width, height=height)

    if (height/4 > FiveMM):
      self.draw_at_slice_left(slices=4, width=width, height=height)
    elif (height/3 > FiveMM):
      self.draw_at_slice_left(slices=3, width=width, height=height)
    else:
      self.draw_at_slice_left(slices=2, width=width, height=height)

    size_str = simplify_float(height) + '"'
    self.pdf.set_font('Arial', 'B', 14)
    string_width = self.pdf.get_string_width(size_str)
    string_height = self.pdf.get_string_width('M')*0.8 #1 em (nominally, the height of the font)
    if (len(size_str) > 2) or size > 1:
      string_width = 0
    self.pdf.text(width/2 - string_width/2, height/2 + string_height/2, size_str)

  def set_cut_line(self):
    self.pdf.set_line_width((0.001 * ureg.point).to('inch').magnitude)
    self.pdf.set_draw_color(255, 0, 0)

  def set_engrave_line(self):
    self.pdf.set_line_width((1 * ureg.point).to('inch').magnitude)
    self.pdf.set_draw_color(0, 0, 0)

  def set_thick_engrave_line(self):
    self.pdf.set_line_width((2 * ureg.point).to('inch').magnitude)
    self.pdf.set_draw_color(0, 0, 0)


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

      # now draw circles
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
    self.pdf.set_draw_color(255, 0, 0)
    for i in range(0, num):
      self.draw_circle_at_center(x, y, size)
      x += spacing


def make_jigs():
  # make 6" hole jigs
  pdf = FPDF(orientation = 'L', unit = 'in')
  maker = PuncherMaker(pdf)

  size = initial_size = 0.25
  interval = 0.25
  max_size = 2
  while (size < max_size):
    size += interval
    maker.make(6, size)

  pdf.output('rivet_jigs.pdf')

if __name__ == '__main__':
    # make ?" belt jigs
    pdf = FPDF(orientation = 'L', unit = 'in')
    maker = PuncherMaker(pdf)

    size = initial_size = 0.25
    interval = 0.25
    max_size = 2
    while (size < max_size):
      size += interval
      maker.make_belt_jig(size)

    pdf.output('belt_loop_jigs.pdf')