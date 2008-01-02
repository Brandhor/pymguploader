from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *
import os
import sys
import re
if not hasattr(sys, "frozen"):
    os.popen("pyuic4 ui.ui -o ui.py").read()
    os.popen("pyrcc4 res.qrc -o res_rc.py").read()
import ui
import imgsite
import tempfile
from watermark import *

class ImageUploader(QMainWindow):
    def __init__(self,  parent=None):
        super(ImageUploader, self).__init__(parent)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        reg = QRegExp("\\d*%")
        val = QRegExpValidator(reg, self)
        self.ui.watermarkX.setValidator(val)
        self.ui.watermarkY.setValidator(val)
        self.counter = 0
        self.watermark = ""
        tempfile.tempdir = tempfile.mkdtemp(prefix="pymguploader")
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Pymguploader")
        self.scanSite()
        self.loadSettings()
        
        self.connect(self.ui.btnAdd,  SIGNAL("clicked()"), self.addClicked)
        self.connect(self.ui.btnAddFolder,  SIGNAL("clicked()"),  self.addFolderClicked)
        self.connect(self.ui.btnCancel, SIGNAL("clicked()"), self.cancelUpload)
        self.connect(self.ui.btnRemove,  SIGNAL("clicked()"), self.removeClicked)
        self.connect(self.ui.btnUpload,  SIGNAL("clicked()"), self.uploadClicked)
        self.connect(self.ui.btnDelete,  SIGNAL("clicked()"),  self.deleteImages)
        
        self.connect(self.ui.pbAddWatermark, SIGNAL("clicked()"), self.addWatermark)
        self.connect(self.ui.pbRemoveWatermark, SIGNAL("clicked()"), self.removeWatermark)
        self.connect(self.ui.rbCustom, SIGNAL("toggled(bool)"), self.wmCustomToggled)
    
    def deleteImages(self):
        res = QMessageBox.question(self,  "Warning", "Are you sure you want to delete these images?", QMessageBox.Ok |QMessageBox.Cancel)
        
        if res == QMessageBox.Ok:
            for i in xrange(0, self.ui.imgList.count()):
                os.remove(str(self.ui.imgList.item(i).text()))
            self.ui.imgList.clear()
            
    def addFolderClicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        filters = QStringList()
        for f in ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tif", "*.tiff"]:
            filters.append(f)
        iList = QDir(dir).entryInfoList(filters)
        
        for f in iList:
            QListWidgetItem(QIcon(f.filePath()), f.filePath(), self.ui.imgList)
        
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            fn = url.toLocalFile()
            if fn.endsWith(".png", Qt.CaseInsensitive)  or \
               fn.endsWith(".jpg", Qt.CaseInsensitive)  or \
               fn.endsWith(".jpeg", Qt.CaseInsensitive) or \
               fn.endsWith(".gif", Qt.CaseInsensitive)  or \
               fn.endsWith(".tiff", Qt.CaseInsensitive) or \
               fn.endsWith(".tif", Qt.CaseInsensitive)  or \
               fn.endsWith(".bmp", Qt.CaseInsensitive):
                   QListWidgetItem(QIcon(fn),  fn,  self.ui.imgList)
        
    def loadSettings(self):
        if self.settings.contains("defaultsite"):
            self.ui.comboSite.setCurrentIndex(self.ui.comboSite.findText(self.settings.value("defaultsite").toString()))
        
        self.settings.beginGroup("watermark")
        self.watermark = self.settings.value("file").toString()
        self.ui.displayWatermark.setPixmap(QPixmap(self.watermark))
        self.ui.spinOpacity.setValue(self.settings.value("opacity", QVariant(1)).toDouble()[0])
        self.ui.watermarkX.setText(self.settings.value("x").toString())
        self.ui.watermarkY.setText(self.settings.value("y").toString())
        position = self.settings.value("position").toString()
        
        if position == "bottomleft":
            self.ui.rbBottomLeft.setChecked(True)
        elif position == "bottomright":
            self.ui.rbBottomRight.setChecked(True)
        elif position == "upperright":
            self.ui.rbUpperRight.setChecked(True)
        elif position == "upperleft":
            self.ui.rbUpperLeft.setChecked(True)
        elif position == "tile":
            self.ui.rbTiled.setChecked(True)
        elif position == "scaled":
            self.ui.rbScaled.setChecked(True)
        elif position == "custom":
            self.ui.rbCustom.setChecked(True)
            self.wmCustomToggled(True)
            
        self.settings.endGroup()
        
    def closeEvent(self, event):
        self.settings.setValue("defaultsite", QVariant(self.ui.comboSite.currentText()))
        
        self.settings.beginGroup("watermark")
        self.settings.setValue("file", QVariant(self.watermark))
        self.settings.setValue("opacity", QVariant(self.ui.spinOpacity.value()))
        self.settings.setValue("x", QVariant(self.ui.watermarkX.text()))
        self.settings.setValue("y", QVariant(self.ui.watermarkY.text()))
        
        if self.ui.rbBottomLeft.isChecked():
            position="bottomleft"
        elif self.ui.rbBottomRight.isChecked():
            position="bottomright"
        elif self.ui.rbUpperRight.isChecked():
            position="upperright"
        elif self.ui.rbUpperLeft.isChecked():
            position="upperleft"
        elif self.ui.rbTiled.isChecked():
            position="tiled"
        elif self.ui.rbScaled.isChecked():
            position="scaled"
        elif self.ui.rbCustom.isChecked():
            position="custom"
        self.settings.setValue("position", QVariant(position))
        self.settings.endGroup()
        
        for root, dirs, files in os.walk(tempfile.tempdir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(tempfile.tempdir)
        event.accept()
            
    def cancelUpload(self):
        self.uploadList = {}
        self.site[str(self.ui.comboSite.currentText())].cancelUpload()
        
    def scanSite(self):
        self.site = {}
        for s in dir(imgsite):
            try:
                if re.match("^[A-Z]", s):
                    c = eval("imgsite."+s+"(self)")
                    self.site[str(c)] = c
                    self.connect(c,  SIGNAL("done(QString)"), self.upload)
            except Exception, e:
                QMessageBox.warning(None, "Exception", str(e))
        
        for s in self.site:
            self.ui.comboSite.addItem(s)
                
    def addClicked(self):
        ls = QFileDialog.getOpenFileNames(self, "Select images to upload", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp *.tif *.tiff);; All *.*")
        for l in ls:
            QListWidgetItem(QIcon(l), l, self.ui.imgList)
            
    def removeClicked(self):
        i = self.ui.imgList.takeItem(self.ui.imgList.currentRow())
        del i
        
    def uploadClicked(self):
        self.uploadList = []
        for i in xrange(0, self.ui.imgList.count()):
            self.uploadList.append(self.ui.imgList.item(i).text())
        self.ui.pbTotal.setMaximum(self.ui.imgList.count())
        self.ui.pbTotal.setValue(0)
        self.upload()
        
    def upload(self, code=None):
        if code:
            self.ui.textBBCode.setText(self.ui.textBBCode.toPlainText()+code)
            self.counter += 1
            if self.counter == 4:
                self.ui.textBBCode.setText(self.ui.textBBCode.toPlainText()+"\n")
                self.counter = 0
                
                
        if not len(self.uploadList):
            return
        
        self.ui.pbTotal.setValue(self.ui.pbTotal.value()+1)
        self.ui.lblTotal.setText("Uploading %d of %d"%(self.ui.pbTotal.value(),  self.ui.pbTotal.maximum()))
        it = self.uploadList.pop(0)
        if self.watermark:
            it = self.doWatermark(it)           
        self.site[str(self.ui.comboSite.currentText())].upload(it)

    def addWatermark(self):
        f = QFileDialog.getOpenFileName(self, "Select watermark", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp *.tif *.tiff);; All *.*")
        self.watermark = f
        self.ui.displayWatermark.setPixmap(QPixmap(f))
            
    def removeWatermark(self):
        self.watermark = ""
        self.ui.displayWatermark.setPixmap(QPixmap())    
            
    def doWatermark(self, it):
        if self.ui.rbBottomLeft.isChecked():
            position="bottomleft"
        elif self.ui.rbBottomRight.isChecked():
            position="bottomright"
        elif self.ui.rbUpperRight.isChecked():
            position="upperright"
        elif self.ui.rbUpperLeft.isChecked():
            position="upperleft"
        elif self.ui.rbTiled.isChecked():
            position="tiled"
        elif self.ui.rbScaled.isChecked():
            position="scaled"
        elif self.ui.rbCustom.isChecked():
            position=(self.ui.watermarkX.text(), self.ui.watermarkY.text())
        
        w = watermark(it, self.watermark, position=position, opacity=self.ui.spinOpacity.value())
        fn = os.path.join(tempfile.tempdir, str(QFileInfo(it).fileName()))
        w.save(fn)
        return fn
    
    def wmCustomToggled(self, checked):
        if checked:
            self.ui.watermarkX.setEnabled(True)
            self.ui.watermarkY.setEnabled(True)
            self.ui.labelX.setEnabled(True)
            self.ui.labelY.setEnabled(True)
        else:
            self.ui.watermarkX.setEnabled(False)
            self.ui.watermarkY.setEnabled(False)
            self.ui.labelX.setEnabled(False)
            self.ui.labelY.setEnabled(False)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ImageUploader()
    mw.show()
    sys.exit(app.exec_())
