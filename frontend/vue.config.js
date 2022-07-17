module.exports = {
  devServer: {
    disableHostCheck: true,
    host: '0.0.0.0',
    port: 8081,
    proxy: {
      '/BananaService/': {
          target: 'http://localhost:8081',
      },
    }
  },
    configureWebpack: {
        module: {
            rules: [
                {
                    test: /\.txt$/i,
                    use: 'raw-loader',
                }
            ]
        }
    },
}
