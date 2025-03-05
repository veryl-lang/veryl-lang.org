+++
title = "Announcing Veryl 0.14.1"
+++

The Veryl team has published a new release of Veryl, 0.14.1.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Resolving Regressions

This version aims to resolve regressions introduced in the previous version.

* Fix broken msb  {{ pr(id="1329") }}

# New Features

## Improve port connection check {{ pr(id="1327") }}

Type cast at port connection caused reset type error, it is fixed correctly.

```veryl
inst u: $sv::SvModule (
    // v0.14.0: `sv_with_implicit_reset` error
    // v0.14.1: no error
    i_rst_n: i_rst as reset_async_low,
);
```

Connecting unassignable type to output port becomes to be detected.

```veryl
inst u: Module (
    out0: 1    , // error
    out1: x + 1, // error
);
```

# Other Changes

Check out everything that changed in [Release v0.14.1](https://github.com/veryl-lang/veryl/releases/tag/v0.14.1).
