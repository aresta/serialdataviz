from dataclasses import dataclass
from random import randrange
from src.datastructs import Gui, Data
from src.gui import update_plot



#  = list( range(50))
#  = [randrange(1, 100) for _ in range(50)]

def process_data( line:str, data:Data, gui:Gui, conf):
    line = line.strip()
    if ',' in line:
        line_vars = line.split(',')
    elif ' ' in line:
        line_vars = line.split(' ')
    else: return
    
    try:
        line_vars = [ float(v) for v in line_vars]
    except Exception as e:
        print("Error: ", e)
        print("line_Vars:", line_vars)
        return

    if not data.vars: 
        data.vars = [[var] for var in line_vars]
        data.time = [0]
        data.vars_num = len( line_vars)
    else:
        i = 0
        for line_var in line_vars:
            data.vars[i].append( line_var)
            i +=1
        data.time.append( data.time[-1] + 1)

    if len( data.time) > conf['buffer_size']: 
        for var in data.vars: del var[0]
        del data.time[0]

    update_plot( data, gui)