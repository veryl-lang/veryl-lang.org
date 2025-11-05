+++
title = "Announcing Verylup 0.1.10"
+++

The Veryl team has published a new release of Verylup, 0.1.10.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.10 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## VersionReq syntax support

VersionReq syntax like `+0.16` instead of complete version `+0.16.0` can be used.
If `+0.16` is specified, the latest version in `0.16.x` is selected.

```
$ veryl +0.16.0 --version
veryl 0.16.0 (56a6056 2025-05-05)
$ veryl +0.16 --version
veryl 0.16.5 (617da3e 2025-10-06)
```

## aarch64-windows support

`aarch64-windows` platform support is added.

## Version check of nightly channel

Before this version, `verylup update` always downloaded nightly build.
Now version checking of nightly channel is added, and `verylup update` becomes faster when there is no update of nightly build.


```
$ verylup update
[INFO ]     checking toolchain: latest (up-to-date)
[INFO ]     checking toolchain: nightly (up-to-date)
[INFO ]     checking verylup: 0.1.10 (up-to-date)
```

# Other Changes

Check out everything that changed in [Release v0.1.10](https://github.com/veryl-lang/verylup/releases/tag/v0.1.10).
