# -*- coding: utf-8 -*-
from base import *

class UploadgeekCom(BaseSite):
    def upload(self, path):
        self.html = ""
        url = QUrl("http://www.uploadgeek.com/upload.php")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)

        req = QNetworkRequest(url)

        req.setRawHeader("Host", "www.uploadgeek.com");
        req.setRawHeader("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        req.setRawHeader("Accept","text/xml,application/xhtml+xml,application/xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Accept-Language", "en-us,en;q=0.5")
        req.setRawHeader("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Referer", "http://www.uploadgeek.com/")
        req.setRawHeader("Content-type", "multipart/form-data; boundary=gc0p4Jq0M2Yt08jU534c0p");

        bytes = QByteArray()

        bytes.append("--gc0p4Jq0M2Yt08jU534c0p\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"typ\"\r\n")
        bytes.append("\r\n")
        bytes.append("s\r\n")
        bytes.append("--gc0p4Jq0M2Yt08jU534c0p\r\n")

        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"f_single\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        bytes.append("--gc0p4Jq0M2Yt08jU534c0p--")
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

        
        c = s.find("meta", {"http-equiv":"refresh"}).get("content")
        
        url = re.search("URL=http://www.uploadgeek.com(.*)", c).group(1)
        u = urllib2.urlopen("http://www.uploadgeek.com"+url)
        r = u.read()
        u.close()
        
        s = BeautifulSoup(r)
        code = s.find("input", {"class":"code_box"}).get("value")
        self.emit(SIGNAL("done(QString)"), code)

    def __str__(self):
        return "Uploadgeek.com"
