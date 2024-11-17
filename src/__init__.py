import tomli
from src.data import Data, Var
from src.gui import Gui
from src.cursors import Cursors
from src.settings import Settings

CONF = tomli.load( open('serialdataviz.conf', mode='rb'))