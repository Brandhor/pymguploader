from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
import urllib2
from BeautifulSoup import BeautifulSoup

class Upmyphoto(QObject):
    def __init__(self, parent):
        super(Upmyphoto, self).__init__(parent)
        self.nm = QNetworkAccessManager(parent)
        self.rep = None
        
        self.connect(self.nm, SIGNAL("finished(QNetworkReply*)"),
                     self.httpRequestFinished)
    
    def upload(self, path):
        self.html = QString()
        url = QUrl("http://www.upmyphoto.com/upload.php")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", "www.upmyphoto.com");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Referer", "http://www.upmyphoto.com")
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"MAX_FILE_SIZE\"\r\n")
        bytes.append("\r\n")
        bytes.append("104857600\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"imgcontent\"\r\n")
        bytes.append("\r\n")
        bytes.append("safe\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"thumb_size\"\r\n")
        bytes.append("\r\n")
        bytes.append("180\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upload\"\r\n")
        bytes.append("\r\n")
        bytes.append("UPLOAD\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"image[]\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        bytes.append("--AaB03x--")
        contentLength = bytes.length()
        req.setRawHeader("Content-Length", "%s" % contentLength)
    
        self.rep = self.nm.post(req, bytes)
        
        self.connect(self.rep, SIGNAL("uploadProgress(qint64, qint64)"),
                     self.updateDataSendProgress)
        self.connect(self.rep, SIGNAL("readyRead()"),
                     self.readHttp)
        self.connect(self.rep, SIGNAL("error(QNetworkReply::NetworkError)"),
                     self.error)
    
        self.httpRequestAborted = False
        self.parent().ui.lblPartial.setText("Uploading %s."%path)
    
    def error(self, code):
        QMessageBox.error(None, self.__str__(),
                                          "Upload failed: %s." % self.rep.errorString())
    
    def readHttp(self):
        self.html += self.rep.readAll()
        
    def cancelUpload(self):
        self.httpRequestAborted = True
        self.rep.abort()
        
    def httpRequestFinished(self, reply):
        if self.httpRequestAborted:
            return            

        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute).toInt()[0]
        
        if statusCode == 302:
            u = urllib2.urlopen("http://upmyphoto.com/%s" % str(reply.rawHeader("location")))
            r = u.read()
            u.close()

            s = BeautifulSoup(r)
            code = s.findAll("textarea")[2].string.strip()

            self.emit(SIGNAL("done(QString)"), code)

    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)
    
    def __str__(self):
        return "Upmyphoto.com"
    
