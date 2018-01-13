const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');


module.exports = {
    entry: './src/js/index.js',
    output: {
        path: path.resolve('public'),
        filename: 'index.js'
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
            shared: 'src/js/shared',
        }

    },
    plugins: [
        new ExtractTextPlugin({
            filename: "styles.css"
        }),
        new HtmlWebpackPlugin({
            title: 'სკივრი',
            template: 'src/template.html'
        }),
        new CopyWebpackPlugin([
            { from: 'src/images', to: 'images' },
            { from: 'src/fonts', to: 'fonts' }
        ]),
    ]
}