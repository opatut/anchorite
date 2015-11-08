var path = require('path');
var webpack = require('webpack');

var dev = process.env.NODE_ENV === 'development';

module.exports = {
	devtool: 'source-map',
	entry: [
		'regenerator/runtime.js',
		'./src/index.jsx',
	],
	output: {
		path: path.join(__dirname, '..', 'server', 'anchorite', 'static'),
		filename: 'bundle.js',
		publicPath: dev ? 'http://localhost:5001/static/' : '/static/',
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				loaders: ['react-hot', 'babel?stage=0&optional[]=runtime'],
				include: [path.join(__dirname, 'src')],
				exclude: /node_modules/,
			},
			{
				test: /\.s?css$/,
				loader: "style!css!sass",
				include: [path.join(__dirname, 'styles')]
			},
			{
				test: /\.json$/,
				loader: "json"
			},
			{
				test: /\.(woff2?|svg|eot|ttf|png)$/,
				loader: 'file'
			},
		],
	},
	plugins: [
		new webpack.HotModuleReplacementPlugin(),
		new webpack.NoErrorsPlugin(),
	],
	resolve: {
		extensions: ['', '.js', '.jsx'],
		alias: {
			'fetch': 'isomorphic-fetch',
		},
	},
};
