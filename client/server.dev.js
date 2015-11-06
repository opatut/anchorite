var WebpackDevServer = require('webpack-dev-server');
var webpack = require('webpack');

var config = require('./webpack.config.js');

config.entry.unshift('webpack-dev-server/client?http://localhost:5001', 'webpack/hot/dev-server');

var compiler = webpack(config);

var server = new WebpackDevServer(compiler, {
	hot: true,
	publicPath: config.output.publicPath,
	colors: true,
	progress: true,
	headers: { 'Access-Control-Allow-Origin': '*' }
});

server.listen(5001);
