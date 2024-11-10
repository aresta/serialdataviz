# Serial Data Plotter
Plot data from the serial port. Time series plots, XY plots and scatter plots are supported at the moment.

Data can be just numbers separated by comas or spaces, or named variables.

![Serial Data Plotter](img/serialdataviz1.jpg) 

## Requeriments
Python >= 3.8   (I believe, not tested)

## Installation
#### Clone the github repository
```
git clone https://github.com/aresta/serialdataviz
cd serialdataviz
```
#### Install a Python virtual environment (Optional)
```
python -m venv 
. activate
```
#### Install dependencies
```
pip install -r requirements.txt
```

## Run
```
py serialdataviz.py
```

## Serial Data formats
You should send the values in the serial port with one of the next formats, depending on the plot type and if you want to name the variables.

The plot type can be selected in the configuration dialog of the application.
### Time series
- One number per line.
- Several numbers per lines, separated by comas or spaces. Each number will get a default variable name: Var1, Var2...
- Several data pairs, separated by comas or spaces:  
```
<var_name>:number
```

### XY plot and Scatter plot
- Two numbers *x,y* per line, separated by comas or spaces.
- Several pairs, separated by semicolons. Each pair will get a default variable name: Var1, Var2...
```
number,number;
```
- Several structures of var names and values , separated by semicolons:
```
<var_name>:number,number;
```

Take into account that the variable names and the data structure will be parsed only in the first valid line received.  The application expects that all lines will have the same structure, so you shouldn't change the order of the variables afterwards.




## License
Distributed under the GPL v3.0 or later License. See the LICENSE file in the root of the project for more information.






