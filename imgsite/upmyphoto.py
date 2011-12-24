from base import *

class Upmyphoto(BaseSite):    
    def upload(self, path):
        self.html = QString()
        url = QUrl("http://upmyphoto.com/upload")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", "upmyphoto.com");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Referer", "http://upmyphoto.com")
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images0\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"names0\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images1\"; filename=\"\"\r\n")
        bytes.append("Content-Type: application/octet-stream\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"names1\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images2\"; filename=\"\"\r\n")
        bytes.append("Content-Type: application/octet-stream\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"names2\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images3\"; filename=\"\"\r\n")
        bytes.append("Content-Type: application/octet-stream\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"names3\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images4\"; filename=\"\"\r\n")
        bytes.append("Content-Type: application/octet-stream\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"names4\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"images5\"; filename=\"\"\r\n")
        bytes.append("Content-Type: application/octet-stream\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"names5\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upload\"\r\n")
        bytes.append("\r\n")
        bytes.append("Upload Images\r\n")
        
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
        
    def httpRequestFinished(self, reply):
        if self.httpRequestAborted:
            return            

        s = BeautifulSoup(str(self.html))
        code = s.find("div", {"id":"content"}).findAll("input", {"class":"urlinput"})[2].get("value").strip()

        self.emit(SIGNAL("done(QString)"), code)

    def __str__(self):
        return "Upmyphoto.com"
    
