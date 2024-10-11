+++
title = "Announcing Verylup 0.1.3"
+++

The Veryl team has published a new release of Verylup, 0.1.3.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.3 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## Offline installation support

Verylup 0.1.3 supports offline installation for environments without internet access.
The procedure of offline installation is below:

* Download the latest toolchain package from [Veryl release page](https://github.com/veryl-lang/veryl/releases).
* Execute `veryl setup` with `--pkg` specification like the following command.

```
verylup setup --offline --pkg veryl-x86_64-linux.zip
```

If you want to update/install toolchain, `--pkg` specification is required as the same as setup.
