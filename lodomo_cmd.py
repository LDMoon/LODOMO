import fonts
import themes
import cmd_requests
from sys import exit


def command_prompt(user_input):
    u_input = user_input.upper()
    maximum_request = 50
    response = []
    input_dict = {}

    # restrict request length
    while len(u_input) > maximum_request:
        u_input = u_input[:-1]

    # Return 0 for further input from user. Return Text for further processing from script.
    if u_input in cmd_requests.cmd_inputs:
        input_dict = cmd_requests.cmd_inputs[u_input]
    else:
        input_dict = cmd_requests.cmd_inputs['ERROR']

    response.append(u_input)
    response.append(input_dict['RESPONSE'])
    code = input_dict['CODE']
    return [response, code]


# CMD Loop
def CMD_Loop(screen, current_version, pygame, mouse_cursor, clock):
    # Theme
    frame_size = [366, 198]
    current_theme = themes.CMDTheme(themes.plain)
    lodomo_location = (15, 2)

    # This pads the text. This needs to be fine-tuned.
    frame_padding = 9
    text_padding_x = 20
    text_padding_y = 24
    version_position = (335, 208)

    # This contains all the text displayed in CMD. TODO output to file.
    main_text = []

    # Boot Text
    main_text.append('LOODOMO [VERSION 0.01A]')
    main_text.append('(C) L.D. MOON STUDIO. ALL RIGHTS RESERVED')

    main_text_max_lines = 20
    vertical_spacing = 8
    user_input = ''
    blinking_cursor = '|'
    blinking_timer = 0
    valid_characters = '1234567890-=qwertyuiop[]asdfghjkl;zxcvbnm,./!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?\' '
    cmd_running = True

    result = ['', 0]

    while cmd_running:
        # Fill the screen with background color.
        screen.fill(current_theme.background_color)

        # Draw the Frame
        screen.blit(current_theme.input_frame, (frame_padding, frame_padding))
        screen.blit(current_theme.lodomo_logo, lodomo_location)

        # Draw version number
        version_number = fonts.babyblocks.render('VERSION ' + current_version, False, current_theme.version_text_color)
        screen.blit(version_number, version_position)

        # Draw the Cursor
        mouse_posit = pygame.mouse.get_pos()
        screen.blit(mouse_cursor, mouse_posit)

        # Blinking Cursor
        if blinking_timer < 30:
            blinking_timer += 1
        else:
            blinking_timer = 0
            if blinking_cursor == '|':
                blinking_cursor = ' '
            else:
                blinking_cursor = '|'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    while len(main_text) >= main_text_max_lines:
                        main_text.pop(0)
                    result = command_prompt(user_input)
                    return_text = result[0]
                    for text in return_text:
                        main_text.append(text)
                    user_input = ''
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1].upper()
                # WRITE IN ALL UPPER CASE
                if event.unicode in valid_characters:
                    user_input += event.unicode.upper()
                # Close On Escape
                if event.key == pygame.K_ESCAPE:
                    cmd_running = not cmd_running

        # Update all the text not being used.
        for i in range(len(main_text)):
            text_surface = fonts.babyblocks.render(main_text[i], True, current_theme.text_color)
            screen.blit(text_surface, (text_padding_x, text_padding_y + (vertical_spacing * i)))

        # Put user inputs on the screen
        display_input = user_input + blinking_cursor
        text_input_surface = fonts.babyblocks.render('> ' + display_input, False, current_theme.text_color)
        screen.blit(text_input_surface, (text_padding_x, text_padding_y + vertical_spacing * len(main_text)))

        # Handle Inputs
        if result[1] != 0:
            # Change Themes
            if result[1] == 1:
                theme_to_load = themes.Load_Theme(result[0][0])
                current_theme = themes.CMDTheme(theme_to_load)
            if result[1] == 2:
                return 2
            if result[1] == 3:
                return 3
            # Stop Requests
            result[1] = 0

        pygame.display.update()
        clock.tick(60)