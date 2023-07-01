import os
os.system('cmd /c "pyrcc5 -o Assets.py Assets.qrc"')

from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import webbrowser
from functools import partial
import texts
import Assets

main_ui_file = 'main_UI.ui'

class Ui(QtWidgets.QMainWindow):
    """this class is used to build class for mainwindow to load GUI application

    :param QtWidgets: _description_
    """

    def __init__(self):
        """this function is used to laod ui file and build GUI application
        """

        super(Ui, self).__init__()

        # app language
        self.language = 'en'

        # load ui file
        uic.loadUi(main_ui_file, self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))

        #
        self._old_pos = None
        self.app_close_flag = False

        # webbrowser
        chrome_path_win = "C://Program Files//Google//Chrome//Application//chrome.exe"
        chrome_path_linux = '/usr/bin/google-chrome %s'
        if sys.platform.startswith('win'):
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path_win))
        elif sys.platform.startswith('linux'):
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path_linux))

        # button connector
        self.button_connector()

        # startup settings
        self.startup_settings()

    def startup_settings(self):
        """this function is used to do startup settings on app start
        """
        return

    def button_connector(self):
        """this function is used to connect ui buttons to their functions
        """
        # top window buttons
        self.minimize_btn.clicked.connect(partial(self.minimize_win))
        self.maximize_btn.clicked.connect(partial(self.maxmize_minimize))
        # close btn
        self.close_btn.clicked.connect(partial(self.close_app))
        # bottom window buttens
        self.dorsa_url_btn.clicked.connect(partial(lambda: webbrowser.open("https://dorsa-co.ir/")))
        return

    def close_app(self):
        """
        this function closes the app
        Inputs: None
        Returns: None
        """
        # create message to confirm close
        res = self.show_alert_window(title=texts.TITLES['close_app'][self.language], message=texts.WARNINGS['app_close_confirm'][self.language], need_confirm=True, level=1)

        if res:
            self.app_close_flag = True

            # close app window and exit the program
            self.close()
            sys.exit()

    def maxmize_minimize(self):
        """
        this function chages the window size of app
        Inputs: None
        Returns: None
        """
        
        if self.isMaximized():
            self.showNormal()

        else:
            self.showMaximized()

    def minimize_win(self):
        """
        this function minimizes the app to taskbar
        Inputs: None
        Returns: None
        """
        self.showMinimized()
    
    def show_alert_window(self, title, message, need_confirm=False, level=0):
        """this function is used to create a confirm window
        :param title: _description_, defaults to 'Message'
        :type title: str, optional
        :param message: _description_, defaults to 'Message'
        :type message: str, optional
        :return: _description_
        :rtype: _type_
        """

        level = 0 if level<0 or level>2 else level

        # create message box
        alert_window = QtWidgets.QMessageBox()

        # icon
        if level==0:
            alert_window.setIcon(QtWidgets.QMessageBox.Information)
        elif level==1:
            alert_window.setIcon(QtWidgets.QMessageBox.Warning)
        elif level==2:
            alert_window.setIcon(QtWidgets.QMessageBox.Critical)

        # message and title
        alert_window.setText(message)
        alert_window.setWindowTitle(title)
        # buttons
        if not need_confirm:
            alert_window.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert_window.button(QtWidgets.QMessageBox.Ok).setText(texts.TITLES['ok'][self.language])
        else:
            alert_window.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
            alert_window.button(QtWidgets.QMessageBox.Ok).setText(texts.TITLES['confirm'][self.language])
            alert_window.button(QtWidgets.QMessageBox.Cancel).setText(texts.TITLES['cancel'][self.language])
        
        alert_window.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        # show
        returnValue = alert_window.exec()

        if not need_confirm:
            return True if returnValue == QtWidgets.QMessageBox.Ok else True
        else:
            return True if returnValue == QtWidgets.QMessageBox.Ok else False


    def mousePressEvent(self, event):
        """mouse press event for moving window

        :param event: _description_
        """

        # accept event only on top and side bars and on top bar
        if event.button() == QtCore.Qt.LeftButton and not self.isMaximized() and event.pos().y()<=self.header.height():
            self._old_pos = event.globalPos()


    def mouseReleaseEvent(self, event):
        """mouse release event for stop moving window

        :param event: _description_
        """

        if event.button() == QtCore.Qt.LeftButton:
            self._old_pos = None


    def mouseMoveEvent(self, event):
        """mouse move event for moving window

        :param event: _description_
        """

        if self._old_pos is None:
            return

        delta = QtCore.QPoint(event.globalPos() - self._old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._old_pos = event.globalPos()


        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()