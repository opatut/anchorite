var path = require('path');
var webpack = require('webpack');

module.exports = {
	devtool: 'cheap-module-eval-source-map',
	entry: [
		'regenerator/runtime.js',
		'./src/index.jsx',
	],
	output: {
		path: path.join(__dirname, 'dist'),
		filename: 'bundle.js',
		publicPath: 'http://localhost:5001/static/',
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				loaders: ['react-hot', 'babel?presets[]=es2015&presets[]=stage-0&presets[]=react'],
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
				test: /(^static|\.(woff2?|svg|eot|ttf)$)/,
				loader: 'file'
			},

			// fontawesome
			{
				test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "url?limit=10000&minetype=application/font-woff"
			},
			{   test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "file"
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
