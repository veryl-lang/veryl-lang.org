+++
title = "Announcing Verylup 0.1.5"
+++

The Veryl team has published a new release of Verylup, 0.1.5.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.5 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## Nightly channel

To use the latest features easily, nightly channel is added.
Nightly channel is built daily from the master branch.

```
verylup install nightly
```

By default, nightly channel is not enabled after installation.
So the following ways can be used to enable it.


```
# Use +nightly
veryl +nightly build

# Set default to nightly
verylup default nightly

# Override by nightly for a specific project
verylup override set nightly
```

# Other Changes

Check out everything that changed in [Release v0.1.5](https://github.com/veryl-lang/verylup/releases/tag/v0.1.5).
