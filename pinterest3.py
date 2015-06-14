
import os
import re
import sys
import urllib

from PySide import QtGui
from PySide import QtCore
from PySide import QtWebKit

class Scraper(QtCore.QObject):

	def __init__(self, parent=None):
		super(Scraper, self).__init__(parent)

	@QtCore.Slot(str)
	def log(self, text):
		print text

	@QtCore.Slot()
	def collectPinUrls(self):
		self.parent().collectPinUrls()

	@QtCore.Slot()
	def doneScrolling(self):
		print 'Done scrolling!'
		self.parent().downloadPins()

	@QtCore.Slot(str)
	def setPinUrls(self, pinUrls):
		self.parent().setPinUrls(pinUrls.split(';'))

class Browser(QtGui.QDialog):

	pinUrls = []
	scrollingEnabled = False
	exportDir = ''
	boardIndex = 0
	boardUrls = ['https://www.pinterest.com/blented/interior-design/',
'https://www.pinterest.com/blented/future-tech/',
'https://www.pinterest.com/blented/ui/',
'https://www.pinterest.com/blented/weapons-fantasy/',
'https://www.pinterest.com/blented/anatomy/',
'https://www.pinterest.com/blented/props-sci-fi/',
'https://www.pinterest.com/blented/details-sci-fi/',
'https://www.pinterest.com/blented/vehicles-low-fi/',
'https://www.pinterest.com/blented/robots/',
'https://www.pinterest.com/blented/clothing-mens/',
'https://www.pinterest.com/blented/characters-low-fi/',
'https://www.pinterest.com/blented/web-design/',
'https://www.pinterest.com/blented/machinery/',
'https://www.pinterest.com/blented/creatures/',
'https://www.pinterest.com/blented/weapons-sci-fi/',
'https://www.pinterest.com/blented/art-tutorials/',
'https://www.pinterest.com/blented/environments/',
'https://www.pinterest.com/blented/art-style/',
'https://www.pinterest.com/blented/interiors-sci-fi/',
'https://www.pinterest.com/blented/cities-sci-fi/',
'https://www.pinterest.com/blented/vehicles-sci-fi/',
'https://www.pinterest.com/blented/cities-fantasy/',
'https://www.pinterest.com/blented/cities-low-fi/',
'https://www.pinterest.com/blented/characters-futuristic/',
'https://www.pinterest.com/blented/design/',
'https://www.pinterest.com/blented/nature/',
'https://www.pinterest.com/blented/concept-art/']

	def __init__(self, parent=None):
		super(Browser, self).__init__(parent)
		gridLayout = QtGui.QGridLayout()
		row = 0

		widget = QtGui.QLabel('Page:')
		widget.setAlignment(QtCore.Qt.AlignRight)
		gridLayout.addWidget(widget, row, 0)
		self.pageEdit = QtGui.QLineEdit('https://www.pinterest.com/login')
		gridLayout.addWidget(self.pageEdit, row, 1)
		row += 1

		widget = QtGui.QPushButton('Load Page')
		widget.clicked.connect(self.loadPage)
		gridLayout.addWidget(widget, row, 0, 1, 2)
		row += 1

		# widget = QtGui.QPushButton('Inject injectJQuery')
		# widget.clicked.connect(self.injectJQuery)
		# gridLayout.addWidget(widget, row, 0, 1, 2)
		# row += 1

		# widget = QtGui.QPushButton('Scroll Page')
		# widget.clicked.connect(self.scrollPage)
		# gridLayout.addWidget(widget, row, 0, 1, 2)
		# row += 1

		widget = QtGui.QLabel('Export Directory:')
		widget.setAlignment(QtCore.Qt.AlignRight)
		gridLayout.addWidget(widget, row, 0)
		self.exportDirEdit = QtGui.QLineEdit('c:/google drive/reference/pinterest/')
		gridLayout.addWidget(self.exportDirEdit, row, 1)
		row += 1

		self.downloadButton = QtGui.QPushButton('Download Boards')
		self.downloadButton.clicked.connect(self.downloadBoards)
		gridLayout.addWidget(self.downloadButton, row, 0, 1, 2)
		row += 1

		self.webView = QtWebKit.QWebView()
		self.webView.loadFinished.connect(self.pageLoad)
		gridLayout.addWidget(self.webView, row, 0, 1, 2)

		self.scraper = Scraper(self)
		self.webView.resize(960, 540)

		self.setLayout(gridLayout)
		self.loadPage()

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
						scraper.doneScrolling()
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

	def downloadBoards(self):
		if self.boardIndex >= len(self.boardUrls):
			self.boardIndex = 0
			self.scrollingEnabled = False
			return

		self.scrollingEnabled = True
		boardUrl = self.boardUrls[self.boardIndex]
		self.pinUrls = []
		exportDir = os.path.join(self.exportDirEdit.text(), boardUrl.split('/')[-2])
		self.setExportDir(exportDir)
		try:
			os.makedirs(exportDir)
		except OSError:
			if not os.path.isdir(exportDir):
				raise

		self.boardIndex += 1
		self.loadPage(boardUrl)

	def downloadPins(self):
		for i, pin in enumerate(self.pinUrls):
			print 'Pins remaining:', (len(self.pinUrls) - i)

			# don't download pins that we've already downloaded
			url = 'https://www.pinterest.com' + pin
			pinID = url[30:-1]
			if os.path.isfile(self.getSavePath(pinID)):
				print pinID, 'already exists. Skipping download.'
				continue
			self.downloadPinImage(url)

		self.downloadBoards()

	def downloadPinImage(self, url):
		html = urllib.urlopen(url).read()
		loc = html.find('class="pinImage"')
		substr = html[loc-140:loc]
		imageUrl = re.findall('("https://s-media-cache-.+?")', substr)
		if not len(imageUrl):
			print 'Error downloading:', url
			return

		imageUrl = imageUrl[0][1:-1]
		self.download(imageUrl, url[30:-1])

	def setExportDir(self, exportDir):
		self.exportDir = exportDir

	def getSavePath(self, name):
		return os.path.join(self.exportDir, name) + '.jpg'

	def download(self, path, name):
		savePath = self.getSavePath(name)
		print 'Downloading:', path, 'to:', savePath
		# only download stuff that doesn't already exist
		if not os.path.isfile(savePath):
			urllib.urlretrieve(path, savePath)

	def pageLoad(self):
		print 'Page Loaded'
		if not self.scrollingEnabled:
			return
		self.injectJQuery()
		self.scrollPage()

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
