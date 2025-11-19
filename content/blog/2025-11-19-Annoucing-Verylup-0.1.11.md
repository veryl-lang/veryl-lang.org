+++
title = "Announcing Verylup 0.1.11"
+++

The Veryl team has published a new release of Verylup, 0.1.11.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.11 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## Custom CA bundle support for downloads

In environments behind a proxy that re-signs HTTPS traffic with an enterprise root CA, custom CA bundle support is necessary.
verylup becomes to load a custom CA bundle through `SSL_CERT_FILE` environment variable or OS-dependent CA stores.


# Other Changes

Check out everything that changed in [Release v0.1.11](https://github.com/veryl-lang/verylup/releases/tag/v0.1.11).
