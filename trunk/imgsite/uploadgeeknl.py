# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
from BeautifulSoup import BeautifulSoup

class UploadgeekNl(QObject):
    def __init__(self, parent):
        super(UploadgeekNl, self).__init__(parent)
        self.nm = QNetworkAccessManager(parent)
        self.rep = None

        self.connect(self.nm, SIGNAL("finished(QNetworkReply*)"),
                     self.httpRequestFinished)

    def upload(self, path):
        self.html = ""
        url = QUrl("http://www.uploadgeek.nl/upload.php")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)

        req = QNetworkRequest(url)

        req.setRawHeader("Host", "www.uploadgeek.nl");
        req.setRawHeader("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        req.setRawHeader("Keep-Alive", "300");
        req.setRawHeader("Connection", "keep-alive");
        req.setRawHeader("Content-type", "multipart/form-data; boundary=AaB03x");

        bytes = QByteArray()

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"upload_type\"\r\n")
        bytes.append("\r\n")
        bytes.append("standard\r\n")
        
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"private_upload\"\r\n")
        bytes.append("\r\n")
        bytes.append("1\r\n")

        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"userfile[]\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
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
        QMessageBox.information(None, self.__str__(),
                                          "Upload failed: %s." % self.rep.errorString())        
    def readHttp(self):
        self.html += self.rep.readAll()

    def cancelUpload(self):
        self.httpRequestAborted = True
        self.rep.abort()

    def httpRequestFinished(self, reply):
        if self.httpRequestAborted:
            return


        body = re.search("</head>(.*)</html>", str(self.html), re.DOTALL).group(1)
        s = BeautifulSoup(body)
        url = s.find("table").find("input").get("value")
        thumb = re.sub("\.(\w*)$", "_thumb.\\1", url)
        code = "[URL=\"%s\"][IMG]%s[/IMG][/URL]"%(url, thumb)
        self.emit(SIGNAL("done(QString)"), str(code))


    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)

    def __str__(self):
        return "Uploadgeek.nl"
