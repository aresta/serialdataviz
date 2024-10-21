from dataclasses import dataclass
from random import randrange
from src.gui import update_plot

@dataclass
class Data:
    time: list = None
    val: list = None

#  = list( range(50))
#  = [randrange(1, 100) for _ in range(50)]

def process_data( line, data, gui, conf):
    if not data.val: data.val = []
    if not data.time: data.time = [] 
    if len( data.val) > conf['buffer_size']: del data.val[0]
    if len( data.time) > conf['buffer_size']: del data.time[0]
    # delta = randrange( -10, 15) if data[-1] < 50 else randrange( -15, 10)
    # data.append( data[-1] + delta)
    data.val.append( line)
    if not data.time: 
        data.time = [1]
    else:
        data.time.append( data.time[-1] + 1)
    update_plot( data, gui)