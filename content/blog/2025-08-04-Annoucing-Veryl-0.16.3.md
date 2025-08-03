+++
title = "Announcing Veryl 0.16.3"
+++

The Veryl team has published a new release of Veryl, 0.16.3.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Language Features

## Support omittable RHS value of proto param {{ pr(id="1778") }}

In proto modules, the right-hand side value of `param` / `const` is not necessary.
So it becomes to be omittable.

```veryl
proto module ModuleA #(
    param A: u32 = 0,
    param B: u32    , // RHS value can be omitted
);
```

## Support for loop in descending order {{ pr(id="1783") }}

`rev` keyword is introduced to indicate loop in descending order.

```veryl
for i: i32 in rev 0..32 {
}

// Generated SV
// for (int i = 32 - 1; i >= 0; i--) begin
// end
```

## Add `fmt(skip)` attribute {{ pr(id="1804") }}

`fmt(skip)` attribute is introduced to indicate the following block is not formatted by `veryl fmt`.
It can be added to module, interface and package.

```veryl
#[fmt(skip)]
module ModuleA {
}
```

# New Tool Features

## Incremental build support {{ pr(id="1823") }}

In large projects, `veryl build` sometimes takes a long time.
To accelarate such case, incremental build is introduced.
If incremental build is enabled, Veryl compiler traces the last modified time and generated time of files,
and re-generates only files related modified source code.

The reliability of tracing is not yet high, so incremental build is not enabled by default.
To enable it, you can specify in `Veryl.toml` like below:

```toml
[build]
incremental = true
```

# Other Changes

Check out everything that changed in [Release v0.16.3](https://github.com/veryl-lang/veryl/releases/tag/v0.16.3).
