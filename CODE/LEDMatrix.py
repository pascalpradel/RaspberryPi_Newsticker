from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix

class LEDMatrix(object):
    def __init__(self, rows=32, cols=128, brightness=100, font="fonts/Calibri-32.bdf", textColor=[0, 255, 0]):
        options = RGBMatrixOptions()
        options.rows = rows
        options.cols = cols
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = brightness
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.panel_type = ""
        #options.hardware_mapping = 'adafruit-hat-pwm'
        options.gpio_slowdown = 4
        options.show_refresh_rate = 0
        options.disable_hardware_pulsing = False
        options.drop_privileges = False

        self.matrix = RGBMatrix(options=options)
        self.offscreenCanvas = self.matrix.CreateFrameCanvas()
        self.font = graphics.Font()
        self.font.LoadFont(font)
        self.textColor = graphics.Color(textColor[0], textColor[1], textColor[2])
        self.pos = self.offscreenCanvas.width

        self.text = ""


    def lenText(self):
        return graphics.DrawText(self.offscreenCanvas, self.font, self.pos, 26, self.textColor, self.text)


    def setText(self, text):
        self.text = text