from base import *

class Bitevox(BaseSite):
    def upload(self, path):
        self.html = QString()
        url = QUrl("http://www.bitevox.com/upload.php")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", "bitevox.com");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"imgurl\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"filename[]\"\r\n")
        bytes.append("\r\n")
        bytes.append("%s\r\n"%QByteArray(QFileInfo(path).fileName().toUtf8()))
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"file[]\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"alt[]\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"private[0]\"\r\n")
        bytes.append("\r\n")
        bytes.append("1\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"shorturl[0]\"\r\n")
        bytes.append("\r\n")
        bytes.append("1\r\n")

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
            
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute).toInt()[0]
        
        if statusCode == 302:
            req = QNetworkRequest(QUrl(reply.header(QNetworkRequest.LocationHeader).toString()))
            self.rep = self.nm.get(req)
        
            self.connect(self.rep, SIGNAL("uploadProgress(qint64, qint64)"),
                         self.updateDataSendProgress)
            self.connect(self.rep, SIGNAL("readyRead()"),
                         self.readHttp)
            self.connect(self.rep, SIGNAL("error(QNetworkReply::NetworkError)"),
                         self.error)
            
        else:
            s = BeautifulSoup(unicode(self.html, "utf-8"))
            thumb = s.find("a", {"id":"fancybox"}).find("img").get("src")

            img = s.find("input", {"id":"codedirect"}).get("value")
            

            code = "[URL=\"%s\"][IMG]%s[/IMG][/URL]"%(img, thumb)
            self.emit(SIGNAL("done(QString)"), code)
  
    def __str__(self):
        return "Bitevox"
    
