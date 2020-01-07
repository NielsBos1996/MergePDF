import sys
import os
import platform
import logging
import PyPDF2
import ctypes
import locale
import subprocess

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox, \
    QTableWidgetItem, QWidget, QLabel

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPixmap

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except Exception:
    pass

# Set logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)

# What OS is running
what_os = platform.system()
if 'Windows' in what_os:
    username = os.environ.get('USERNAME')
    # start_location = 'c:\\Users\\{}\\Documents'.format(username)
    # TODO verwijderen voor release
    start_location = os.getcwd()  # Development setting
    logging.info('OS: Windows')
else:
    username = os.environ.get('USER')
    # start_location = '/Users/{}/Documents'.format(username)
    # TODO verwijderen voor release
    start_location = os.getcwd()  # Development setting
    logging.info('OS: MacOS or Linux')


# PyQT GUI
class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load Main UI
        loadUi('./ui_files/main_window.ui', self)
        # Set Size Application
        self.setFixedSize(640, 480)
        # Set Application Icon
        self.setWindowIcon(QtGui.QIcon('./assets/merge-logo.svg'))

        # Logo
        # label_logo
        self.label_logo = QLabel(self)
        self.label_logo.setGeometry(50, 40, 50, 50)
        pixmap = QPixmap('./assets/merge-logo.svg')
        pixmap = pixmap.scaledToWidth(50)
        self.label_logo.setPixmap(pixmap)

        # Source files field
        # plainTextEdit_source_files

        # Select files button
        # toolButton_choose_files
        self.toolButton_choose_files.clicked.connect(self.choose_files)
        self.files_total = []  # List of upload files

        # Clear field button
        # toolButton_clear_field
        self.toolButton_clear_field.setIcon(QtGui.QIcon('./assets/delete.ico'))
        self.toolButton_clear_field.clicked.connect(self.clear_field)

        # Save-as button
        # toolButton_save_as
        self.toolButton_save_as.clicked.connect(self.save_as)

        # Filename field
        # lineEdit_filename

        # Remove old files checkbox
        # checkBox_delete_old

        # Merge button
        # pushButton_merge
        self.pushButton_merge.clicked.connect(self.merge_files)
        self.new_file_content = []  # List of new file content

        # Taal instellingen
        if 'Windows' in what_os:
            windll = ctypes.windll.kernel32
            windll.GetUserDefaultUILanguage()
            self.os_language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
            logging.info('System language: {}'.format(self.os_language))
            if "nl" in self.os_language:
                # Buttons and fields NL (Only windows)
                self.plainTextEdit_source_files.setPlaceholderText('PDF bestanden')
                self.toolButton_choose_files.setText('Bestanden uploaden...')
                self.toolButton_save_as.setText('Opslaan als...')
                self.plainTextEdit_filename.setPlaceholderText('Locatie voor opslaan')
                self.checkBox_open_file.setText('Open het bestand na het samenvoegen')
                self.checkBox_delete_old.setText('Verwijder oude bestanden')
                self.pushButton_merge.setText('Samenvoegen')
                self.toolButton_clear_field.setToolTip('Leeg het upload  veld')
                # QFileDialog
                self.files_filename_window = 'PDF bestanden (*.pdf)'
                # Messageboxes
            else:
                # Buttons and fields EN
                self.plainTextEdit_source_files.setPlaceholderText('PDF files')
                self.toolButton_choose_files.setText('Upload files...')
                self.toolButton_save_as.setText('Save as...')
                self.plainTextEdit_filename.setPlaceholderText('Save location')
                self.checkBox_open_file.setText('Open file after merge')
                self.checkBox_delete_old.setText('Delete old files')
                self.pushButton_merge.setText('Merge')
                self.toolButton_clear_field.setToolTip('Clear upload field')
                # QFileDialog
                self.files_filename_window = 'PDF files (*.pdf)'
                # Messageboxes
        # MacOS and Linux
        else:
            self.loc = locale.getlocale()  # get current locale
            logging.info('System language: {}'.format(self.loc))
            if "nl_NL" in self.loc:
                # Buttons and fields NL (Only windows)
                self.plainTextEdit_source_files.setPlaceholderText('PDF bestanden')
                self.toolButton_choose_files.setText('Bestanden uploaden...')
                self.toolButton_save_as.setText('Opslaan als...')
                self.plainTextEdit_filename.setPlaceholderText('Locatie voor opslaan')
                self.checkBox_open_file.setText('Open het bestand na het samenvoegen')
                self.checkBox_delete_old.setText('Verwijder oude bestanden')
                self.pushButton_merge.setText('Samenvoegen')
                self.toolButton_clear_field.setToolTip('Leeg het upload  veld')
                # QFileDialog
                self.files_filename_window = 'PDF bestanden (*.pdf)'
                # Messageboxes
            else:
                # Buttons and fields EN
                self.plainTextEdit_source_files.setPlaceholderText('PDF files')
                self.toolButton_choose_files.setText('Upload files...')
                self.toolButton_save_as.setText('Save as...')
                self.plainTextEdit_filename.setPlaceholderText('Save location')
                self.checkBox_open_file.setText('Open file after merge')
                self.checkBox_delete_old.setText('Delete old files')
                self.pushButton_merge.setText('Merge')
                self.toolButton_clear_field.setToolTip('Clear upload field')
                # QFileDialog
                self.files_filename_window = 'PDF files (*.pdf)'
                # Messageboxes

    # Functions
    def choose_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, " ", start_location,
                                                self.files_filename_window, options=options)

        # File selector
        for i in range(len(files)):
            if len(self.files_total) < 5:
                self.plainTextEdit_source_files.appendPlainText(os.path.basename(files[i]))
                self.files_total.append(files[i])
            else:
                self.toolButton_choose_files.setEnabled(False)
                self.criticalbox('Maximum bereikt!\nVoor het uploaden van meer bestanden koop de '
                                 'pro versie\nhttps://snipbasic.com/')

        logging.info('Items in  files_total: {}'.format(len(self.files_total)))

    # Clear Field
    def clear_field(self):
        self.plainTextEdit_source_files.clear()
        self.files_total = []
        self.toolButton_choose_files.setEnabled(True)
        logging.info('Items in  files_total: {}'.format(len(self.files_total)))

    # Save merged file
    def save_as(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getSaveFileName(self, " ", start_location,
                                                self.files_filename_window, options=options)

        if files:
            file, extension = os.path.splitext(files)
            if extension:  # Check file extension
                if '.pdf' in extension:
                    self.plainTextEdit_filename.setPlainText(files)
                    logging.info('Save file as: {}'.format(files))
                else:
                    self.warningbox('\nDe extensie {} is niet toegestaan'.format(extension))
                    logging.error('Save file as: {} is not allowed'.format(extension))
            else:
                self.plainTextEdit_filename.setPlainText(files + '.pdf')
                logging.info('Save file as: {}.pdf'.format(files))

    # Merge Files
    def merge_files(self):
        save_location = self.plainTextEdit_filename.toPlainText()

        # Checks
        if len(self.files_total) < 2:
            logging.error('Less than 2 documents')
            self.warningbox('Upload minimaal 2 PDF documenten')  # Less than 2 documents
            return
        if not save_location:
            logging.error('No save location set')
            self.warningbox('Bepaal de locatie voor het opslaan')  # No save location
            return

        writer = PyPDF2.PdfFileWriter()  # Openen blanco PDF bestand

        try:
            pdf_file_objs = [open(file, 'rb') for file in self.files_total]
            readers = [PyPDF2.PdfFileReader(pdf_file_obj) for pdf_file_obj in pdf_file_objs]
            for file in readers:
                for page in range(file.numPages):
                    writer.addPage(file.getPage(page))

            # IMPORTANT! Make sure to save the new file before closing the involved pdf files
            with open(save_location, 'wb') as output_file:
                writer.write(output_file)

        finally:
            # Now close all the files
            [elem.close() for elem in pdf_file_objs]

        logging.info('File merge completed')

        if self.checkBox_delete_old.isChecked():
            logging.info('Checkbox is checked')
            # Delete files
            for files in range(len(self.files_total)):
                logging.info('File removed: {}'.format(self.files_total[files]))
                if self.files_total:
                    os.unlink(self.files_total[files])
            self.checkBox_delete_old.setChecked(False)  # Reset checkbox

        # Open the new file
        if self.checkBox_open_file.isChecked():
            try:
                # Check OS and open PDF in default PDF reader
                if "Windows" in what_os:
                    os.startfile(save_location)
                    logging.info('Open file after merge (Windows)')
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, save_location])
                    if opener == "open":
                        logging.info('Open file after merge (MacOS)')
                    else:
                        logging.info('Open file after merge (Linux)')
            except Exception:
                self.warningbox('Het nieuwe bestand is aangemaakt maar kon niet geopend worden.')
                logging.error('{} Can not be opened'.format(save_location))

        # Reset input fields
        self.plainTextEdit_source_files.clear()
        self.files_total = []
        self.toolButton_choose_files.setEnabled(True)
        self.plainTextEdit_filename.clear()
        self.checkBox_open_file.setChecked(False)
        logging.info('Reset all fields completed')

    # Messageboxen
    def criticalbox(self, message):
        buttonReply = QMessageBox.critical(self, 'Error', message, QMessageBox.Close)

    def warningbox(self, message):
        buttonReply = QMessageBox.warning(self, 'Warning', message, QMessageBox.Close)


def main():
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
