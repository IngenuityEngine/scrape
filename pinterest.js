
// var _ = require('lodash')
// var async = require('async')
var page = require('webpage').create()
page.viewportSize = {
  width: 1024,
  height: 640
}

var pins
var step = 1

function renderStep()
{
	page.render('/debug/step' + step + '.png')
	step += 1
}
function boardPageLoaded()
{
	renderStep()
	page.injectJs('jquery2.js')
	pins = page.evaluate(function()
	{
		var $ = window.$
		var pins = []
		$('.pinUiImage').parents('a').each(function()
		{
			pins.push($(this).attr('href'))
		})
		return pins
	})
	console.log(pins)

	console.log('all done')
}
function formSubmitted()
{
	renderStep()
	console.log('form submitted')
	page.open('https://www.pinterest.com/blented/characters-low-fi/',
	boardPageLoaded)
}


page.open('https://www.pinterest.com/login',
function(status)
{
	console.log('Status:', status)
	if (page.injectJs('jquery2.js'))
	{
		console.log('Were in')
		renderStep()
		page.evaluate(function()
		{
			var $ = window.$
			$('input[type=email]').val('blented@gmail.com')
			$('input[type=password]').val('pinterest325266')
			$('button[type=submit]').click()
		})
		renderStep()
		console.log('form submitted')
		setTimeout(formSubmitted, 5000)
	}
	else
	{
		console.log('failed')
	}
})

// pin urls
// $('.pinUiImage').parents('a').attr('src')

// image source on the pin details page
// $('.pinImageSourceWrapper img').attr('src')
