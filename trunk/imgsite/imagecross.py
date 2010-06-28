# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
from BeautifulSoup import BeautifulSoup
import urllib2

class Imagecross(QObject):
    def __init__(self, parent):
        super(Imagecross, self).__init__(parent)
        self.http = QHttp(parent)

        self.connect(self.http, SIGNAL("requestFinished(int, bool)"),
                     self.httpRequestFinished)
        self.connect(self.http, SIGNAL("dataSendProgress(int, int)"),
                     self.updateDataSendProgress)
        self.connect(self.http, SIGNAL("responseHeaderReceived(QHttpResponseHeader)"),
                     self.readResponseHeader)
        self.connect(self.http, SIGNAL("readyRead(QHttpResponseHeader)"), 
                     self.readHttp)

        u = urllib2.urlopen("http://www.imagecross.com")
        r = u.read()
        s = BeautifulSoup(r)
        self.url = QUrl(s.find("form", {"name":"uploadform"}).get("action"))

    def upload(self, path):
        self.html = ""
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)

        if self.url.port() != -1:
            self.http.setHost(self.url.host(), self.url.port())
        else:
            self.http.setHost(self.url.host(), 80)
        if  not self.url.userName().isEmpty():
            self.http.setUser(self.url.userName(), self.url.password())

        print self.url
        header = QHttpRequestHeader("POST",  "/basicg.php",  1,  1)
        header.setValue("Host", self.url.host());
        header.setValue("User-Agent" ,"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5");
        header.setValue("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        header.setValue("Keep-Alive", "300");
        header.setValue("Connection", "keep-alive");
        header.setValue("Referer", "http://www.imagecross.com/private.php")

        header.setValue("Content-type", "multipart/form-data; boundary=AaB03x");

        bytes = QByteArray()

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"userfile\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upload\"\r\n")
        bytes.append("\r\n")
        bytes.append("Uploading...\r\n")
        
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
            QMessageBox.information(self, self.tr("Imagecross"),
                                          self.tr("Upload failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            f = open("cross.html", "w")
            f.write(str(self.html))
            f.close()
            self.html = str(self.html).replace("</h6<", "</h6>")
            s = BeautifulSoup(self.html)
            s = BeautifulSoup(s.find("table").find("input").get("value"))
            url = s.find("img").get("src")
            code = "[URL=\"%s\"][IMG]%s[/IMG][/URL]"%(url, url.replace("image-hosting-", "image-hosting-th-"))
            self.emit(SIGNAL("done(QString)"), code)

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() != 200:
            print responseHeader.statusCode()
            QMessageBox.information(None, "Imagecross",
                                          "Upload failed: %s."%responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.http.abort()
            return

    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)

    def __str__(self):
        return "Imagecross"

