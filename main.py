import sys

from Interface import *


version = "v0.2"

if __name__ == '__main__':

    app = QApplication(sys.argv)
    # CSS style sheet: https://doc.qt.io/archives/qt-4.8/stylesheet-examples.html#customizing-qgroupbox
    app.setStyleSheet('''
        QWidget {
            font-size: 14px;
        }
        
        QLabel {
            text-align: center;
        }
        
        QTextBrowser {
            font-size: 12px;
        }
    ''')

    ui = Interface(f"Price Comparison Tool ({version})", './images/price_tag_euro.ico')

    try:
        sys.exit(app.exec())

    except SystemExit:
        print("Closing window ... Auf Wiedersehen!")



