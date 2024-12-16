+++
title = "Announcing Verylup 0.1.4"
+++

The Veryl team has published a new release of Verylup, 0.1.4.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.4 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## Add config subcommand

Now `config` subcommand is added.
Through the command, you can show the current configuration and change the value.

```
verylup config show
verylup config set offline true
```

## Show the latest toolchain version

`verylup show` shows the latest toolchain version like below:

```
$ verylup show
installed toolchains
--------------------

latest: 0.13.3 (default)
```

# Other Changes

Check out everything that changed in [Release v0.1.4](https://github.com/veryl-lang/verylup/releases/tag/v0.1.4).
