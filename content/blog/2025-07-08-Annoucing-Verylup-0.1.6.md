+++
title = "Announcing Verylup 0.1.6"
+++

The Veryl team has published a new release of Verylup, 0.1.6.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.6 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## Add proxy support 

Verylup supports HTTP/SOCKS5 proxy.
By default, verylup refers system proxy configuration via the following environment variables:

* `HTTPS_PROXY` / `https_proxy`
* `ALL_PROXY` / `all_proxy`

If you want to specify proxy for verylup only, the following command can be used.

```
verylup config set proxy socks5://127.0.0.1:1086
```

## Add aarch64-linux support

Now verylup supports aarch64-linux. The supported platforms are below:

* x86_64-linux
* x86_64-mac
* x86_64-windows
* aarch64-linux
* aarch64-mac

# Other Changes

Check out everything that changed in [Release v0.1.6](https://github.com/veryl-lang/verylup/releases/tag/v0.1.6).
