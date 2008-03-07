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
import postmarkup
from watermark import *
from ImageQt import ImageQt
try:
    from QLCoverFlow import QLCoverFlow
    from QLCoverFlowItem import QLCoverFlowItem
    USE_COVERFLOW = True
except:
    USE_COVERFLOW = False

class ImageUploader(QMainWindow):
    def __init__(self,  parent=None):
        super(ImageUploader, self).__init__(parent)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        if USE_COVERFLOW:
            self.coverFlow = QLCoverFlow()
            self.coverFlow.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.coverFlow.setFocusPolicy(Qt.ClickFocus)
            self.coverFlow.hide()
            self.ui.hboxlayout.insertWidget(0, self.coverFlow)
            self.connect(self.ui.btnCoverFlow,  SIGNAL("clicked()"),  self.toggleCoverFlow)
        else:
            self.ui.btnCoverFlow.hide()
        
        reg = QRegExp("\\d*%")
        val = QRegExpValidator(reg, self)
        self.ui.watermarkX.setValidator(val)
        self.ui.watermarkY.setValidator(val)
        self.watermark = ""
        self.lastDir = ""
        self.codeList = []
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
        self.connect(self.ui.tabWidget_2,  SIGNAL("currentChanged(int)"), self.tabChanged)
        self.connect(self.ui.rbUpperLeft,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.rbBottomLeft,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.rbUpperRight,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.rbBottomRight,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.rbScaled,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.rbTiled,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.rbCustom,  SIGNAL("clicked()"),  self.updateWatermarkPreview)
        self.connect(self.ui.watermarkX,  SIGNAL("textChanged(QString)"),  self.updateWatermarkPreview)
        self.connect(self.ui.watermarkY,  SIGNAL("textChanged(QString)"),  self.updateWatermarkPreview)
        self.connect(self.ui.spinOpacity,  SIGNAL("valueChanged(double)"),  self.updateWatermarkPreview)
        
        self.connect(self.ui.spinImg,  SIGNAL("valueChanged(int)"),  self.updateList)
        
    def toggleCoverFlow(self):
        if USE_COVERFLOW:
            if self.ui.btnCoverFlow.isChecked():
                self.coverFlow.show()
                self.ui.imgList.hide()
            else:
                self.coverFlow.hide()
                self.ui.imgList.show()
    
    def tabChanged(self, index):
        if index == 1: #watermark tab
            self.updateWatermarkPreview()
    
    def deleteImages(self):
        res = QMessageBox.question(self,  "Warning", "Are you sure you want to delete these images?", QMessageBox.Ok |QMessageBox.Cancel)
        
        if res == QMessageBox.Ok:
            for i in xrange(0, self.ui.imgList.count()):
                os.remove(str(self.ui.imgList.item(i).text()))
            self.ui.imgList.clear()
            if USE_COVERFLOW:
                self.coverFlow.clear()
            
    def addFolderClicked(self):
        fDir = QFileDialog.getExistingDirectory(self, "Select Directory", self.lastDir)
        filters = QStringList()
        for f in ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tif", "*.tiff"]:
            filters.append(f)
        iList = QDir(fDir).entryInfoList(filters)

        for f in iList:
            im = self.image(f.filePath()).copy()
            ico = QIcon(QPixmap.fromImage(im))
            QListWidgetItem(ico, f.filePath(), self.ui.imgList)
            if USE_COVERFLOW:
                self.addCoverFlowItem(f)

        if fDir:
            self.lastDir = fDir
        
    def resizeEvent(self, event):
        if self.ui.tabWidget_2.currentIndex() == 1: #watermark tab
            self.updateWatermarkPreview()
    
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
                    im = self.image(fn).copy()
                    ico = QIcon(QPixmap.fromImage(im))
                    QListWidgetItem(ico,  fn,  self.ui.imgList)
                    if USE_COVERFLOW:
                        self.addCoverFlowItem(QFileInfo(fn))
        
    def loadSettings(self):
        if self.settings.contains("defaultsite"):
            self.ui.comboSite.setCurrentIndex(self.ui.comboSite.findText(self.settings.value("defaultsite").toString()))
        
        self.lastDir = self.settings.value("lastDir").toString()
        self.ui.spinImg.setValue(self.settings.value("numImg", QVariant(4)).toInt()[0])
        if USE_COVERFLOW:
            self.ui.btnCoverFlow.setChecked(self.settings.value("coverFlow", QVariant(False)).toBool())
            self.toggleCoverFlow()
        
        self.settings.beginGroup("watermark")
        self.watermark = self.settings.value("file").toString()
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
        self.settings.setValue("lastDir", QVariant(self.lastDir))
        self.settings.setValue("numImg", QVariant(self.ui.spinImg.value()))
        if USE_COVERFLOW:
            self.settings.setValue("coverFlow", QVariant(self.ui.btnCoverFlow.isChecked()))
        
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
        ls = QFileDialog.getOpenFileNames(self, "Select images to upload", 
                                           self.lastDir,
                                           "Images (*.png *.jpg *.jpeg *.gif *.bmp *.tif *.tiff);; All *.*")
        for l in ls:
            im = self.image(l).copy()
            ico = QIcon(QPixmap.fromImage(im))
            QListWidgetItem(ico, l, self.ui.imgList)
            if USE_COVERFLOW:
                self.addCoverFlowItem(QFileInfo(l))
            self.lastDir = QFileInfo(l).absolutePath()
        
    def removeClicked(self):
        if self.ui.btnCoverFlow.isChecked():
            cfi = self.coverFlow.at(self.coverFlow.selected())
            lIt = self.ui.imgList.findItems(cfi.title(), Qt.MatchExactly)
            if len(lIt):
                i = self.ui.imgList.takeItem(self.ui.imgList.row(lIt[0]))
                del i
                self.coverFlow.remove(cfi)
        else:
            item = self.ui.imgList.takeItem(self.ui.imgList.currentRow())
            if USE_COVERFLOW:
                for k in xrange(0, self.coverFlow.size()):
                    if self.coverFlow.at(k).title() == item.text():
                        del item
                        self.coverFlow.remove(k)
                        break
            
    def uploadClicked(self):
        self.uploadList = []
        self.codeList = []
        for i in xrange(0, self.ui.imgList.count()):
            self.uploadList.append(self.ui.imgList.item(i).text())
        self.ui.pbTotal.setMaximum(self.ui.imgList.count())
        self.ui.pbTotal.setValue(0)
        self.upload()
        
    def upload(self, code=None):
        if code:
            self.codeList += [str(code)]
            self.updateList()
                
        if not len(self.uploadList):
            return
        
        self.ui.pbTotal.setValue(self.ui.pbTotal.value()+1)
        self.ui.lblTotal.setText("Uploading %d of %d"%(self.ui.pbTotal.value(),  self.ui.pbTotal.maximum()))
        it = self.uploadList.pop(0)
        if self.watermark:
            w = self.doWatermark(it)     
            it = os.path.join(tempfile.tempdir, str(QFileInfo(it).fileName()))
            w.save(it)
        self.site[str(self.ui.comboSite.currentText())].upload(it)

    def updateList(self,  value=None):
        self.ui.textBBCode.clear()
        i = 0
        for code in self.codeList:
            self.ui.textBBCode.setText(self.ui.textBBCode.toPlainText()+code)
            if i == self.ui.spinImg.value()-1:
                self.ui.textBBCode.setText(self.ui.textBBCode.toPlainText()+"\n")
                i = 0
            else:
                i += 1
        
    def addWatermark(self):
        if not self.watermark:
            last = self.lastDir
        else:
            last = QFileInfo(self.watermark).absolutePath()

        f = QFileDialog.getOpenFileName(self, "Select watermark", 
                                         last,
                                         "Images (*.png *.jpg *.jpeg *.gif *.bmp *.tif *.tiff);; All *.*")
        self.watermark = f
        self.updateWatermarkPreview()
            
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
        return w
    
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
        
    def updateWatermarkPreview(self, *args,  **kwargs):
        if self.ui.imgList.count() == 0 and self.watermark:
            self.ui.displayWatermark.setPixmap(QPixmap.fromImage(self.image(self.watermark)))
        elif not self.watermark:
            return
        else:
            w = ImageQt(self.doWatermark(self.ui.imgList.item(0).text()))
            w = w.scaled(self.ui.displayWatermark.size())
            self.ui.displayWatermark.setPixmap(QPixmap.fromImage(w))
        
        
    def addCoverFlowItem(self, fileInfo):
        if USE_COVERFLOW:
            item = QLCoverFlowItem(self.image(fileInfo.absoluteFilePath()).scaledToWidth(200, Qt.SmoothTransformation))
            item.setTitle(fileInfo.absoluteFilePath())
            item.setComment(str(fileInfo.size()/1024)+"K")
            self.coverFlow.add(item)
    
    def image(self, path):
        im = QImage()
        try:
            im = ImageQt(path)
        except:
            im = QImage(path)
        return im
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ImageUploader()
    mw.show()
    sys.exit(app.exec_())
