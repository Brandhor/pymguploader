from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import sys
import re
os.popen("pyuic4 ui.ui -o ui.py").read()
import ui
import imgsite

class ImageUploader(QMainWindow):
    def __init__(self,  parent=None):
        super(ImageUploader, self).__init__(parent)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.counter = 0
        
        self.scanSite()
        self.connect(self.ui.btnAdd,  SIGNAL("clicked()"), self.addClicked)
        self.connect(self.ui.btnCancel, SIGNAL("clicked()"), self.cancelUpload)
        self.connect(self.ui.btnRemove,  SIGNAL("clicked()"), self.removeClicked)
        self.connect(self.ui.btnUpload,  SIGNAL("clicked()"), self.uploadClicked)
    
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
        self.uploadList = {}
        for i in xrange(0, self.ui.imgList.count()):
            self.uploadList[self.ui.imgList.item(i).text()] = self.site[str(self.ui.comboSite.currentText())]
        self.ui.pbTotal.setMaximum(self.ui.imgList.count())
        self.ui.pbTotal.setValue(0)
        self.upload()
        
    def upload(self,  code=None):
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
        it = self.uploadList.popitem()
        it[1].upload(it[0])

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ImageUploader()
    mw.show()
    sys.exit(app.exec_())
