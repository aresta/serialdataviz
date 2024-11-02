from src.data import Data, Var, Data_Format, Plot_Type


def process_time_series( data:Data, line:str):
    if ',' in line:
        line_vars = line.split(',')
    elif ' ' in line:
        line_vars = line.split(' ')
    else: line_vars = [line]
    
    if not data.vars:
        if ':' in line_vars[0]:
            data.data_format = Data_Format.VAR_NAMES
            var_names = [ v.split(':')[0] for v in line_vars]
        else:
            var_names = [ f"Var{i+1}" for i in range( len(line_vars))]

    try:
        if data.data_format == Data_Format.VAR_NAMES:
            line_vars = [ v.split(':')[1] for v in line_vars]
        line_vars = [ float(v) for v in line_vars]
    except Exception as e:
        print("Error: ", e, line_vars)
        return

    if not data.vars: 
        data.vars = [ Var(name=var[0], y=[var[1]]) for var in zip( var_names, line_vars)]
        data.time = [0]
    else:
        for var, line_var in zip( data.vars, line_vars):
            var.y.append( line_var)
        data.time.append( data.time[-1] + 1)


def process_xy( data:Data, line:str):
    if ';' in line:
        line_vars = line.split(';')
    else: 
        line_vars = [line]

    if not data.vars:
        if ':' in line_vars[0]:
            data.data_format = Data_Format.VAR_NAMES
            var_names = [ v.split(':')[0] for v in line_vars]
        else:
            var_names = [ f"Var{i+1}" for i in range( len(line_vars))]
 
    try:
        if data.data_format == Data_Format.VAR_NAMES:
            line_vars = [ v.split(':')[1] for v in line_vars]
        coords = [ v.split(',') for v in line_vars]
        coords = [ (float(x), float(y)) for x,y in coords]
    except Exception as e:
        print("Error: ", e, line_vars)
        return

    if not data.vars: 
        data.vars = [ Var( name=name, x=[coord[0]], y=[coord[1]]) for name,coord in zip( var_names, coords)]
    else:
        for var, coord in zip( data.vars, coords):
            var.x.append( coord[0])
            var.y.append( coord[1])

def process_data( data:Data, line:str):
    line = line.strip()
    if data.plot_type == Plot_Type.TIME_SERIES:
        process_time_series( data, line)
    elif data.plot_type == Plot_Type.XY:
        process_xy( data, line)
    elif data.plot_type == Plot_Type.SCATTER:
        process_xy( data, line) # same line formats
    
    




