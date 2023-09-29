#!/usr/bin/env python

from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
import time

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 128
options.chain_length = 1
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 0
options.pwm_bits = 11
options.brightness = 100
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RGB"
options.pixel_mapper_config = ""
options.panel_type = ""
#options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 4
options.show_refresh_rate = 0
options.disable_hardware_pulsing = False
options.drop_privileges = False

#Creating matrix instance
matrix = RGBMatrix(options=options)

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("fonts/Calibri-26.bdf")
textColor = graphics.Color(0, 255, 0)
pos = offscreen_canvas.width
#my_text = "Hello World!"
my_text = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz,;.:-_öäü+*#'!€§$%&/()="

counter = 0
while True:
    offscreen_canvas.Clear()
    len = graphics.DrawText(offscreen_canvas, font, pos, 26, textColor, my_text)
    pos -= 1
    
    
    print(len, pos)
    
    if (pos + len < 0):
        pos = offscreen_canvas.width

    """
    
    if (pos + len < 128):
        my_text += " Hello World #" + str(counter) +"!"
        counter+= 1
    """    


    time.sleep(0.01)
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)