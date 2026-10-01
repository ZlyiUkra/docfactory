# @vitejs/plugin-basic-ssl README 1.0.0 … 1.0.2: @vitejs/plugin-basic-ssl [![npm](https://img.shields.io/npm/v/@vitejs/plugin-basic-ssl.svg)](https://npmjs.com/package/@vitejs/plugin-basic-ssl)
# джерело: https://raw.githubusercontent.com/vitejs/vite-plugin-basic-ssl/v1.0.2/README.md
# отримано: 2026-10-01
# версія: 1.0.2, 1.0.1, 1.0.0

A plugin to generate untrusted certificates which still allows to access the page after proceeding a wall with warning.

In most scenarios, it is recommended to generate a secure trusted certificate instead and use it to configure `server.https`

## Usage

```js
// vite.config.js
import basicSsl from '@vitejs/plugin-basic-ssl'

export default {
  plugins: [
    basicSsl()
  ]
}
```

## License

MIT
