+++
title = "Official Docker image drops Alpine and Bullseye variants"
+++

Starting with Veryl 0.22.0, the [official Docker image](https://hub.docker.com/r/veryllang/veryl)
is no longer published in its Alpine and Debian Bullseye variants. The last images
of those variants are for Veryl 0.21.0, and they will not be updated.

## Removed variants

- **Alpine** (`alpine`, `alpine3.20`, `alpine3.21`, `alpine3.22`, and the
  versioned tags such as `0.21.0-alpine`): the Linux release binaries
  [switched from musl to glibc](@/blog/2026-09-09-Linux-Binaries-Switch-to-glibc.md),
  and musl builds are no longer published. Alpine is musl-based, so the official
  binaries do not run on it.
- **Bullseye** (`bullseye`, `slim-bullseye`, and the versioned tags such as
  `0.21.0-bullseye`): Debian 11 has [reached the end of its long term support](https://www.debian.org/News/2026/20260831)
  on August 31, 2026.

## Migration

If you use an Alpine tag, switch to a slim tag. `slim` is the closest replacement
for `alpine` as a small base image:

```
FROM veryllang/veryl:slim
```

If you use a Bullseye tag, switch to the corresponding Trixie or Bookworm tag:
`bullseye` to `trixie` or `bookworm`, and `slim-bullseye` to `slim` or
`slim-bookworm`.

If you pin a version, for example `0.21.0-alpine`, the image keeps working as it
is, but newer versions are only available in the Trixie and Bookworm variants.
