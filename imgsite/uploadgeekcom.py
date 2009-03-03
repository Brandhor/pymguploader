# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import mimetypes
import re
from BeautifulSoup import BeautifulSoup

class UploadgeekCom(QObject):
    def __init__(self, parent):
        super(UploadgeekCom, self).__init__(parent)
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
        self.html = ""
        url = QUrl("http://www.uploadgeek.com/upload.php")
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)

        if url.port() != -1:
            self.http.setHost(url.host(), url.port())
        else:
            self.http.setHost(url.host(), 80)
        if not url.userName().isEmpty():
            self.http.setUser(url.userName(), url.password())

        header = QHttpRequestHeader("POST",  "/upload.php",  1,  1)
        header.setValue("Host", "www.uploadgeek.com");
        header.setValue("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        header.setValue("Accept","text/xml,application/xhtml+xml,application/xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");
        header.setValue("Accept-Language", "en-us,en;q=0.5")
        header.setValue("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
        header.setValue("Keep-Alive", "300");
        header.setValue("Connection", "keep-alive");
        header.setValue("Referer", "http://www.uploadgeek.com/")
        header.setValue("Content-type", "multipart/form-data; boundary=gc0p4Jq0M2Yt08jU534c0p");

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
            QMessageBox.information(self.parent(), self.tr("Uploadgeek.com"),
                                          self.tr("Upload failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            s = BeautifulSoup(str(self.html))

            c = None
            try:
                c = s.find("meta", {"http-equiv":"refresh"}).get("content")
            except:
                pass

            if c:
                url = re.search("URL=http://www.uploadgeek.com(.*)", c).group(1)
                self.html = ""
                self.httpGetId = self.http.get(url)
            else:
                code = s.find("input", {"class":"code_box"}).get("value")
                self.emit(SIGNAL("done(QString)"), code)

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() == 302:
            self.httpRequestAborted = False
            self.httpGetId = self.http.get(responseHeader.value("Location"))
        elif responseHeader.statusCode() != 200:
            QMessageBox.information(self.parent(), self.tr("Uploadgeek.com"),
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
        return "Uploadgeek.com"
