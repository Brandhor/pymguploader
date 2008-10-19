from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
from BeautifulSoup import BeautifulSoup

class Imagebam(QObject):
    def __init__(self, parent):
        super(Imagebam, self).__init__(parent)
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
        url = QUrl("http://www.imagebam.com/nav/save")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        if url.port() != -1:
            self.http.setHost(url.host(), url.port())
        else:
            self.http.setHost(url.host(), 80)
        if  not url.userName().isEmpty():
            self.http.setUser(url.userName(), url.password())
    
        header = QHttpRequestHeader("POST",  "/nav/save",  1,  1)
        header.setValue("Host", "www.imagebam.com");
        header.setValue("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        header.setValue("Keep-Alive", "300");
        header.setValue("Connection", "keep-alive");
        header.setValue("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"content_type\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"thumb_size\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"thumb_align\"\r\n")
        bytes.append("\r\n")
        bytes.append("1\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"makegallery\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"file[]\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
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
            QMessageBox.information(self.parent(), self.tr(self.__str__()),
                                          self.tr("Upload failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            s = BeautifulSoup(str(self.html))
            code = s.find("form").findAll("input")[1].get("value")
            self.emit(SIGNAL("done(QString)"), code)

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() == 302:
            self.httpRequestAborted = False
            self.httpGetId = self.http.get(responseHeader.value("Location"))
        elif responseHeader.statusCode() != 200:
            QMessageBox.information(self.parent(), self.tr(self.__str__()),
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
        return "Imagebam"
    
