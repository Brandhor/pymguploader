from base import *

class SimplestImHost(BaseSite):    
    def upload(self, path):
        self.html = QString()
        url = QUrl("http://api.simplest-image-hosting.net/upload:image,default")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
    
        req.setRawHeader("Host", "api.simplest-image-hosting.net")
        req.setRawHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; rv:2.0b7pre) Gecko/20100926 Firefox/4.0b7pre")
        
        req.setRawHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        req.setRawHeader("Accept-Language", "en-us,en;q=0.5")
        req.setRawHeader("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
        req.setRawHeader("Keep-Alive", "115")
        req.setRawHeader("Connection", "keep-alive")
        req.setRawHeader("Content-type", "multipart/form-data;boundary=777690000022206660123")        
        req.setRawHeader("Pragma", "no-cache")
        req.setRawHeader("Cache-Control", "no-cache")
        
        
        bytes = QByteArray()

        bytes.append("\r\n--777690000022206660123\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data;name=\"fileName\";filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        bytes.append("--777690000022206660123--\r\n")
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

        url = str(re.search("800\\n(http://.+)\\n", self.html).group(1))
        
        u = urllib2.urlopen(url)
        r = u.read()
        u.close()

        s = BeautifulSoup(r)
        img = s.find("img").get("src")
        r = re.search("(.*)/.*/(.*)", img)
        thumb = r.group(1)+"/thumbnail/"+r.group(2)        

        code = "[URL=\"%s\"][IMG]%s[/IMG][/URL]"%(img, thumb)
        self.emit(SIGNAL("done(QString)"), code)
    
    def __str__(self):
        return "simplest-image-hosting.net"
    
