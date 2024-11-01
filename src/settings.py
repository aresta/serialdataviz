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

        main_layout.addSpacing(10) # space

        # sample rate
        sample_rate_layout = Qtw.QHBoxLayout()
        sample_rate_gbox = Qtw.QGroupBox("Sample Rate")
        sample_rate_gbox.setCheckable(True)
        sample_rate_gbox.setChecked(False)
        sample_rate_layout.addWidget( Qtw.QLabel("Seconds per sample"))
        self.sample_rate = Qtw.QLineEdit()
        self.sample_rate.setMaximumWidth(80)
        sample_rate_layout.addWidget( self.sample_rate)
        sample_rate_layout.addStretch()
        sample_rate_gbox.setLayout( sample_rate_layout)
        main_layout.addWidget( sample_rate_gbox)

        main_layout.addWidget( buttonBox)
        dlg.setLayout( main_layout)
        dlg.exec()