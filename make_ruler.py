#!/usr/bin/python

from fpdf import FPDF

import math
import os

from fraction_utils import simplify_float


import pint
ureg = pint.UnitRegistry()

from base_ruler_maker import BaseRulerMaker

import argparse
parser = argparse.ArgumentParser(description='Make a ruler for laser cutting')
parser.add_argument('-H', '--height', type=float, help='height of ruler units', dest='height', required=True)
parser.add_argument('-w', '--width', type=int, help='width of ruler in units', dest='width', required=True)
parser.add_argument('-u', '--unit', '--units', choices=['inches', 'in', 'centimeters', 'cm'], dest='unit', default='in')
args = parser.parse_args()

unit = 'in'
if args.unit in ['cm', 'centimeters']:
  unit = 'cm'



class RulerMaker(BaseRulerMaker):
  def __init__(self, pdf):
    super(RulerMaker, self).__init__(pdf, unit)
    self.pdf.add_font('Arial', '', 'Arial.ttf', uni=True)
    self.pdf.set_font('Arial')
    self.pdf.set_font_size((args.height * ureg.parse_expression(unit)).to('point').magnitude / 3.5)

  def draw_side_ticks(self, width, height):
    if unit == 'cm':
      side_tick_length = 2.5
    elif unit == 'in':
      side_tick_length = 0.25

    self.set_engrave_line()
    # left side, thirds
    slices = 3
    for fraction in range(1, slices):
      y = height * fraction / slices
      # first draw lines on the side
      self.pdf.line(0, y, side_tick_length, y)

    # right side, quarters
    slices = 4
    for fraction in range(1, slices):
      y = height * fraction / slices
      # first draw lines on the side
      self.pdf.line(width-side_tick_length, y, width, y)

  def draw_ticks(self, width, height):
    if unit == 'in':
      sliceDiv = 0.125
    elif unit == 'cm':
      sliceDiv = 1

    slices = int(width / sliceDiv)

    maxHeight = height * 0.25

    for slice in range(1, slices):
      if unit == 'cm':
        if slice % 10 == 0:
          lineHeight = maxHeight  
        else: 
          lineHeight = maxHeight * 0.7
      elif unit == 'in':
        if slice % 8 == 0:
          lineHeight = maxHeight
        elif slice % 4 == 0:
          lineHeight = maxHeight * 0.7
        elif slice % 2 == 0:
          lineHeight = maxHeight * 0.5
        else:
          lineHeight = maxHeight * 0.4

      if lineHeight == maxHeight:
        self.set_thick_engrave_line()
      else:
        self.set_engrave_line()

      x = slice * sliceDiv
      self.pdf.line(x, 0, x, lineHeight) # math.fabs(y_factor - height))
      self.pdf.line(x, height, x, height - lineHeight) # math.fabs(y_factor - height))
    
  def draw_basic_template(self, width, height, unit):
    print(height)
    print(width)
    self.pdf.add_page(orientation='L', format=(height, int(math.ceil(width))))

    self.set_cut_line()
    self.pdf.rect(0, 0, width, height)
    self.draw_string_in_middle(height=height, width=width, string=f'{simplify_float(height)}{unit} x {simplify_float(width)}{unit}')
    self.draw_side_ticks(height=height, width=width)
    self.draw_ticks(height=height, width=width)

def make_ruler():    
  pdf = FPDF(orientation = 'L', unit = unit)
  ruler_maker = RulerMaker(pdf)
  ruler_maker.draw_basic_template(width=args.width, height=args.height, unit=' ' + args.unit)
  pdf.output('ruler-%s-x-%s-%s.pdf' % (args.height, args.width, args.unit))

if __name__ == '__main__':
  make_ruler()