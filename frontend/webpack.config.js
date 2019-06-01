var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = {

  mode: 'development',

  context: '/frontend',
  entry: {
    "main": [
      //'webpack-dev-server/client?http://localhost:8001',
      // doesn't fall back to refresh
      //'webpack/hot/only-dev-server',
      //'webpack/hot/dev-server',
      '/frontend/scripts/entry',
    ]
  },

  output: {
      filename: "[name]-[hash].js",
      publicPath:"http://localhost:8001/"
  },

  devServer: {
    disableHostCheck: true,
    headers: {
      "Access-Control-Allow-Origin": "\*",
    },
    port:8001,
    //hot:true,
    host: '0.0.0.0'
  },


  // https://webpack.js.org/configuration/devtool/
  // devtool: 'inline-source-map',

  plugins: [
    //new webpack.HotModuleReplacementPlugin(),
    new VueLoaderPlugin(),
    //new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error

    new BundleTracker({filename: './webpack/local/stats.json'})
  ],

  module: {
    //loaders: [
      // we pass the output from babel loader to react-hot loader
      //{ test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel'], },
    //],

    // https://webpack.js.org/guides/typescript/
    /*rules: [
     {
       test: /\.tsx?$/,
       use: 'ts-loader',
       exclude: /node_modules/
     }
   ]*/
   rules: [
    {
      test: /\.js$/,
      exclude: /(node_modules|bower_components)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: [
            'env'
          ]
          // plugins: [require('babel-plugin-transform-object-rest-spread')]
        }
      }
    },
    {
      test: /\.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
      loader: 'file-loader?name=fonts/[name].[ext]'
    },
    {
      test: /\.vue$/,
      loader: 'vue-loader',
      options: {
        loaders: {
          js: 'babel-loader'
        }
      }
    },
    // https://github.com/webpack-contrib/sass-loader
    {
        test: /\.scss$/,
        use: [{
            loader: "style-loader" // creates style nodes from JS strings
        }, {
            loader: "css-loader" // translates CSS into CommonJS
        }, {
            loader: "sass-loader", // compiles Sass to CSS
/*
            options: {
                includePaths: ["openfootprint/static"]
            }
*/
        }]
    },
    {
      test: /\.css$/,
      use: [{
          loader: "style-loader" // creates style nodes from JS strings
      }, {
          loader: "css-loader" // translates CSS into CommonJS
      }]
    }
  ]
  },

  resolve: {
    //modulesDirectories: ['static/node_modules'],
    extensions: ['.js', '.jsx', ".vue", ".ts", ".tsx"],
    alias: {
      vue: 'vue/dist/vue.esm.js'
    }
  }
}