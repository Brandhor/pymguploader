from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
import urllib2
from BeautifulSoup import BeautifulSoup

class Turboimagehost(QObject):
    def __init__(self, parent):
        super(Turboimagehost, self).__init__(parent)
        self.nm = QNetworkAccessManager(parent)
        self.rep = None
        self.server = None
        
        self.connect(self.nm, SIGNAL("finished(QNetworkReply*)"),
                     self.httpRequestFinished)
    
    def upload(self, path):
        if not self.server:
            u = urllib2.urlopen("http://www.turboimagehost.com/")
            r = u.read()
            u.close()
            s = BeautifulSoup(r)
            self.server = s.find(id="form2").get("action")
        

        self.html = QString()
        url = QUrl(self.server)
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", str(url.host()));
        req.setRawHeader("User-Agent" ,"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"imcontent\"\r\n")
        bytes.append("\r\n")
        bytes.append("all\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"privacy\"\r\n")
        bytes.append("\r\n")
        bytes.append("private\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"thumb_size\"\r\n")
        bytes.append("\r\n")
        bytes.append("3\r\n")


        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images[]\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
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
        QMessageBox.error(None, "Turboimagehost",
                                          "Upload failed: %s." % self.rep.errorString())
    
    def readHttp(self):
        self.html += self.rep.readAll()
        
    def cancelUpload(self):
        self.httpRequestAborted = True
        self.rep.abort()
        
    def httpRequestFinished(self, reply):
        if self.httpRequestAborted:
            return            

        s = BeautifulSoup(str(self.html))
        code = s.findAll("input", {"class":"codes"})[1].get("value")
        self.emit(SIGNAL("done(QString)"), code)

    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)
    
    def __str__(self):
        return "Turboimagehost.com"
    
