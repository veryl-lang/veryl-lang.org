+++
title = "Announcing Verylup 0.1.13"
+++

The Veryl team has published a new release of Verylup, 0.1.13.
Verylup is the official toolchain installer of Veryl.
It installs the latest Veryl toolchain and eases to update and switch the toolchains.

If you have a previous version of Verylup installed, getting Verylup 0.1.13 is as easy as stopping any programs which may be using Verylup (e.g. closing your IDE) and running:

```
verylup update
```

If you don't have it already, please refer [Getting Started](https://doc.veryl-lang.org/book/03_getting_started/01_installation.html).

# Security Update

## Update rustls-webpki for RUSTSEC-2026-0382

This release updates `rustls-webpki`, which Verylup uses to verify TLS certificates when downloading toolchains, to 0.103.16.
Earlier versions could accept certificate chains through distrusted eMudhra (emSign) intermediate certificates whose private keys are publicly known.
See [RUSTSEC-2026-0382](https://rustsec.org/advisories/RUSTSEC-2026-0382.html) for details.

We recommend all users to update to Verylup 0.1.13.

# New Features

## Download retry for temporary errors

Downloads are now retried up to 3 times with exponential backoff when a request fails or the server returns a 5xx error.
This makes `verylup install` and `verylup update` more robust against temporary network or server problems.

## Check the installed toolchain can be executed

After installing a toolchain, Verylup now checks that the installed `veryl` can actually be executed.
If it can't, the installation is reported as an error instead of succeeding silently.
On hosts where the released binaries can't run, a hint is shown, for example:

* On NixOS, nixpkgs' `veryl` or `programs.nix-ld.enable` is required.
* On Linux without the glibc loader (e.g. musl-based distributions), the missing loader path is shown.

# Other Changes

Check out everything that changed in [Release v0.1.13](https://github.com/veryl-lang/verylup/releases/tag/v0.1.13).
