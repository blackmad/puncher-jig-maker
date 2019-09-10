import pint
ureg = pint.UnitRegistry()

class BaseRulerMaker:
  def __init__(self, pdf, unit):
    self.pdf = pdf
    self.unit = unit

  def set_cut_line(self):
    self.pdf.set_line_width((0.001 * ureg.point).to(self.unit).magnitude)
    self.pdf.set_draw_color(255, 0, 0)

  def set_engrave_line(self):
    self.pdf.set_line_width((1 * ureg.point).to(self.unit).magnitude)
    self.pdf.set_draw_color(0, 0, 0)

  def set_thick_engrave_line(self):
    self.pdf.set_line_width((2 * ureg.point).to(self.unit).magnitude)
    self.pdf.set_draw_color(0, 0, 0)

  def draw_string_in_middle(self, height, width, string):
    string_width = self.pdf.get_string_width(string, normalized=True)
    string_height = self.pdf.get_string_width('M')*0.8 #1 em (nominally, the height of the font)
    # if (len(size_str) > 2): # or height > 1:
      # string_width = 0
    # print((width/2 - string_width/2, height/2 + string_height/2, size_str))
    self.pdf.text(width/2 - string_width/2, height/2 + string_height/2, string)