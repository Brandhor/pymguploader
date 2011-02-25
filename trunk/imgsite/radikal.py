from base import *

class Radikal(BaseSite):
    def upload(self, path):
        self.html = QString()
        url = QUrl("http://www.radikal.ru/action.aspx")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", "radikal.ru");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upload\"\r\n")
        bytes.append("\r\n")
        bytes.append("yes\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"VM\"\r\n")
        bytes.append("\r\n")
        bytes.append("300\r\n")

        """
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"GEO_POINT_ID\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"GEO_LINK\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"GEO_NOT_PRIVATE\"\r\n")
        bytes.append("\r\n")
        bytes.append("1\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"hmode4params\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"O\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"M\"\r\n")
        bytes.append("\r\n")
        bytes.append("640\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"IM\"\r\n")
        bytes.append("\r\n")
        bytes.append("7\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"R\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"JQ\"\r\n")
        bytes.append("\r\n")
        bytes.append("85\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"J\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"N\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"RE\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"VE\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"V\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"XE\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"X\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"FS\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"user_url\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"VE\"\r\n")
        bytes.append("\r\n")
        bytes.append("0\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"alb_id\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"input_comment\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"URLF\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")
        """
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"F\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
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

    def httpRequestFinished(self, reply):
        if self.httpRequestAborted:
            return

        s = BeautifulSoup(unicode(self.html, "utf-8"))
        img = s.find("input", {"id":"input_link_1"}).get("value")
        thumb = s.find("input", {"id":"input_link_3"}).get("value")
        
        code = re.sub("URL=(.*?)\]\[", "URL=%s]["%img, thumb)

        self.emit(SIGNAL("done(QString)"), code)
  
    def __str__(self):
        return "radikal.ru"
    
