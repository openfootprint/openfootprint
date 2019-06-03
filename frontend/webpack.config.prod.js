var config = require("./webpack.config");
var BundleTracker = require('webpack-bundle-tracker');
var VueLoaderPlugin = require('vue-loader/lib/plugin')

config = Object.assign(config, {
  "mode": "production",
  "output": {
    filename: "[name]-[hash].js",
    path: "/app/frontend/webpack/prod/"
  },
  "plugins": [
    new VueLoaderPlugin(),
    new BundleTracker({filename: './webpack/prod/stats.json'})
  ],

});

module.exports = config;