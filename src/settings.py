import PyQt6.QtWidgets as Qtw
from src.data import Plot_Type

class Settings:
    # settings dialog
    def create_settings_dialog( self):
        dlg = Qtw.QDialog()
        def settings_save():
            if self.data.vars:
                i=0
                for var, checkbox in zip( self.data.vars, checkboxes):
                    if checkbox.isChecked() and not var.is_visible:
                        self.plot_widget.addItem( self.plot_data_items[i])
                    elif not checkbox.isChecked() and var.is_visible:
                        self.plot_widget.removeItem( self.plot_data_items[i])
                    var.is_visible = checkbox.isChecked()
                    i+=1
            if ts_button.isChecked(): self.data.plot_type = Plot_Type.TIME_SERIES
            elif xy_button.isChecked(): self.data.plot_type = Plot_Type.XY
            elif scatter_button.isChecked(): self.data.plot_type = Plot_Type.SCATTER

            self.show_h_grid = h_grid.isChecked()
            self.show_v_grid = v_grid.isChecked()
            self.plot_widget.getPlotItem().showGrid( x = self.show_v_grid, y = self.show_h_grid)

            if sample_rate_gbox.isChecked():
                try:
                    val = sample_rate.text().strip().replace('u','µ')
                    if val[-1] in ('m','µ'):
                        self.data.sample_rate = float( val[:-1])
                        self.data.sample_rate_scale = val[-1]
                    else:
                        self.data.sample_rate = float( val)
                        self.data.sample_rate_scale = ''
                except Exception as e:
                    print("Sample rate error:" , e, sample_rate.text())
                # adjust scaling
                if self.data.sample_rate_scale == 'µ' and self.data.sample_rate >= 10:
                    self.data.sample_rate /= 1000 
                    self.data.sample_rate_scale = 'm'
                elif self.data.sample_rate_scale == 'm' and self.data.sample_rate >= 10:
                    self.data.sample_rate /= 1000 
                    self.data.sample_rate_scale = ''
                self.x_range = self.data.sample_rate * 100
                self.data.show_time = True
            else:
                self.data.show_time = False
                self.data.sample_rate = 1
                self.data.sample_rate_scale = ''

            dlg.accept()

        dlg.setWindowTitle("Settings")
        main_layout = Qtw.QVBoxLayout()

        QBtn = Qtw.QDialogButtonBox.StandardButton.Save | Qtw.QDialogButtonBox.StandardButton.Cancel
        buttonBox = Qtw.QDialogButtonBox( QBtn)
        buttonBox.accepted.connect( settings_save)
        buttonBox.rejected.connect( dlg.reject)
        
        # vars
        checkboxes:list[Qtw.QCheckBox] = []
        vars_layout = Qtw.QVBoxLayout()
        for var in self.data.vars or []:
            checkbox = Qtw.QCheckBox( var.name)
            checkbox.setChecked( var.is_visible)
            vars_layout.addWidget( checkbox)
            checkboxes.append( checkbox)
        vars_gbox = Qtw.QGroupBox("Variables")
        vars_gbox.setLayout( vars_layout)
        main_layout.addWidget( vars_gbox)

        main_layout.addSpacing(10) # space

        # plot type
        plot_type_layout = Qtw.QVBoxLayout()
        plot_type_gbox = Qtw.QGroupBox("Plot Type")
        plot_type_layout.addWidget( ts_button := Qtw.QRadioButton("Time series"))
        plot_type_layout.addWidget( xy_button := Qtw.QRadioButton("X/Y line"))
        plot_type_layout.addWidget( scatter_button := Qtw.QRadioButton("Scatter plot"))
        if self.data.plot_type == Plot_Type.TIME_SERIES: ts_button.setChecked( True)
        elif self.data.plot_type == Plot_Type.XY: xy_button.setChecked( True)
        elif self.data.plot_type == Plot_Type.SCATTER: scatter_button.setChecked( True)

        plot_type_gbox.setLayout( plot_type_layout)
        main_layout.addWidget( plot_type_gbox)
        if self.plot_data_items:  # plot is active
            plot_type_gbox.setEnabled( False) 

        main_layout.addSpacing(10) # space

        # sample rate
        sample_rate_layout = Qtw.QHBoxLayout()
        sample_rate_gbox = Qtw.QGroupBox("Sample Rate")
        sample_rate_gbox.setCheckable( True)
        sample_rate_gbox.setChecked( self.data.show_time)
        sample_rate_layout.addWidget( Qtw.QLabel("Seconds per sample"))
        sample_rate_layout.addWidget( sample_rate := Qtw.QLineEdit())
        sample_rate.setMaximumWidth( 80)
        sample_rate.setText( str( self.data.sample_rate) + self.data.sample_rate_scale) #TODO add units
        sample_rate_layout.addStretch()
        sample_rate_gbox.setLayout( sample_rate_layout)
        main_layout.addWidget( sample_rate_gbox)
        sample_rate_gbox.setEnabled( False if self.plot_data_items else True) 

        main_layout.addSpacing(10) # space

        # show grids
        show_grid_layout = Qtw.QVBoxLayout()
        show_grid_gbox = Qtw.QGroupBox("Show grid")
        show_grid_layout.addWidget( h_grid := Qtw.QCheckBox("Horizontal grid"))
        show_grid_layout.addWidget( v_grid := Qtw.QCheckBox("Vertical grid"))
        h_grid.setChecked( self.show_h_grid)
        v_grid.setChecked( self.show_v_grid)
        show_grid_gbox.setLayout( show_grid_layout)
        main_layout.addWidget( show_grid_gbox)


        main_layout.addWidget( buttonBox)
        dlg.setLayout( main_layout)
        dlg.exec()