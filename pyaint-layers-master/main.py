import pygame

from utils import *
from Pyaint.LayerList import LayerList

WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Pyaint")
STATE = "COLOR"
Change = False


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw_mouse_position_text(win):
    pos = pygame.mouse.get_pos()
    pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
    try:
        row, col = get_row_col_from_pos(pos)
        text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
        win.blit(text_surface, (5, HEIGHT - TOOLBAR_HEIGHT))
    except IndexError:
        for button in buttons:
            if not button.hover(pos):
                continue
            if button.text == "Clear":
                text_surface = pos_font.render("Clear Everything", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Erase":
                text_surface = pos_font.render("Erase", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "FillBucket":
                text_surface = pos_font.render("Fill Bucket", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Brush":
                text_surface = pos_font.render("Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Change":
                text_surface = pos_font.render("Swap Toolbar", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            r, g, b = button.color
            text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1,
                                           BLACK)

            win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))

        for button in brush_widths:
            if not button.hover(pos):
                continue
            if button.width == size_small:
                text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_medium:
                text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_large:
                text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break


def draw_grid_lines(win):
    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw_layer_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    draw_grid_lines(win)

    draw_brush_widths(win)
    draw_mouse_position_text(win)


def draw_brush_widths(win):
    brush_widths = [
        Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, None,
               "ellipse"),
        Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, None,
               "ellipse"),
        Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, None,
               "ellipse")
    ]
    for button in brush_widths:
        button.draw(win)
        # Set border colour
        border_color = BLACK
        if button.color == BLACK:
            border_color = GRAY
        else:
            border_color = BLACK
        # Set border width
        border_width = 2
        if ((BRUSH_SIZE == 1 and button.width == size_small) or (
                BRUSH_SIZE == 2 and button.width == size_medium) or (
                BRUSH_SIZE == 3 and button.width == size_large)):
            border_width = 4
        else:
            border_width = 2
        # Draw border
        pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height),
                            border_width)  # border


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= ROWS:
        raise IndexError
    return row, col


def paint_using_brush(row, col, size):
    if BRUSH_SIZE == 1:
        layers.current.visible_grid[row][col] = drawing_color
    else:  # for values greater than 1
        r = row - BRUSH_SIZE + 1
        c = col - BRUSH_SIZE + 1

        for i in range(BRUSH_SIZE * 2 - 1):
            for j in range(BRUSH_SIZE * 2 - 1):
                if r + i < 0 or c + j < 0 or r + i >= ROWS or c + j >= COLS:
                    continue
                layers.current.visible_grid[r + i][c + j] = drawing_color

            # Checks whether the coordinated are within the canvas


def inBounds(row, col):
    if row < 0 or col < 0:
        return 0
    if row >= ROWS or col >= COLS:
        return 0
    return 1


def fill_bucket(row, col, color):
    # Visiting array
    vis = [[0 for i in range(101)] for j in range(101)]

    # Creating queue for bfs
    obj = []

    # Pushing pair of {x, y}
    obj.append([row, col])

    # Marking {x, y} as visited
    vis[row][col] = 1

    # Until queue is empty
    while len(obj) > 0:

        # Extracting front pair
        coord = obj[0]
        x = coord[0]
        y = coord[1]
        preColor = grid[x][y]

        grid[x][y] = color

        # Popping front pair of queue
        obj.pop(0)

        # For Upside Pixel or Cell
        if inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
            obj.append([x + 1, y])
            vis[x + 1][y] = 1

        # For Downside Pixel or Cell
        if inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
            obj.append([x - 1, y])
            vis[x - 1][y] = 1

        # For Right side Pixel or Cell
        if inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
            obj.append([x, y + 1])
            vis[x][y + 1] = 1

        # For Left side Pixel or Cell
        if inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
            obj.append([x, y - 1])
            vis[x][y - 1] = 1


run = True

clock = pygame.time.Clock()
drawing_color = BLACK

button_width = 40
button_height = 40
button_y_top_row = HEIGHT - TOOLBAR_HEIGHT / 2 - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT / 2 + 1
button_space = 42

size_small = 25
size_medium = 35
size_large = 50

rtb_x = WIDTH + RIGHT_TOOLBAR_WIDTH / 2
brush_widths = [
    Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, "ellipse"),
    Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, "ellipse"),
    Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, "ellipse")
]

# Adding Buttons
buttons = []

for i in range(int(len(COLORS) / 2)):
    buttons.append(
        Button(100 + button_space * i, button_y_top_row, button_width, button_height, COLORS[i]))

for i in range(int(len(COLORS) / 2)):
    buttons.append(Button(100 + button_space * i, button_y_bot_row, button_width, button_height,
                          COLORS[i + int(len(COLORS) / 2)]))

# -------- Layer Functionality --------

# Create layer list object

layers = LayerList()
# add initial layer
layers.addLayer(buttons)

# Add layer button
buttons.append(Button(HEIGHT - 2 * button_width, HEIGHT - button_height - 10, button_width,
                      button_height,
                      WHITE, "Add", BLACK, name="add_layer"))

buttons.append(Button(HEIGHT - 3 * button_width - 5, HEIGHT - button_height - 10, button_width,
                      button_height,
                      WHITE, "Delete", BLACK, name="delete_layer"))

buttons.append(Button(HEIGHT - 3 * button_width - 5, HEIGHT - button_height * 2.3, button_width,
                      button_height,
                      WHITE, "Merge", BLACK, name="merge_layer"))

buttons.append(Button(HEIGHT - 2 * button_width, HEIGHT - button_height * 2.3, button_width,
                      button_height,
                      WHITE, "Visible", BLACK, name="toggle_visibility"))


buttons.append(Button(HEIGHT + 5 - button_width, HEIGHT - button_height * 2.3, button_width,
                      button_height,
                      WHITE, "Up", BLACK, name="move_up"))

buttons.append(Button(HEIGHT + 5 - button_width, HEIGHT - button_height - 10, button_width,
                      button_height,
                      WHITE, "Down", BLACK, name="move_down"))

# -------- Layer Functionality End --------

# set the top grid to be the current layer
grid = layers.get_main_grid()

buttons.append(
    Button(WIDTH - button_space * 1.8, button_y_bot_row, button_width, button_height, WHITE,
           "Erase",
           BLACK, name="erase_btn"))  # Erase Button
buttons.append(
    Button(WIDTH - button_space * 2 - 35, button_y_bot_row, button_width, button_height, WHITE,
           "Clear",
           BLACK, name="clear_btn"))  # Clear Button
buttons.append(
    Button(WIDTH - 3 * button_space + 5, button_y_top_row, button_width - 5, button_height - 5,
           name="FillBucket", image_url="assets/paint-bucket.png"))  # FillBucket
buttons.append(
    Button(WIDTH - 3 * button_space + 45, button_y_top_row, button_width - 5, button_height - 5,
           name="Brush", image_url="assets/paint-brush.png"))  # Brush

draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT / 2 - 30, 60, 60, drawing_color)
buttons.append(draw_button)

while run:
    clock.tick(FPS)  # limiting FPS to 60 or any other value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if user closed the program
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)

                if STATE == "COLOR":
                    paint_using_brush(row, col, BRUSH_SIZE)

                elif STATE == "FILL":
                    fill_bucket(row, col, drawing_color)

            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    if button.text == "Clear":
                        layers.current.reset_grid()
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        break

                    if button.text == "Erase":
                        drawing_color = WHITE
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        break

                    if button.name == "FillBucket":
                        STATE = "FILL"
                        break

                    # add a new layer
                    if button.name == "add_layer":
                        layers.addLayer(buttons)
                        grid = layers.current.visible_grid
                        break

                    # delete a layer
                    if button.name == "delete_layer":
                        layers.deleteLayer(buttons)
                        grid = layers.current.visible_grid
                        break

                    # merge selected layers
                    if button.name == "merge_layer":
                        layers.merge_layers(buttons)
                        break

                    # Toggle layer visibility
                    if button.name == "toggle_visibility":
                        layers.toggle_visible()
                        break

                    # move layer up
                    if button.name == "move_up":
                        layers.move_layer_up()
                        break

                    # move layer down
                    if button.name == "move_down":
                        layers.move_layer_down()
                        break



                    if button.name == "Change":
                        Change = not Change
                        for i in range(10):
                            if i == 0:
                                buttons.append(
                                    Button(HEIGHT - 2 * button_width, (i * button_height) + 5,
                                           button_width, button_height, WHITE, name="Change"))
                            else:
                                if Change == False:
                                    buttons.append(
                                        Button(HEIGHT - 2 * button_width, (i * button_height) + 5,
                                               button_width, button_height, WHITE, "B" + str(i - 1),
                                               BLACK))
                                if Change == True:
                                    buttons.append(
                                        Button(HEIGHT - 2 * button_width, (i * button_height) + 5,
                                               button_width, button_height, WHITE, "C" + str(i - 1),
                                               BLACK))
                        break

                    if button.name == "Brush":
                        STATE = "COLOR"
                        break

                    if button.text is not None:
                        if button.text[0] == 'L':
                            layers.select_layer(button.name)
                            break

                    if button.name is not None:
                        if button.name[0] == 'L':
                            layers.select_multiple_layers(int(button.name[1:]))
                            break


                    drawing_color = button.color
                    draw_button.color = drawing_color

                    break

                for button in brush_widths:
                    if not button.clicked(pos):
                        continue
                    # set brush width
                    if button.width == size_small:
                        BRUSH_SIZE = 1
                    elif button.width == size_medium:
                        BRUSH_SIZE = 2
                    elif button.width == size_large:
                        BRUSH_SIZE = 3

                    STATE = "COLOR"

    # method combines all layers to show as 1 grid
    layers.show_layers()

    draw(WIN, layers.get_main_grid(), buttons)
    # apply hover effect on buttons

    layers.on_hover_effect(buttons)

    pygame.display.update()

pygame.quit()
