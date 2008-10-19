from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
import urllib2
import urllib
import random
from BeautifulSoup import BeautifulSoup

class Tinypic(QObject):
    def __init__(self, parent):
        super(Tinypic, self).__init__(parent)
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
        f = urllib2.urlopen("http://tinypic.com/")
        r = f.read()
        f.close()
        s = BeautifulSoup(r)
        uid = s.find("input", {"name":"UPLOAD_IDENTIFIER"}).get("value")
        upk = s.find("input", {"name":"upk"}).get("value")
        lang = s.find("input", {"name":"domain_lang"}).get("value")
        maxs = s.find("input", {"name":"MAX_FILE_SIZE"}).get("value")

        self.html = QString()
        n = random.randint(1, 4)
        url = QUrl("http://s%s.tinypic.com/upload.php"%n)
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        if url.port() != -1:
            self.http.setHost(url.host(), url.port())
        else:
            self.http.setHost(url.host(), 80)
        if  not url.userName().isEmpty():
            self.http.setUser(url.userName(), url.password())
    
        header = QHttpRequestHeader("POST",  "/upload.php",  1,  1)
        header.setValue("Host", "s%s.tinypic.com"%n)
        header.setValue("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        header.setValue("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        header.setValue("Keep-Alive", "300");
        header.setValue("Connection", "keep-alive")
        header.setValue("Referer" ,"http://tinypic.com/")
        header.setValue("Content-type", "multipart/form-data; boundary=AaB03x")
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"action\"\r\n")
        bytes.append("\r\n")
        bytes.append("upload\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"UPLOAD_IDENTIFIER\"\r\n")
        bytes.append("\r\n")
        bytes.append("%s\r\n"%uid)

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upk\"\r\n")
        bytes.append("\r\n")
        bytes.append("%s\r\n"%upk)

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"domain_lang\"\r\n")
        bytes.append("\r\n")
        bytes.append("%s\r\n"%lang)

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"MAX_FILE_SIZE\"\r\n")
        bytes.append("\r\n")
        bytes.append("%s\r\n"%maxs)

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"file_type\"\r\n")
        bytes.append("\r\n")
        bytes.append("image\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"description\"\r\n")
        bytes.append("\r\n")
        bytes.append("\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"dimension\"\r\n")
        bytes.append("\r\n")
        bytes.append("1600\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"the_file\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
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
            QMessageBox.information(self, self.tr(self.__str__()),
                                          self.tr("Upload failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            s = BeautifulSoup(str(self.html))
            hh = s.findAll("input", {"type":"hidden"})
            hl = {}
            for h in hh:
                hl[h.get("name")] = h.get("value")

            uri = "http://tinypic.com/?t=postupload&%s" % urllib.urlencode(hl)
            f = urllib2.urlopen(uri)
            r = f.read()
            f.close()
            s = BeautifulSoup(r)

            thumb = s.find("div", {"class":"upload-actions"}).find("img", {"alt":"View Full Size Image"}).get("src")
            url = s.find("input", {"id":"direct-url"}).get("value")
            code = "[URL=\"%s\"][IMG]%s[/IMG][/URL]"%(url, thumb)
            self.emit(SIGNAL("done(QString)"), str(code))

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() != 200:
            QMessageBox.information(self, self.tr(self.__str__()),
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
        return "Tinypic"
    
