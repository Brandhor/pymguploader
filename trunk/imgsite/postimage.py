from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
import urllib2
from BeautifulSoup import BeautifulSoup

class Postimage(QObject):
    def __init__(self, parent):
        super(Postimage, self).__init__(parent)
        self.nm = QNetworkAccessManager(parent)
        self.rep = None
        
        self.connect(self.nm, SIGNAL("finished(QNetworkReply*)"),
                     self.httpRequestFinished)
    
    def upload(self, path):
        u = urllib2.urlopen("http://www.postimage.org/index.php?sid=Pq")
        r = u.read()
        u.close()
        s = BeautifulSoup(r)
        
        hash = s.find("input", {"name":"hash"}).get("value")
        
        self.html = QString()
        url = QUrl("http://www.postimage.org/index.php?sid=Pq")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", str(url.host()));
        req.setRawHeader("User-Agent" ,"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Referer", "http://www.postimage.org")
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"mode\"\r\n")
        bytes.append("\r\n")
        bytes.append("local\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"forumurl\"\r\n")
        bytes.append("\r\n")
        bytes.append("http://www.postimage.org/\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"lang\"\r\n")
        bytes.append("\r\n")
        bytes.append("english\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"tpl\"\r\n")
        bytes.append("\r\n")
        bytes.append(".\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"ver\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"addform\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"mforum\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"um\"\r\n")
        bytes.append("\r\n")
        bytes.append("image\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"adult\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"MAX_FILE_SIZE\"\r\n")
        bytes.append("\r\n")
        bytes.append("10485760\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"adult\"\r\n")
        bytes.append("\r\n")
        bytes.append("no\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"hash\"\r\n")
        bytes.append("\r\n")
        bytes.append("%s\r\n" % hash)
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"optsize\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"submit\"\r\n")
        bytes.append("\r\n")
        bytes.append("Upload It!\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upload\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
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
            
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute).toInt()[0]
        
        if statusCode == 302:
            u = urllib2.urlopen(str(reply.header(QNetworkRequest.LocationHeader).toString()))
            r = u.read()
            u.close()

            s = BeautifulSoup(r)
            code = s.findAll("input", {"type":"text"})[0].get("value")
            self.emit(SIGNAL("done(QString)"), code)

    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)
    
    def __str__(self):
        return "Postimage.org"
    
