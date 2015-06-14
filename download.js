var async = require('async')
var _ = require('lodash')
var http = require('http-get')
var args = process.argv

console.log('args:', args)

var getFuncs = _.collect(_.range(2, args.length, 2), function(i)
{
	return function(cb)
	{
		var path = args[i]
		var name = process.cwd() + '/downloads/' + args[i+1]
		console.log('download:', path, 'to:', name)
		http.get(path, name,
		function(err)
		{
			if (err)
				console.log('err:', err)
			cb()
		})
	}
})

async.series(getFuncs, function()
{
	console.log('all done')
})
