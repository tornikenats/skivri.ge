const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: './skivrige/src/js/index.js',
    output: {
        path: path.resolve('skivrige/static/js'),
        filename: 'index_bundle.js'
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            use: [{
                loader: 'babel-loader',
                options: {
                    presets: [
                        'babel-preset-react'
                    ]
                }
            }]
        },
        {
            test: /\.scss$/,
            use: ExtractTextPlugin.extract({
                fallback: 'style-loader',
                use: ['css-loader', 'sass-loader']
            })
        }
        ]
    },
    resolve: {
        alias: {
            shared: path.resolve(__dirname, 'skivrige/src/js/shared/'),
        }

    },
    plugins: [
        new ExtractTextPlugin({
            filename: "../css/styles.css"
        }),
    ]
}