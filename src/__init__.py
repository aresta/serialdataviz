import tomllib
from src.data import Data, Var
from src.gui import Gui
from src.cursors import Cursors
from src.settings import Settings

CONF = tomllib.load( open('serialdataviz.conf', mode='rb'))