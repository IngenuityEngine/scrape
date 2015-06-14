
var element1 = document.createElement("script");
element1.src = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js";
document.getElementsByTagName("head")[0].appendChild(element1);

var $ = window.$
var scroller = {
	docHeight: 0,
	scrollTries: 0,
	scrollPage: function()
	{
		scraper.log('scrolling');
		scroller.currentHeight = $(document).height();
		$(document).scrollTop(scroller.currentHeight);
		if (scroller.docHeight == scroller.currentHeight)
		{
			if (scroller.scrollTries < 3)
			{
				scroller.scrollTries += 1;
			}
			else
			{
				alert('done scrolling');
				return;
			}
		}
		scroller.docHeight = scroller.currentHeight
		// wait between .5 and 1.5 seconds
		setTimeout(scroller.scrollPage, Math.random()*1500+500);
	}
};scroller.scrollPage()

(function collectPins()
{
	var pinURls = [];
	var iframeDoc = $('#site').contents();
	var pins = iframeDoc.find('.pinUiImage').parents('a');
	pins.each(function()
	{
		pinURls.push($(this).attr('href'));
	})
	scraper.setPins(pinURls);
})();

$(document).ready(function()
{
	console.log('Page ready to go')

	$('#loadPage').click(function()
	{
		$('#site').off('load').on('load', scrollPage)
		$('#site').src($('#webpage').val())
	})

	$('#collectPins').click(function()
	{
		$('#site').off('load').on('load', scrollPage)
		$('#site').src($('#webpage').val())
	})
})
