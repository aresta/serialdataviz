import PyQt6.QtWidgets as Qtw

class Settings:
    # settings dialog
    def create_settings_dialog( self):
        dlg = Qtw.QDialog()
        def settings_save():
            if not self.data.vars: return
            for var, checkbox in zip( self.data.vars, checkboxes):
                var.is_visible = checkbox.isChecked()
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
        vars_group = Qtw.QGroupBox("Variables")
        vars_group.setLayout( vars_layout)
        main_layout.addWidget( vars_group)

        main_layout.addSpacing(10) # space
        # main_layout.addStretch() # space

        # plot type
        plot_type_layout = Qtw.QVBoxLayout()
        plot_type_group = Qtw.QGroupBox("Plot Type")
        plot_type_layout.addWidget( r1 := Qtw.QRadioButton("Time series"))
        plot_type_layout.addWidget( Qtw.QRadioButton("X/Y line"))
        plot_type_layout.addWidget( Qtw.QRadioButton("Scatter plot"))
        r1.setChecked( True)
        plot_type_group.setLayout( plot_type_layout)
        main_layout.addWidget( plot_type_group)

        main_layout.addWidget( buttonBox)
        dlg.setLayout( main_layout)
        dlg.exec()