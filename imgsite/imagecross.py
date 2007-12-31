from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re

class Imagecross(QObject):
    def __init__(self, parent):
        super(Imagecross, self).__init__(parent)
        self.http = QHttp(parent)
        
        self.connect(self.http, SIGNAL("requestFinished(int, bool)"),
                     self.httpRequestFinished)
        self.connect(self.http, SIGNAL("dataSendProgress(int, int)"),
                     self.updateDataSendProgress)
        self.connect(self.http, SIGNAL("responseHeaderReceived(QHttpResponseHeader)"),
                     self.readResponseHeader)
        self.connect(self.http, SIGNAL("readyRead(QHttpResponseHeader)"), 
                     self.readHttp)
    
    def upload(self, path):
        self.html = QString()
        url = QUrl("http://hosting03.imagecross.com/basic.php")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        if url.port() != -1:
            self.http.setHost(url.host(), url.port())
        else:
            self.http.setHost(url.host(), 80)
        if  not url.userName().isEmpty():
            self.http.setUser(url.userName(), url.password())
    
        header = QHttpRequestHeader("POST",  "/basic.php",  1,  1)
        header.setValue("Host", "hosting03.imagecross.com");
        header.setValue("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        header.setValue("Keep-Alive", "300");
        header.setValue("Connection", "keep-alive");
        header.setValue("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"userfile\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        bytes.append("--AaB03x--")
        contentLength = bytes.length()
        header.setContentLength(contentLength)
    
    
        self.httpRequestAborted = False
        self.httpGetId = self.http.request(header, bytes)
        self.parent().ui.lblPartial.setText("Uploading %s."%path)
    
    
    def readHttp(self,  responseHeader):
        self.html += self.http.readAll()
        
    def cancelUpload(self):
        self.httpRequestAborted = True
        self.http.abort()
        
    def httpRequestFinished(self, requestId, error):
        if self.httpRequestAborted:
            return

        if requestId != self.httpGetId:
            return
    
        if error:
            QMessageBox.information(self, self.tr("Imagecross"),
                                          self.tr("Upload failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            code = re.search(r"myspace-image-upload-viewer-(?P<char>.)\.php\?id=(?P<id>.*)\"><img", self.html.toUtf8())
            code = "[URL=\"http://www.imagecross.com/myspace-image-upload-viewer-%s.php?id=%s\"][IMG]http://hosting03.imagecross.com/myspace-image-upload-thumbs-%s/%s[/IMG][/URL]"%(code.group(1), code.group(2), code.group(1), code.group(2))
            self.emit(SIGNAL("done(QString)"), code)

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() != 200:
            QMessageBox.information(self, self.tr("Imagecross"),
                                          self.tr("Upload failed: %1.")
                                          .arg(responseHeader.reasonPhrase()))
            self.httpRequestAborted = True
            self.http.abort()
            return

    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)
    
    def __str__(self):
        return "Imagecross"
    
