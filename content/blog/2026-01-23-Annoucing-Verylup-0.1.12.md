+++
title = "Announcing Verylup 0.1.12"
+++

The Veryl team has published a new release of Verylup, 0.1.12.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.12 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# Important Notice

## `verylup install nightly` failure

From Verylup 0.1.10 to 0.1.11, `verylup install nightly` fails like below if the nightly installation is the first time.

```
$ verylup install nightly
Error: No such file or directory (os error 2)
```

Please update to Verylup 0.1.12 if you encountered this issue.

# Other Changes

Check out everything that changed in [Release v0.1.12](https://github.com/veryl-lang/verylup/releases/tag/v0.1.12).
