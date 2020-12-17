import arcade
from solver.state import State

class Window(arcade.Window):
  def __init__(self, width, height):
    super().__init__(width, height, "8 puzzel solver")
    self.width = width
    self.height = height

  def setup(self):
    arcade.set_background_color(arcade.color.WHITE)

    self.state = State(self.width, self.height)
    self.state.solve()

    arcade.run()
    pass

  def on_draw(self):
    arcade.start_render()
    self.state.render()
    pass

  def update(self, delta_time):
    self.state.update(delta_time)
    pass