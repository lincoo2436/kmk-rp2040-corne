import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.scanners.digitalio import MatrixScanner
from kmk.modules.layers import Layers
from kmk.modules.combos import Combos, Chord, Sequence
from kmk.modules.holdtap import HoldTap
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.peg_oled_display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.hid import HIDModes
from kmk.extensions.display import Display, TextEntry, ImageEntry
# For SSD1306
from kmk.extensions.display.ssd1306 import SSD1306
# Replace SCL and SDA according to your hardware configuration.
i2c_bus = busio.I2C(board.SCL, board.SDA)
driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
    # Optional:
    device_address=0x3C,
)
# For displays initialized by CircuitPython by default
# IMPORTANT: breaks if a display backend from kmk.extensions.display is also in use
from kmk.extensions.display.builtin import BuiltInDisplay
# For all display types
display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)
holdtap = HoldTap()
combo_layers = {
  (1, 2): 3,
  }

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        import digitalio
        self.matrix = MatrixScanner(
            cols=self.col_pins,
            rows=self.row_pins,
            diode_orientation=self.diode_orientation,
            pull=digitalio.Pull.DOWN,
            rollover_cols_every_rows=None, # optional
        )
    col_pins = (board.GP29, board.GP28, board.GP27, board.GP26, board.GP22, board.GP20,)
    row_pins = (board.GP4, board.GP5, board.GP6, board.GP7,)
    diode_orientation = DiodeOrientation.COL2ROW
    data_pin = board.GP0
    data_pin2 = board.GP1
    i2c = board.I2C
    SCL=board.SCL
    SDA=board.SDA
    coord_mapping = [
                0,  1,  2,  3,  4,  5,  29, 28, 27, 26, 25, 24,
         6,  7,  8,  9, 10, 11,  35, 34, 33, 32, 31, 30,
        12, 13, 14, 15, 16, 17,  41, 40, 39, 38, 37, 36,
                    21, 22, 23,  47, 46, 45,
    ]
keyboard = MyKeyboard()
# Split code:
split = Split(
    split_target_left=True,
    use_pio = True,
    uart_flip=True,
    split_side=SplitSide.LEFT,
    data_pin=MyKeyboard.data_pin,
    data_pin2=MyKeyboard.data_pin2,
    )
display.entries = [
   TextEntry(text='Layer: ', x=0, y=32, y_anchor='B'),
        TextEntry(text='BASE', x=40, y=32, y_anchor='B', layer=0),
        TextEntry(text='LOWER', x=40, y=32, y_anchor='B', layer=1),
        TextEntry(text='RAISE', x=40, y=32, y_anchor='B', layer=2),
        TextEntry(text='ADJUST', x=40, y=32, y_anchor='B', layer=3),
        TextEntry(text='NUMBER', x=40, y=32, y_anchor='B', layer=4),
        TextEntry(text='MOUSE', x=40, y=32, y_anchor='B', layer=5),
        TextEntry(text='0 1 2 3 4 5', x=0, y=4),
        TextEntry(text='0', x=0, y=4, inverted=True, layer=0),
        TextEntry(text='1', x=12, y=4, inverted=True, layer=1),
        TextEntry(text='2', x=24, y=4, inverted=True, layer=2),
        TextEntry(text='3', x=36, y=4, inverted=True, layer=3),
        TextEntry(text='4', x=48, y=4, inverted=True, layer=4),
        TextEntry(text='5', x=60, y=4, inverted=True, layer=5
        ),
]
keyboard.extensions.append(display)
keyboard.modules.append(Layers(combo_layers))
combos = Combos()
keyboard.modules.append(combos)
keyboard.modules.append(holdtap)
keyboard.modules.append(MouseKeys())
keyboard.modules.append(split)
keyboard.extensions.append(MediaKeys())
# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)
LALT = KC.HT(KC.BSLASH, KC.LALT)
RSHIFT = KC.HT(KC.SLSH, KC.RSFT)

# fmt:off
keyboard.keymap = [
    [  #QWERTY
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,  KC.BSPC,
        KC.CAPS,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,
        KC.LSFT,   LALT, KC.Z,    KC.X,    KC.C,    KC.V,                        KC.B,     KC.N,    KC.M, KC.COMM,  KC.DOT, RSHIFT,
                                            KC.LCTL,   KC.LGUI,  LOWER,    KC.ENT,   KC.SPC,  RAISE,
    ],
    [  #LOWER
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                         KC.N6,   KC.N7,  KC.N8,   KC.N9,   KC.N0, KC.BSPC,
        KC.CAPS, XXXXXXX, XXXXXXX, XXXXXXX, KC.HOME, KC.END,                        KC.LEFT, KC.UP, KC.DOWN,   KC.RIGHT, XXXXXXX, XXXXXXX,
        KC.LSFT, KC.LCTL(KC.GRV), KC.LGUI(KC.GRV), KC.LALT(KC.GRV), KC.BSPC, KC.ENT,                        KC.MINS, KC.EQL, KC.UNDS, KC.PLUS, XXXXXXX, KC.TG(3),
                                            KC.LCTL,   KC.LGUI,  LOWER,     KC.ENT,   KC.SPC,  RAISE,
    ],
    [  #RAISE
        KC.ESC, KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                         KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL,
        KC.LCTL, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                       KC.LBRC,  KC.RBRC,  KC.LCBR, KC.RCBR, KC.PIPE,  KC.GRV,
        KC.LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        KC.MINS, KC.EQL, KC.UNDS, KC.PLUS,  KC.BSLS, KC.TILD,
                                            KC.LCTL,   KC.LGUI,  LOWER,     KC.ENT,   KC.SPC,  RAISE,
    ],
    [  #ADJUST
        KC.ESC, KC.F1,   KC.F2, KC.F3,  KC.F4, KC.F5,                           KC.TILD, KC.AMPR, KC.ASTR, KC.LPRN, KC.UP, KC.DEL,
        KC.CAPS, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10,                            KC.TG(4),  KC.PGUP, KC.PGDN, KC.LEFT, KC.DOWN,  KC.RIGHT,
        KC.LSFT, KC.F11, KC.F12, XXXXXXX, XXXXXXX, KC.LALT,                     KC.TG(5), KC.PLUS, KC.LBRC, KC.RBRC, KC.BSLS, KC.TG(3),
                                            KC.LCTL,   KC.LGUI,  LOWER,     KC.ENT,   KC.SPC,  RAISE,
    ],
    [  #Number
        KC.ESC, KC.EXLM,   KC.N7, KC.N8,  KC.N9, KC.N0,                         XXXXXXX, KC.N7, KC.N8, KC.N9, KC.N0, KC.BSPC,
        KC.LCTL, XXXXXXX, KC.N4, KC.N5, KC.N6, XXXXXXX,                        XXXXXXX,  KC.N4, KC.N5, KC.N6, XXXXXXX,  XXXXXXX,
        KC.LSFT, XXXXXXX, KC.N1, KC.N2, KC.N3, KC.TG(4),                        KC.TG(4), KC.N1, KC.N2, KC.N3, XXXXXXX, XXXXXXX,
                                            KC.LCTL,   KC.LGUI,  LOWER,     KC.ENT,   KC.SPC,  RAISE,
    ],
    [  #MOUSE&Media
        KC.ESC, KC.MUTE,   KC.VOLU, KC.VOLD,  KC.BRIU, KC.BRID,                  KC.MB_LMB, KC.MB_RMB, KC.MW_UP, KC.MW_DN, XXXXXXX, KC.BSPC,
        KC.LCTL, XXXXXXX, KC.N4, KC.N5, KC.MSTP, KC.MPLY,                        KC.MS_LT,  KC.MS_UP, KC.MS_DN, KC.MS_RT, XXXXXXX,  XXXXXXX,
        KC.LSFT, XXXXXXX, KC.N1, KC.MPRV, KC.MNXT, KC.TG(5),                     KC.TG(5), KC.N1, KC.N2, KC.N3, XXXXXXX, XXXXXXX,
                                            KC.LCTL,   KC.LGUI,  LOWER,     KC.ENT,   KC.SPC,  RAISE,
    ],
]
combos.combos = [
    Chord((KC.J, KC.K), KC.ESC),
]

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
