
import os
import sys
import urllib

from PySide import QtGui
from PySide import QtCore
from PySide import QtWebKit



class Scraper(QtCore.QObject):

	exportDir = ''

	def __init__(self, parent=None):
		super(Scraper, self).__init__(parent)

	def setExportDir(self, exportDir):
		self.exportDir = exportDir

	def getSavePath(self, name):
		return os.path.join(self.exportDir, name) + '.jpg'

	@QtCore.Slot(str)
	def log(self, text):
		print text

	@QtCore.Slot()
	def collectPinUrls(self):
		self.parent().collectPinUrls()

	@QtCore.Slot(str, str)
	def download(self, path, name):
		savePath = self.getSavePath(name)
		print 'Downloading:', path, 'to:', savePath
		# only download stuff that doesn't already exist
		if not os.path.isfile(savePath):
			urllib.urlretrieve(path, savePath)

		self.parent().downloadPins()

	@QtCore.Slot(str)
	def setPinUrls(self, pinUrls):
		self.parent().setPinUrls(pinUrls.split(';'))

class Browser(QtGui.QDialog):

	pinUrls = []

	def __init__(self, parent=None):
		super(Browser, self).__init__(parent)
		gridLayout = QtGui.QGridLayout()
		row = 0

		widget = QtGui.QLabel('Page:')
		widget.setAlignment(QtCore.Qt.AlignRight)
		gridLayout.addWidget(widget, row, 0)
		self.pageEdit = QtGui.QLineEdit('https://www.pinterest.com/blented/weapons-sci-fi/')
		gridLayout.addWidget(self.pageEdit, row, 1)
		row += 1

		widget = QtGui.QPushButton('Load Page')
		widget.clicked.connect(self.loadPage)
		gridLayout.addWidget(widget, row, 0, 1, 2)
		row += 1

		widget = QtGui.QPushButton('Inject injectJQuery')
		widget.clicked.connect(self.injectJQuery)
		gridLayout.addWidget(widget, row, 0, 1, 2)
		row += 1

		widget = QtGui.QPushButton('Scroll Page')
		widget.clicked.connect(self.scrollPage)
		gridLayout.addWidget(widget, row, 0, 1, 2)
		row += 1

		widget = QtGui.QLabel('Export Directory:')
		widget.setAlignment(QtCore.Qt.AlignRight)
		gridLayout.addWidget(widget, row, 0)
		self.exportDir = QtGui.QLineEdit('c:/google drive/reference/pinterest/weapons-sci-fi/')
		gridLayout.addWidget(self.exportDir, row, 1)
		row += 1

		self.downloadButton = QtGui.QPushButton('Download Pins')
		self.downloadButton.clicked.connect(self.startPinDownload)
		gridLayout.addWidget(self.downloadButton, row, 0, 1, 2)
		row += 1

		self.webView = QtWebKit.QWebView()
		self.webView.loadFinished.connect(self.pageLoad)
		gridLayout.addWidget(self.webView, row, 0, 1, 2)

		self.scraper = Scraper(self)
		self.webView.resize(960, 540)

		self.setLayout(gridLayout)

	def loadPage(self, page=None):
		if not page:
			page = self.pageEdit.text()
		print 'Loading:', page
		self.webView.load(QtCore.QUrl(page))

	def injectJQuery(self):
		self.runJavascript('''
		var element1 = document.createElement("script");
		element1.src = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js";
		document.getElementsByTagName("head")[0].appendChild(element1);
		''')

	def scrollPage(self):
		self.runJavascript('''
		var scroller = {
			scrollTries: 0,
			currentHeight: 0,
			scrollPage: function()
			{
				scraper.log('Scrolling');
				scroller.currentHeight += 1000;
				$(document).scrollTop(scroller.currentHeight);
				if (scroller.currentHeight > $(document).height())
				{
					if (scroller.scrollTries < 3)
					{
						scroller.scrollTries += 1;
						$(document).scrollTop(scroller.currentHeight - 1000);
					}
					else
					{
						alert('Done scrolling');
						return;
					}
				}
				scraper.collectPinUrls();
				// wait between 1 and 3 seconds
				setTimeout(scroller.scrollPage, Math.random()*2000+100);
			}
		};scroller.scrollPage()''')

	def collectPinUrls(self):
		self.runJavascript('''
		(function collectPinUrls()
		{
			var pinUrls = [];
			var pins = $('.pinUiImage').parents('a');
			pins.each(function()
			{
				pinUrls.push($(this).attr('href'));
			})
			scraper.setPinUrls(pinUrls.join(';'));
		})();''')

	def setPinUrls(self, pinUrls):
		print 'Adding', len(pinUrls), 'pins'
		self.pinUrls += pinUrls
		self.pinUrls = list(set(self.pinUrls))
		self.downloadButton.setText('Download ' + str(len(self.pinUrls)) + ' pins')

	def startPinDownload(self):
		exportDir = self.exportDir.text()
		self.scraper.setExportDir(exportDir)
		try:
			os.makedirs(exportDir)
		except OSError:
			if not os.path.isdir(exportDir):
				raise

		self.downloadPins()

	def downloadPins(self):
		print 'Pins remaining:', len(self.pinUrls)
		if not len(self.pinUrls):
			return

		# don't download pins that we've already downloaded
		url = 'https://www.pinterest.com' + self.pinUrls.pop()
		pinID = url[30:-1]
		if os.path.isfile(self.scraper.getSavePath(pinID)):
			return self.downloadPins()

		self.loadPage(url)

	def pageLoad(self):
		print 'Page Loaded'
		self.downloadPin()

	def downloadPin(self):
		# this will error and do nothing if we're not on a pin page
		self.runJavascript('''
		path = document.querySelector('.pinImageSourceWrapper img').src;
		name = window.location.href.slice(30,-1);
		scraper.download(path, name);
		''')


	def runJavascript(self, javascript):
		frame = self.webView.page().mainFrame()
		frame.addToJavaScriptWindowObject('scraper', self.scraper)
		frame.evaluateJavaScript(javascript)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Browser()
	ex.show()
	app.exec_()

if __name__ == '__main__':
	main()
