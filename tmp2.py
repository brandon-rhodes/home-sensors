import os
print([i for i in os.environ.items() if i[0].startswith('BLINKA')])

# import adafruit_hdc302x
# import adafruit_scd4x
# import adafruit_sgp40

import board
# print(dir(board))
# exit()
print(board.board_id)
print('Board:', board.detector.board.id)
print('Chip:', board.detector.chip.id)
print(dir(board))
i2c = board.I2C()
print(i2c.scan())
