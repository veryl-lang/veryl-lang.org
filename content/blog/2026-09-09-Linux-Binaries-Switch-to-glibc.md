+++
title = "Linux binaries switch from musl to glibc"
+++

The Linux release binaries of Veryl are now dynamically linked against glibc. They
used to be statically linked against musl. The asset names are unchanged,
`veryl-x86_64-linux.zip` and `veryl-aarch64-linux.zip`, only their contents differ,
and musl builds are no longer published.

This breaks compatibility for musl-only environments, so it is announced ahead of
the release that carries it: the nightly toolchain switches over first.

## Why

A statically linked binary carries no dynamic loader, so `dlopen` can never
succeed. Two features were therefore dead in the official binaries.

- **Native verification components.** [Components written in Rust](@/blog/2026-07-14-Verification-Components.md)
  declared under `[[components]]` could not be loaded at all. `veryl publish`
  reported "library does not export a veryl manifest", which blamed the component
  rather than the loader: the export was there, the library was never loaded.
- **The `cc` simulator backend.** `--backend cc`, the default where a C compiler is
  available, compiled the generated C and then failed to `dlopen` the result. It
  fell back to the Cranelift JIT silently, so users who never touched components
  were affected without any visible sign of it.

Both work as intended on glibc-based distributions from now on.

## Which glibc

The binaries need **glibc 2.17 or later**, which is the RHEL/CentOS 7 generation
and covers mainstream distributions in current use. An environment older than that
needs a build from source, and a statically linked one leaves the two features
above unavailable, just as the previous official binaries did.

## musl-only environments

Where there is no glibc, the official binaries no longer run:

- **Alpine and other musl-based images**: switch to a glibc-based image, or build
  from source.
- **NixOS**: set `programs.nix-ld.enable = true`, or use the veryl package from
  nixpkgs. With nix-ld enabled the official binaries run as they are, verification
  components and the `cc` backend included.

A static binary you build yourself still cannot use the two features, but it now
says so instead of failing obscurely: a component that fails to load reports the
real cause, and `veryl test` warns when it falls back from the `cc` backend for
this reason.

## Timing

The nightly toolchain switches over before the next stable release. `verylup`
downloads these same archives, so `verylup install nightly` gets the new binaries.
