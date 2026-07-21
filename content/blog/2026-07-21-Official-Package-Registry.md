+++
title = "Official package registry"
+++

We have launched the official Veryl package registry at
[registry.veryl-lang.org](https://registry.veryl-lang.org/). It is a place to
discover published Veryl packages and browse their generated documentation.

Veryl dependencies have always been plain git references, and that does not
change. The registry does not host code or become a new place to fetch it from.
It is an index over public git repositories, plus documentation generated from
each package's source. Resolving a dependency still pulls straight from GitHub,
GitLab, or wherever the package lives, exactly as before. The registry is what
makes those packages discoverable.

## Finding and using a package

Packages are grouped into categories such as Processor, Peripheral, Memory,
Verification, and Tooling, so you can browse by the kind of IP you are looking
for. Each package has a page with its description, license, latest version, and
auto-generated documentation.

Every page also shows the line to drop into your `Veryl.toml`. For
[`veryl-lang/vip`](https://github.com/veryl-lang/vip), a set of AXI
[verification components](@/blog/2026-07-14-Verification-Components.md), that is:

```toml
[dependencies]
vip = { github = "veryl-lang/vip", version = "0.1.0" }
```

That is the same dependency you would have written by hand; the registry just
saves you from hunting for the repository and the current version.

## Registering your own package

Registration is opt-in and tied to publishing. First, point `[project]
repository` at your package's git URL:

```toml
[project]
name       = "my_ip"
version    = "0.1.0"
repository = "https://example.com/you/my_ip"
```

Then `veryl publish` will offer to register the project the first time. You can
make the choice permanent in `Veryl.toml` so you are never prompted again:

```toml
[publish]
register = true   # or false to never register
```

To register a project that is already published, without bumping a version, run:

```console
$ veryl register
```

A few things worth knowing:

- GitHub, GitLab, Codeberg, and other hosts are all accepted.
- The registry refreshes on a periodic crawl, so a newly registered package or
  version can take a little while to appear.
- Registration failures never fail a publish, and nothing about depending on or
  building a package requires the registry.

## Availability

The registry is live now, and you can browse it today. The `veryl publish` and
`veryl register` integration described above arrives in the next release, and it
is already available on the nightly toolchain via `verylup install nightly`.
