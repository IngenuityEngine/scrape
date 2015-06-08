var os = require('os')
var _ = require('lodash')
var express = require('express')
var app = express()
var http = require('http').Server(app)

var port = 3000
var IPs = ''


// allow CORS
// var allowCrossDomain = function(req, res, next)
// {
// 	res.header('Access-Control-Allow-Origin','*')
// 	res.header('Access-Control-Allow-Credentials', true)
// 	res.header('Access-Control-Allow-Methods',
// 		'POST, GET, PUT, DELETE, OPTIONS')
// 	res.header('Access-Control-Allow-Headers','Content-Type')
// 	next()
// }
// app.use(allowCrossDomain)

// serve public files
app.use(express.static(__dirname + '/public'))

// app.get('/:name', function(req, res)
// {
// 	var options = {
// 		root: __dirname,
// 		dotfiles: 'deny',
// 		headers: {
// 				'x-timestamp': Date.now(),
// 				'x-sent': true,
// 				'Access-Control-Allow-Origin': '*',
// 		}
// 	}

// 	var filename = req.params.name
// 	res.sendFile(filename, options, function (err)
// 	{
// 		if (err)
// 		{
// 			console.log(err)
// 			res.status(err.status).end()
// 		}
// 		else
// 		{
// 			console.log('Sent:', filename)
// 		}
// 	})

// })

http.listen(port, function()
{
	console.log('\n\nServer listening at:\n')

	// loop through the networkInterfaces and list
	// each IPv4 that we find
	var prefix
	_.each(os.networkInterfaces(), function(i)
	{
		_.each(i, function(entry)
		{
			if (entry.family == 'IPv4')
			{
				prefix = entry.internal ? '(internal)' : '(external)'
				console.log(prefix + ' http://' +
					entry.address + ':' +
					port)
				if (!entry.internal)
					IPs += '<li>' + entry.address + '</li>\n'
			}
		})
	})
	IPs = IPs.slice(0, -1)
})
