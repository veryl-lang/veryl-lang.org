+++
title = "Announcing Verylup 0.1.8"
+++

The Veryl team has published a new release of Verylup, 0.1.8.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.8 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# Important Notice

Verylup 0.1.7 unexpectedly disabled the self-update feature by default. If you see the following message at `verylup update`, please update to Verylup 0.1.8 manually.

```
$ verylup update
...
[INFO ]  self-update is disabled
```

# New Features

## `VERYLUP_HOME` environment variable support

By default, verylup uses the data directory defined by [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/) to store Veryl toolchains.
This directory is defined every users, therefore it cannot be share by some users.

This behaviour causes a problem in cases like creating container image, in which the user installing Veryl and the actual user are different.
To resolve the issue, `VERYLUP_HOME` environment variable can be used.
If it is defined, verylup installs Veryl toolchains under the `VERYLUP_HOME` directory.


# Other Changes

Check out everything that changed in [Release v0.1.8](https://github.com/veryl-lang/verylup/releases/tag/v0.1.8).
