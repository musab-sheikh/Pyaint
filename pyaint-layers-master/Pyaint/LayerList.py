from utils.button import Button
from utils.settings import *
from Pyaint.Layer import Layer
from copy import deepcopy

x_val = HEIGHT - 2 * 40

empty_grid = [[BG_COLOR] * COLS for _ in range(ROWS)]


class LayerList:
    def __init__(self):
        self.layers = []
        self.current = None
        self.selected_layers = []
        self.main_grid = None

    # getters and setters
    def get_main_grid(self):
        return self.main_grid

    def addLayer(self, buttons):
        # max no. of layers that can be added are 9
        # if that limit is exceeded than it should not add any more layers
        if len(self.layers) < 9:
            # if the layer being inserted is the first layer
            if len(self.layers) == 0:
                # set layer id to 1
                layer_id = 1
                # set the y coordinate to 40 beginning from the top
                y_val = 40
            else:
                # else get the last layer's id and increment to generate a new id
                layer_id = self.layers[len(self.layers) - 1].id + 1
                # set the y_coordinate to be the last layer's button coordinate + the button height
                y_val = self.layers[-1].layer_button.y + self.layers[-1].layer_button.height

            # create the new layer to be inserted
            new_layer = Layer(HEIGHT - 2 * 40, y_val, layer_id)

            # append the layer into the layer list
            self.layers.append(new_layer)

            # append the button for the layer so, it can be rendered
            buttons.append(new_layer.layer_button)
            buttons.append(new_layer.selection_button)

            # any new layer that is inserted will automatically be the currently selected layer
            self.select_layer(new_layer.id)

            # set the current layer
            self.current = new_layer

            # set the main grid to be the current layers grid
            self.main_grid = self.current.visible_grid

    def select_layer(self, layer_id):
        # change color of previously selected layer if it exists
        if self.current is not None:
            # color of the previously selected layer
            self.current.layer_button.color = WHITE

        # find the layer with the given layer id
        for layer in self.layers:
            # if the layer is found
            if layer.id == int(layer_id):
                # set it as the current layer
                self.current = layer
                # change background color of the layer's button to be LIME
                self.current.layer_button.color = LIME
                # end for loop
                break

    # method for deleting a layer
    # param: buttons list from the main file
    # layer needs to be selected so, it can be deleted
    def deleteLayer(self, buttons):
        # do not delete if the list has only 1 layer remaining since
        # minimum no. of layers should be 1
        if len(self.layers) < 2:
            return

        if len(self.selected_layers) == len(self.layers):
            return

        for layer in self.selected_layers:
            # delete the layer from the list
            self.layers.remove(layer)

            # delete its corresponding button
            buttons.remove(layer.layer_button)
            buttons.remove(layer.selection_button)

            # adjust placement of all layers (x, y) coordinates
            for i in range(len(self.layers)):
                self.layers[i].layer_button.y = 40 * i + 40
                self.layers[i].selection_button.y = 40 * i + 50

        # select the previous layer that is in the list
        if len(self.layers) > 0:
            self.select_layer(self.layers[len(self.layers) - 1].id)

        # clear selected list
        self.clear_selection()

    # method to delete a layer given its id
    def delete_layer_by_id(self, buttons, layer_id):
        # do not delete if the list has only 1 layer remaining since
        # minimum no. of layers should be 1
        if len(self.layers) < 2:
            return

        for layer in self.layers:
            if layer.id == layer_id:
                self.layers.remove(layer)
                buttons.remove(layer.layer_button)
                buttons.remove(layer.selection_button)
                break

        # adjust placement of all layers (x, y) coordinates
        for i in range(len(self.layers)):
            self.layers[i].layer_button.y = 40 * i + 40
            self.layers[i].selection_button.y = 40 * i + 50

        # select the previous layer that is in the list
        if len(self.layers) > 0:
            self.select_layer(self.layers[len(self.layers) - 1].id)

    # select multiple layers:
    def select_multiple_layers(self, layer_id):
        # find the layer with the given layer id
        for layer in self.layers:
            # if the layer is found
            if layer.id == int(layer_id):
                # if already selected unselect it
                if layer.selection_button.color == BLACK:
                    # remove from selected layers
                    self.selected_layers.remove(layer)
                    # change bg color of button
                    layer.selection_button.color = WHITE
                    break
                else:
                    # add layer into selected layers list
                    self.selected_layers.append(layer)
                    # change background color of the layer's button to be LIME
                    layer.selection_button.color = BLACK
                    # end for loop
                    break

    # method to clear all selected layers
    def clear_selection(self):

        # remove all selected layers from the list
        self.selected_layers.clear()

        # loop through the layers list
        for layer in self.layers:
            # if the list is selected - button is black
            if layer.selection_button.color == BLACK:
                # unselect it
                layer.selection_button.color = WHITE

    # show all layers in layers list
    def show_layers(self):

        # show all layers on the screen giving priority to the top list
        self.main_grid = deepcopy(self.layers[0].visible_grid)

        # for every row and col
        for row in range(ROWS):
            for col in range(COLS):

                # for every layer in layers list
                for layer in self.layers:
                    # if the layer cell is not empty
                    if layer.visible_grid[row][col] != BG_COLOR:
                        # add that spot to combined layer grid
                        self.main_grid[row][col] = layer.visible_grid[row][col]
                        # break so it does not override
                        break

    # merge all layers in selected layer list
    def merge_layers(self, buttons):
        # do not merge if not more than 1 layer selected
        if len(self.selected_layers) < 2:
            return

        new_grid = deepcopy(self.selected_layers[len(self.selected_layers) - 1].visible_grid)
        # combine layers into same grid
        for i in range(ROWS):
            for j in range(COLS):

                # for every layer in the selected layers combine them into a single grid
                for layer in self.selected_layers:
                    if layer.visible_grid[i][j] != BG_COLOR:
                        new_grid[i][j] = layer.visible_grid[i][j]
                        break

        # get the id of the 1st selected layer
        stay_id = self.selected_layers[0].id

        # delete all layers in selected layers except 1
        for layer in self.selected_layers:
            if stay_id != layer.id:
                self.delete_layer_by_id(buttons, layer.id)

        # find the layer with that id and set it's grid as combined grid
        for layer in self.layers:
            if layer.id == stay_id:
                layer.visible_grid = new_grid
                # set the current layer that was generated after merged
                self.current = layer
                break

        # clear all selections of layers that were selected
        self.clear_selection()

    def toggle_visible(self):

        # check if already invisible
        if self.current.visible_grid == empty_grid:
            # toggle visibility to on
            self.current.visible_grid = self.current.grid
        else:
            # save the original grid to grid variable
            self.current.grid = self.current.visible_grid
            # set grid to bg color
            self.current.visible_grid = empty_grid

    def on_hover_effect(self, buttons):
        mouse_pos = pygame.mouse.get_pos()
        # all button types related to layers
        button_types = ['add_layer', 'delete_layer', 'merge_layer', 'toggle_visibility',
                        'move_up', 'move_down', 'erase_btn', 'clear_btn']

        # for every button in buttons check if button is in button types
        # if button is hovered change it's color or else change back to original
        for button in buttons:
            if button.name in button_types:
                if button.hover(mouse_pos):
                    button.color = BLACK
                    button.text_color = WHITE
                else:
                    button.color = WHITE
                    button.text_color = BLACK

    # moves the currently selected layer up
    def move_layer_up(self):
        # get the current layer's index
        try:
            layer_index = self.layers.index(self.current)

            # if it's the top layer, cannot be moved up
            if layer_index == 0:
                return

            # get the layer above current layer
            upper_layer = self.layers[layer_index - 1]

            x1, y1 = self.current.layer_button.x, self.current.layer_button.y

            x2, y2 = self.current.selection_button.x, self.current.selection_button.y

            # swap button coordinates
            self.current.layer_button.x = upper_layer.layer_button.x
            self.current.layer_button.y = upper_layer.layer_button.y

            # swap toggle button coordinates
            self.current.selection_button.x = upper_layer.selection_button.x
            self.current.selection_button.y = upper_layer.selection_button.y

            # set the layer to previous index
            self.layers[layer_index - 1] = self.current

            upper_layer.layer_button.x, upper_layer.layer_button.y = x1, y1

            upper_layer.selection_button.x, upper_layer.selection_button.y = x2, y2

            # set the upper layer to bottom
            self.layers[layer_index] = upper_layer


        except ValueError:
            print('current layer is None')

    def move_layer_down(self):
        # get the current layer's index
        try:
            layer_index = self.layers.index(self.current)

            # if it's the top layer, cannot be moved up
            if layer_index == len(self.layers) - 1:
                return

            # get the layer above current layer
            upper_layer = self.layers[layer_index + 1]

            x1, y1 = self.current.layer_button.x, self.current.layer_button.y

            x2, y2 = self.current.selection_button.x, self.current.selection_button.y

            # swap button coordinates
            self.current.layer_button.x = upper_layer.layer_button.x
            self.current.layer_button.y = upper_layer.layer_button.y

            # swap toggle button coordinates
            self.current.selection_button.x = upper_layer.selection_button.x
            self.current.selection_button.y = upper_layer.selection_button.y

            # set the layer to previous index
            self.layers[layer_index + 1] = self.current

            upper_layer.layer_button.x, upper_layer.layer_button.y = x1, y1

            upper_layer.selection_button.x, upper_layer.selection_button.y = x2, y2

            # set the upper layer to bottom
            self.layers[layer_index] = upper_layer


        except ValueError:
            print('current layer is None')
