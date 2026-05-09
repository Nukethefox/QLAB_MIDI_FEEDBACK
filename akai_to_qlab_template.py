import mido

# --- Put here the exact device names ---
AKAI_IN  = 'APC mini mk2 Control'
QLAB_OUT = 'Driver IAC IACtoQLAB'

# --- Put here the exact buttons used  ---
# --- (in this example, on the AKAI APC MINI MK2, I'm using the first 7 buttons on each row + the first 4 buttons above the faders)
QLAB_NOTES = [
  56,57,58,59,60,61,62,
  48,49,50,51,52,53,54,
  40,41,42,43,44,45,46,
  32,33,34,35,36,37,38,
  24,25,26,27,28,29,30,
  16,17,18,19,20,21,22,
  8,9,10,11,12,13,14,
  0,1,2,3,4,5,6,
  104,105,106,107
]

# --- channel config ---
IN_CHANNEL  = 1   # AKAI sends on ch1
OUT_CHANNEL = 10  # QLab listens on ch10

# Just like in the code above, each row represents a physical row...
# I'm using 104 row as panic, go, pause, resume
# colours: 0 off, 3 white, blue 40-44-41-45, red 5, orange 60, yellow 13, green 21 or 17, 54 dark pink
GRID_COLORS = {
  56: 40, 57: 21, 58: 13, 59: 5, 60: 40, 61: 54, 62: 54,
  48: 40, 49: 13, 50: 5, 51: 40, 52: 5, 53: 54, 54: 54,
  40: 40, 41: 13, 42: 21, 43: 54, 44: 0, 45: 54, 46: 54,
  32: 40, 33: 45, 34: 45, 35: 45, 36: 0, 37: 54, 38: 54,
  24: 40, 25: 13, 26: 5, 27: 0, 28: 0, 29: 54, 30: 54,
  16: 40, 17: 13, 18: 21, 19: 5, 20: 45, 21: 45, 22: 0,
  8: 40, 9: 13, 10: 21, 11: 5, 12: 45, 13: 45, 14: 0,
  0: 45, 1: 45, 2: 45, 3: 45, 4: 45, 5: 45, 6: 45
}

GRID_CHANNEL = 7  # use channel 7 for main buttons grid, for max brightness


EXTRA_COLORS = {
  104: 1, 105: 1, 106: 5, 107: 1
}

EXTRA_CHANNEL = 1  # use channel 1 for small buttons on the AKAI (they are only on/off, no colors)


akai_in  = mido.open_input(AKAI_IN)
akai_out = mido.open_output(AKAI_IN)
qlab_out = mido.open_output(QLAB_OUT)

# --- turn on LEDs at start ---
for note in GRID_COLORS:
    akai_out.send(
        mido.Message(
            'note_on',
            note=note,
            velocity=GRID_COLORS[note],
            channel=GRID_CHANNEL - 1
        )
    )

for note in EXTRA_COLORS:
    akai_out.send(
        mido.Message(
            'note_on',
            note=note,
            velocity=EXTRA_COLORS[note],
            channel=EXTRA_CHANNEL - 1
        )
    )

print("MIDI bridge + LEDs are active now. Ctrl+C to exit.")

# --- main loop to send to qlab ---
for msg in akai_in:
    if msg.type == 'note_on' and msg.note in QLAB_NOTES:
        if msg.channel + 1 == IN_CHANNEL:
            msg.channel = OUT_CHANNEL - 1
            qlab_out.send(msg)
