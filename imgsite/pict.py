# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
from BeautifulSoup import BeautifulSoup

class Pict(QObject):
    def __init__(self, parent):
        super(Pict, self).__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.reply = None

        self.connect(self.manager, SIGNAL("finished(QNetworkReply*)"), self.httpRequestFinished)

    def upload(self, path):
        self.html = QString()
        url = QUrl("http://www.pict.com/api/upload/")
        request = QNetworkRequest(url)
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        if url.port() != -1:
            self.http.setHost(url.host(), url.port())
        else:
            self.http.setHost(url.host(), 80)
        if  not url.userName().isEmpty():
            self.http.setUser(url.userName(), url.password())
    
        header = QHttpRequestHeader("POST",  "/api/upload/",  1,  1)
        header.setValue("Host", "www.pict.com");
        header.setValue("User-Agent" ,"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5");
        header.setValue("Accept","text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        header.setValue("Keep-Alive", "300");
        header.setValue("Connection", "keep-alive");
        header.setValue("Content-type", "multipart/form-data; boundary=AaB03x");
        
        
        
        bytes = QByteArray()
        bytes.append("--AaB03x\r\n")
        bytes.append("Content-Disposition: ")
        bytes.append("form-data; name=\"Filedata\"; filename=\"" + QByteArray(QFileInfo(path).fileName().toUtf8()) + "\"\r\n")
        bytes.append("Content-Type: %s\r\n"%mimetypes.guess_type(str(path))[0])
        bytes.append("\r\n")
        bytes.append(fp.readAll())
        fp.close()
        bytes.append("\r\n")
        bytes.append("--AaB03x--")
        contentLength = bytes.length()
        request.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(contentLength))

        self.reply = self.manager.post(request, bytes)

        self.connect(self.reply, SIGNAL("uploadProgress(qint64, qint64)"), self.updateDataSendProgress)
        self.connect(self.reply, SIGNAL("readyRead()"), self.readHttp)
        self.connect(self.reply, SIGNAL("error(QNetworkReply::NetworkError)"), self.error)

        self.httpRequestAborted = False
        self.parent().ui.lblPartial.setText("Uploading %s."%path)

    def readHttp(self):
        self.html += self.reply.readAll()

    def cancelUpload(self):
        self.httpRequestAborted = True
        self.reply.abort()

        if requestId != self.httpGetId:
            return
    
        if error:
            QMessageBox.information(self, self.tr("Pict.com"),
                                          self.tr("Upload failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            s = BeautifulSoup(str(self.html))
            url = s.find("copy", type="original").find("link", type="directLink").next.next
            thumb = re.sub("/(?!.*/.*)", "/300/", url)
            code = "[URL=\"%s\"][IMG]%s[/IMG][/URL]"%(url, thumb)
            self.emit(SIGNAL("done(QString)"), str(code))

    def httpRequestFinished(self, reply):
        if self.httpRequestAborted:
            return

        s = BeautifulSoup(str(self.html))
        url = s.find("copy", type="original").find("link", type="boardLink").next.next
        self.emit(SIGNAL("done(QString)"), str(url))
        self.reply.deleteLater()

    def updateDataSendProgress(self, done, total):
        if self.httpRequestAborted:
            return
        self.parent().ui.pbPartial.setMaximum(total)
        self.parent().ui.pbPartial.setValue(done)

    def __str__(self):
        return "Pict.com"
