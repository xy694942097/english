# TOAST UI Editor vendor files

`editor-bundle.js` bundles `@toast-ui/editor` 3.2.2 and its npm dependencies for the local browser. The CSS and `zh-cn.js` come from the same npm package. Copyright and MIT terms are in `LICENSE` (the upstream repository's license).

The package's `dist/toastui-editor.js` has external module dependencies, so it cannot be used alone as a browser script. The browser bundle was built with esbuild 0.25.12 using this entry:

```js
import Editor from '@toast-ui/editor';
window.toastui = { Editor };
```

Build command after installing those two packages in a temporary directory:

```sh
esbuild entry.js --bundle --minify --platform=browser --format=iife --outfile=editor-bundle.js
```

The upstream repository was archived in September 2026. Keep the editor local-only and retest Markdown round trips before changing its version.
