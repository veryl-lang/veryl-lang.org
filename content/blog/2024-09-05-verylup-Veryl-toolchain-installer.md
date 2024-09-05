+++
title = "verylup: Veryl toolchain installer"
+++

verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

# Installation

There are two installation ways. In either case, executing `verylup setup` is required after installing.

## Download binary

Download from [release page](https://github.com/veryl-lang/verylup/releases/latest), and extract to the directory in `PATH`.

## Cargo

You can install with [cargo](https://crates.io/crates/verylup).

```
cargo install verylup
```

# Usage

`verylup` can be used like below:

```
// Setup verylup (only once at first)
verylup setup

// Update the latest toolchain
verylup update

// Install a specific toolchain
verylup install 0.12.0

// Show installed toolchains
verylup show
```

After installing `verylup`, verion specifier by `+` can be used in `veryl` command like below: 

```
// Use the latest toolchain
veryl build

// Use a specific toolchain
veryl +0.12.0 build
veryl +latest build
```

# For Veryl Developer

For Veryl developer, a special toolchain target `local` is prepared.
If `verylup install local` is executed in your local Veryl repository, the built toolchain is installed as `local` toolchain.
`local` becomes the default toolchain if it exists.

```
// Build and install the toolchain from local Veryl repository
verylup install local

// Use the built toolchain
veryl build

// Use the latest toolchain
veryl +latest build
```
