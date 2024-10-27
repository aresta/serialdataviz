from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
import pyqtgraph as pg
from src.linearRegionItemFix import LinearRegionItemFix

class Cursors:

    # cursors
    def create_cursors( self):
        cursor_pen = QPen( pg.mkColor( self.CONF['cursors']['line_color']))
        cursor_pen.setStyle( Qt.PenStyle.DotLine)
        cursor_pen.setWidth( 4)
        cursor_pen.setCosmetic( True)
        cursor_penhover = QPen( cursor_pen)
        cursor_penhover.setColor( pg.mkColor( self.CONF['cursors']['line_hover_color']))
        self.cursors_h = LinearRegionItemFix(
            orientation = 'horizontal',
            swapMode = 'push',
            pen = cursor_pen,
            hoverPen = cursor_penhover,
            brush = pg.mkBrush( pg.mkColor( self.CONF['cursors']['bg_color'])), 
            hoverBrush = pg.mkBrush( pg.mkColor( self.CONF['cursors']['bg_hover_color'])))
        self.cursors_h.setZValue(-10)
        self.cursors_v = LinearRegionItemFix(
            swapMode = 'push',
            pen = cursor_pen,
            hoverPen = cursor_penhover,
            brush = pg.mkBrush( pg.mkColor( self.CONF['cursors']['bg_color'])), 
            hoverBrush = pg.mkBrush( pg.mkColor( self.CONF['cursors']['bg_hover_color'])))
        self.cursors_v.setZValue(-10)

        # cursor labels
        pg.InfLineLabel( 
            self.cursors_v.lines[0],
            text = 'x1: {value:0.2f}', 
            position=0.9, color = self.CONF['cursors']['label_color'],
            movable=True)
        pg.InfLineLabel( 
            self.cursors_v.lines[1],
            text = 'x2: {value:0.2f}', 
            position=0.87, color = self.CONF['cursors']['label_color'],
            movable=True)
        pg.InfLineLabel( 
            self.cursors_h.lines[1],
            text = 'y1: {value:0.2f}', 
            position=0.06, color = self.CONF['cursors']['label_color'],
            movable=True)
        pg.InfLineLabel( 
            self.cursors_h.lines[0],
            text = 'y2: {value:0.2f}', 
            position=0.05, color = self.CONF['cursors']['label_color'],
            movable=True)
        self.plot_widget.addItem( self.cursors_h)
        self.plot_widget.addItem( self.cursors_v)
        self.cursors_h.hide()
        self.cursors_v.hide()

        self.cursors_h_deltalabel = pg.TextItem("", color=pg.mkColor( self.CONF['cursors']['label_color']))
        self.cursors_v_deltalabel = pg.TextItem("", color=pg.mkColor( self.CONF['cursors']['label_color']), anchor=( 0.5,0))
        self.plot_widget.addItem( self.cursors_h_deltalabel)
        self.plot_widget.addItem( self.cursors_v_deltalabel)
        self.cursors_h_deltalabel.hide()
        self.cursors_v_deltalabel.hide()

        self.cursors_v.sigRegionChanged.connect( self.cursors_deltalabels_update)
        self.cursors_h.sigRegionChanged.connect( self.cursors_deltalabels_update)
        self.plot_widget.sigRangeChanged.connect( self.plot_range_changed)

    def cursors_h_set_region( self):
        self.cursors_h.show() # should be visible before setRegion
        self.cursors_h.setRegion([ 
            self.plot_widget.visibleRange().center().y() - self.plot_widget.visibleRange().height()/8,
            self.plot_widget.visibleRange().center().y() + self.plot_widget.visibleRange().height()/8 ])

    def cursors_v_set_region( self):
        self.cursors_v.show()
        self.cursors_v.setRegion([ 
            self.plot_widget.visibleRange().center().x() - self.plot_widget.visibleRange().width()/8,
            self.plot_widget.visibleRange().center().x() + self.plot_widget.visibleRange().width()/8 ])
        
    def plot_range_changed( self):
        self.cursors_deltalabels_update()
    
    def cursors_deltalabels_update( self):
        self.cursors_h_deltalabel.setText( "△: {:.2f}".format( self.cursors_h.boundingRect().height()))
        self.cursors_v_deltalabel.setText( "△: {:.2f}".format( self.cursors_v.boundingRect().width()))
        if self.cursors_h_checkbox.isChecked():
            self.cursors_h_deltalabel.setPos( 
                self.plot_widget.visibleRange().left(),
                self.cursors_h.boundingRect().center().y())
        if self.cursors_v_checkbox.isChecked():
            self.cursors_v_deltalabel.setPos( 
                self.cursors_v.boundingRect().center().x(),
                self.plot_widget.visibleRange().bottom()-5)