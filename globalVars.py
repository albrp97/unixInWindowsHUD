import pygame

black = pygame.Color("#2E3440")
grey = pygame.Color("#4C566A")
greyLigth = pygame.Color("#D8DEE9")
white = pygame.Color("#ECEFF4")
red = pygame.Color("#BF616A")
orange = pygame.Color("#D08770")
yellow = pygame.Color("#EBCB8B")
green = pygame.Color("#A3BE8C")
violet = pygame.Color("#B48EAD")
violetLight = pygame.Color("#afa4ee")
blueDark = pygame.Color("#5E81AC")
blue = pygame.Color("#81A1C1")
cyan = pygame.Color("#88C0D0")

def color_gradient(start_color, end_color, steps):
    # Extract the RGB values of the start and end colors
    start_rgb = start_color.r, start_color.g, start_color.b
    end_rgb = end_color.r, end_color.g, end_color.b

    # Calculate the step size for each RGB component
    step_size = [(end - start) / steps for start, end in zip(start_rgb, end_rgb)]

    # Generate a list of colors representing the gradient between start and end colors
    gradient_colors = [pygame.Color(int(start_rgb[0] + step_size[0] * i),
                                int(start_rgb[1] + step_size[1] * i),
                                int(start_rgb[2] + step_size[2] * i)) for i in range(steps)]

    return gradient_colors

def color_gradient_with_repeats(color_list, steps, repeats):
    """
    Generates a color gradient between all colors in the input list, with repeated original colors.
    :param color_list: a list of pygame.Color objects representing the original colors.
    :param steps: an integer representing the number of steps in the gradient between each pair of colors.
    :param repeats: an integer representing the number of times each original color should be repeated before the next gradient starts.
    :return: a list of pygame.Color objects representing the gradient.
    """
    gradient = []
    for i, color in enumerate(color_list[:-1]):
        # Repeat the original color k times
        gradient.extend([color] * repeats)

        # Calculate the gradient between this color and the next color
        next_color = color_list[i+1]
        gradient.extend(color_gradient(color, next_color, steps))

    # Repeat the last color k times
    gradient.extend([color_list[-1]] * repeats)

    return gradient

