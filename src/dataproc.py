from src.data import Data, Var

def process_data( data:Data, line:str):
    line = line.strip()
    if ',' in line:
        line_vars = line.split(',')
    elif ' ' in line:
        line_vars = line.split(' ')
    else: line_vars = [line]
    
    if not data.vars:
        if ':' in line_vars[0]:
            data.is_nameval_format = True
            var_names = [ v.split(':')[0] for v in line_vars]
        else:
            var_names = [ f"Var{i+1}" for i in range(line_vars)]
    try:
        if data.is_nameval_format:
            line_vars = [ v.split(':')[1] for v in line_vars]

        line_vars = [ float(v) for v in line_vars]
    except Exception as e:
        print("Error: ", e)
        return

    if not data.vars: 
        data.vars = [ Var(name=var[0],vals=[var[1]]) for var in zip( var_names, line_vars)]
        data.time = [0]
    else:
        for var, line_var in zip( data.vars, line_vars):
            var.vals.append( line_var)
        data.time.append( data.time[-1] + 1)




