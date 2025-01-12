

def message(text, color, position):
    msg = font_style.render(text, True, color)
    screen.blit(msg, position)

def draw_borders():
    pygame.draw.rect(screen, YELLOW, (PLAYABLE_X_OFFSET, PLAYABLE_Y_OFFSET, PLAYABLE_WIDTH, PLAYABLE_HEIGHT), 5)  # Border thickness is 5
