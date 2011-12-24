from base import *
import os
import urllib
import json

class Minus(BaseSite):
    EDITOR_ID = ""
    def upload(self, path):
        if not self.EDITOR_ID:
            r = urllib2.urlopen("http://min.us/api/CreateGallery", "")
            js = json.loads(r.read())
            self.EDITOR_ID = js["editor_id"]
        
        
        print self.EDITOR_ID
        self.html = QString()
        fname = os.path.basename(str(path))
        self.extension = os.path.splitext(str(path))[1]
        par = urllib.urlencode({"filename":fname, "key":"OK", "editor_id":self.EDITOR_ID})
        url = QUrl("http://min.us/api/UploadItem?"+par)
        fp = QFile(path)
        fp.open(QIODevice.ReadOnly)
        
        req = QNetworkRequest(url)
        
        bytes = QByteArray()
        bytes.append(fp.readAll())
        fp.close()
    
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

        js = json.loads(str(self.html))
        
        
        img = "http://i.min.us/i%s%s"%(js["id"], self.extension)
        thumb = "http://i.min.us/j%s%s"%(js["id"], self.extension)
        code = "<a href=\"%s\"><img width=400 src=\"%s\" /></a>"%(img, thumb)

        self.emit(SIGNAL("done(QString)"), code)

    def __str__(self):
        return "Min.us"
    
