from kivy.config import Config
Config.set('graphics', 'width',  903)
Config.set('graphics', 'height', 933)
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

        # If game is paused, run it, making an iteration every half a second
        # Change the labels to Pause and Stop

        if self.active is False:
            for instance in CustomButton.cells:
                instance.disabled = True
            self.clock = Clock.schedule_interval(iteration, 0.5)
            self.active = True
            self.start_pause = 'Pause'
            self.clear_stop = 'Stop'

        # Else, unschedule the game and change the labels to Start and Clear

        elif self.active is True:
            self.clock.cancel()
            for instance in CustomButton.cells:
                instance.disabled = False
            self.active = False
            self.start_pause = 'Start'
            self.clear_stop = 'Clear'

    def clear_action(self):

        # Stop the game if running, and change all instances to their normal
        # state and set them to False, so that they are not considered as
        # living cells in the next game.

        if self.active is False:
            for instance in CustomButton.cells:
                instance.state = 'normal'
                instance.phase = False
        elif self.active is True:
            self.start_action()
            for instance in CustomButton.cells:
                instance.state = 'normal'
                instance.phase = False


class CustomButton(ToggleButton):

    # Class for cells. Give them an id and a False phase.
    # The phase tells the program if the cell is alive or dead.
    # Store them in a list

    cells = []

    def __init__(self, index, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.id = str(index)
        self.phase = False
        CustomButton.cells.append(self)

    def __str__(self):
        return 'Index: {}'.format(self.id)

    def __int__(self):
        return int(self.id)


def iteration(dt):

    # Get the list of cells.
    # Create temporary list

    cells = CustomButton.cells
    next_iteration = []

    # For each cell, count its living neighbours by trying to access them and
    # checking their phase

    for i, instance in enumerate(cells):

        neighbours = [-51, -50, -49, -1, 1, 49, 50, 51]
        living_neighbours = 0

        for x in neighbours:
            try:
                if cells[i + x].phase is True:
                    living_neighbours += 1
            except IndexError:
                pass
            if living_neighbours == 4:
                break

        # Apply the game's rules
        #  1: Any live cell with fewer than two live neighbours dies,
        #     as if caused by underpopulation.
        #  2: Any live cell with two or three live neighbours lives on to
        #     the next generation.
        #  3: Any live cell with more than three live neighbours dies,
        #     as if by overpopulation.
        #  4: Any dead cell with exactly three live neighbours becomes a
        #     live cell, as if by reproduction.

        if instance.phase is True:
            if living_neighbours < 2:
                next_iteration.append(False)
            elif living_neighbours > 3:
                next_iteration.append(False)
            else:
                next_iteration.append(True)
        else:
            if living_neighbours == 3:
                next_iteration.append(True)
            else:
                next_iteration.append(False)

    # Change the state of the buttons according to their phases

    for i, instance in enumerate(cells):
        instance.phase = next_iteration[i]
        if next_iteration[i] is True:
            instance.state = 'down'
        else:
            instance.state = 'normal'


def change_phase(instance):

    # If a cell is clicked, turn it to its opposite phase.
    # True - False
    # Alive - Dead

    if instance.phase is True:
        instance.phase = False
    else:
        instance.phase = True


class GameOfLifeApp(App):

    # Build the game
    # Create a 50x50 grid, and assign a button to each cell.
    # Bind the button to the change_phase() function

    def build(self):

        layout_base = GridLayout(cols=1, row_force_default=True,
                                 row_default_height=30)
        layout_base.add_widget(MenuGrid())

        layout = GridLayout(cols=50, spacing=3, padding=3)
        for i in range(0, 2500):
            button = CustomButton(i, size_hint=[None, None], width=15,
                                  height=15)
            button.bind(on_press=change_phase)
            layout.add_widget(button)

        layout_base.add_widget(layout)

        return layout_base


# Run the game

if __name__ == '__main__':
    GameOfLifeApp().run()
