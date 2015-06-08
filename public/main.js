
var $ = window.$
var _ = window._

$(document).ready(function()
{
	console.log('Page ready to go')
})

var helpers = {

getTarget: function(event)
{
	return $(event.target ||
				event.currentTarget ||
				event.relatedTarget ||
				event.toElement)
},
getName: function(elem)
{
	return elem.prop('tagName').toLowerCase() + '.' +
		elem.prop('class') + '\n'
}

}

$("#site").load(function()
{
	console.log('Site ready to go')
	var iframeDoc = $('body iframe').contents()

	function captureClicks(event)
	{
		event.preventDefault()
		event.stopPropagation()

		console.log('click')
		var target = helpers.getTarget(event)
		var name = ''
		var parents = target.parentsUntil('body')
		parents.each(function()
		{
			name = helpers.getName($(this)) + name
		})
		$('#target').val(name)
	}

	// recursively bind clicks
	function bindClicks(elements)
	{
		iframeDoc.find('*')
			.off('click mousedown touchstart')
			.on('click', captureClicks)
		iframeDoc.find('a')
			.off('click mousedown touchstart')
			.on('click', captureClicks)

		return
		if (elements.children().length)
			bindClicks(elements.children())

		elements
			.off('click mousedown touchstart')
			.on('click', captureClicks)
	}
	function continuousClickCatcher()
	{
		console.log('got yo clicks')
		bindClicks(iframeDoc)
		setTimeout(continuousClickCatcher, 2000)
	}
	continuousClickCatcher()
})

