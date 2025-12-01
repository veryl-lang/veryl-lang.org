+++
title = "Announcing Veryl 0.17.1"
+++

The Veryl team has published a new release of Veryl, 0.17.1.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Tool Features

## DSim runner {{ pr(id="2034") }}

[Altair DSim](https://altair.com/dsim) support for `veryl test` is added.

```
$ veryl test --sim dsim
```

## `vertical_align` format option {{ pr(id="2065") }}

By default, `veryl fmt` formats with keeping vertial alignment like below.

```
let a : logic    = 1;
let aa: logic<2> = 1;
```

However, this causes unexpected differences by revision control systems like git.

```
let a  : logic    = 1; // not changed logically, but diff occurs
let aa : logic<2> = 1; // not changed logically, but diff occurs
let aaa: logic<2> = 1;
```

To prevent this behaviour, you can use `vertical_align` option.

```toml
[format]
vertical_align = false
```

# New Standard Library

## Basic synchronizer implementation {{ pr(id="2036") }}

The default implementation of `std::synchronizer`, which uses single-bit FF scheme, is added.

[https://std.veryl-lang.org/synchronizer_basic.html](https://std.veryl-lang.org/synchronizer_basic.html)

# Other Changes

Check out everything that changed in [Release v0.17.1](https://github.com/veryl-lang/veryl/releases/tag/v0.17.1).
