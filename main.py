from kivy.config import Config

SIZE = 20 # Define length of grid's side.
Config.set('graphics', 'width',  (SIZE * 18) + 3)
Config.set('graphics', 'height', (SIZE * 18) + 33)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.properties import StringProperty

class MenuGrid(GridLayout):

    active = False  # Defines whether the game is running, or paused.
    start_pause = StringProperty('Start')
    clear_stop = StringProperty('Clear')
    clock = None

    def start_action(self):

        # If game is paused, run it, making an iteration every half a second.
        # Change the labels to Pause and Stop.

        if not self.active:
            for y in GameOfLifeApp.cells:
                for x in y:
                    x.disabled = True
            self.clock = Clock.schedule_interval(self.iteration, 0.5)
            self.active = True
            self.start_pause = 'Pause'
            self.clear_stop = 'Stop'

        # Else, unschedule the game and change the labels to Start and Clear.

        elif self.active:
            self.clock.cancel()
            for y in GameOfLifeApp.cells:
                for x in y:
                    x.disabled = False
            self.active = False
            self.start_pause = 'Start'
            self.clear_stop = 'Clear'

    def clear_action(self):

        # Stop the game if running, and change all instances to their normal
        # state and set them to False, so that they are not considered as
        # living cells in the next game.

        if self.active is False:
            for y in GameOfLifeApp.cells:
                for x in y:
                    x.state = 'normal'
                    x.phase = False
        elif self.active is True:
            self.start_action()
            for y in GameOfLifeApp.cells:
                for x in y:
                    x.state = 'normal'
                    x.phase = False

    def iteration(self, _dt):

        # Get the list of cells.
        # Create temporary list.

        cells = GameOfLifeApp.cells
        next_iteration = [[] for i in range(SIZE)]

        # For each cell, count its living neighbours by trying to access them
        # and checking their phase.

        neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                      (1, 0), (1, 1)]

        for y, row in enumerate(cells):
            for x, instance in enumerate(row):
                
                living_neighbours = 0
                for i in neighbours:
                    try:
                        new_y = y + i[0]
                        new_x = x + i[1]
                        if new_y >= 0 and new_x >= 0:
                            if cells[new_y][new_x].phase:
                                living_neighbours += 1
                    except IndexError:
                        pass
                    if living_neighbours == 4:
                        break

                # Apply the game's rules
                #  1: Any live cell with fewer than two live neighbours dies,
                #     as if caused by underpopulation.
                #  2: Any live cell with two or three live neighbours lives on
                #     to the next generation.
                #  3: Any live cell with more than three live neighbours dies,
                #     as if by overpopulation.
                #  4: Any dead cell with exactly three live neighbours becomes
                #     a live cell, as if by reproduction.

                if instance.phase:
                    if living_neighbours < 2:
                        next_iteration[y].append(False)
                    elif living_neighbours > 3:
                        next_iteration[y].append(False)
                    else:
                        next_iteration[y].append(True)
                else:
                    if living_neighbours == 3:
                        next_iteration[y].append(True)
                    else:
                        next_iteration[y].append(False)

        # Change the state of the buttons according to their phases or stop it
        # if no more living cells remain.

        if any(True in y for y in next_iteration):
            for y, row in enumerate(cells):
                for x, instance in enumerate(row):
                    instance.phase = next_iteration[y][x]
                    if next_iteration[y][x]:
                        instance.state = 'down'
                    else:
                        instance.state = 'normal'
        else:
            self.clear_action()


class CustomButton(ToggleButton):

    # Class for cells. Phase is False by default.
    # The phase tells the program if the cell is alive or dead.
    # Store them in a list.

    def __init__(self, y, x, **kwargs):
        self.phase = False
        GameOfLifeApp.cells[y].append(self)
        super().__init__(**kwargs)


class GameOfLifeApp(App):

    cells = [[] for i in range(SIZE)]

    def change_phase(self, instance):

        # If a cell is clicked, flip the phase.

        instance.phase = not instance.phase

    # Build the game
    # Create a grid, and assign a button to each cell.
    # Bind the button to the change_phase() function

    def build(self):

        layout_base = GridLayout(cols=1, row_force_default=True,
                                 row_default_height=30)
        layout_base.add_widget(MenuGrid())
        layout = GridLayout(cols=SIZE, spacing=3, padding=3)

        for y in range(SIZE):
            for x in range(SIZE):
                button = CustomButton(y, x, size_hint=[None, None],
                                      width=15, height=15)
                button.bind(on_press=self.change_phase)
                layout.add_widget(button)

        layout_base.add_widget(layout)

        return layout_base


# Run the game

if __name__ == '__main__':
    GameOfLifeApp().run()
