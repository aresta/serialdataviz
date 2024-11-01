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
        data.vars = [ Var(name=var[0],vals=[var[1]]) for var in zip( var_names, line_vars)]
        data.time = [0]
    else:
        for var, line_var in zip( data.vars, line_vars):
            var.vals.append( line_var)
        data.time.append( data.time[-1] + 1)


def process_xy( data:Data, line:str):
    if ',' in line:
        line_vars = line.split(',')
    elif ' ' in line:
        line_vars = line.split(' ')
    else: return
    if len( line_vars) != 2: return

    try:
        line_vars = ( float( line_vars[0]), float( line_vars[1]))
    except Exception as e:
        print("Error: ", e, line_vars)
        return

    if not data.vars:
        data.vars = [ Var( name = "Var1", vals = [])]
    data.vars[0].vals.append( line_vars)


def process_data( data:Data, line:str):
    line = line.strip()
    if data.plot_type == Plot_Type.TIME_SERIES:
        process_time_series( data, line)
    elif data.plot_type == Plot_Type.XY:
        process_xy( data, line)
    
    




