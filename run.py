from PySide6.QtWidgets import QApplication, QWidget
from ui import MainWindowUI

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main_window = QWidget()
    ui = MainWindowUI()
    ui.setup_ui(main_window)

    main_window.show()

    sys.exit(app.exec())
