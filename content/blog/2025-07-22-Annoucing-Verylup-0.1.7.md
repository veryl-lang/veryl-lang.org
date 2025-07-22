+++
title = "Announcing Verylup 0.1.7"
+++

The Veryl team has published a new release of Verylup, 0.1.7.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.7 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# New Features

## Add `--no-self-update` option and `no-self-update` feature support

If users don't have write permission for the verylup binary, various commands of verylup are failed.
For example, installing verylup through Linux distribution's packaging system causes this issue.

To avoid this issue, the two option is provided.
`--no-self-update` option can be used at `verylup setup`.
This option disables self-update of verylup for users who executed `verylup setup`.
This is for users who don't prefer self-update feature.

```
verylup setup --no-self-update
```

`no-self-update` feature can be used at `cargo build` or `cargo install`.
This feature permanently disables self-update.
This is for Linux distribution's packaging.

```
cargo build --release --features no-self-update
cargo install verylup --features no-self-update
```

# Other Changes

Check out everything that changed in [Release v0.1.7](https://github.com/veryl-lang/verylup/releases/tag/v0.1.7).
