+++
title = "Announcing Veryl 0.19.0"
+++

The Veryl team has published a new release of Veryl, 0.19.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Breaking Changes

To migrate some syntax changes, `veryl migrate` can be used:

<details>

```console
// Check how changes will be applied
$ veryl migrate --check

// Migrate
$ veryl migrate
```

</details>

## Report error for calling function which has references to variables defined after the call {{ pr(id="2240") }} {{ pr(id="2284") }}

The following code worked until Veryl 0.19.0, but these code sometimes caused false-positive warning/error.
To resolve this issue, Veryl 0.19.0 reports error for these code.


```veryl
always_comb {
    a = func(); // function call before `b` definition
}

var b: logic;
function func() -> logic {
    return b;
}
```

The following code is still valid, because `b` is defined before the function call.

```veryl
var b: logic;
always_comb {
    a = func(); // function call after `b` definition
}

function func() -> logic {
    return b;
}
```

# New Language Features

## Support inferable enum width {{ pr(id="2199") }}

The type of enum can be omitted like `enum A {}`, but in this case the base type of enum is fixed to `logic`.
We introduced a new syntax to specify the base type of enum like below.

```veryl
enum A: bit<_> {
   X,
   Y,
}

enum B: logic<_> {
   X,
   Y,
}
```

# New Standard Library

## Add interface definition of AXI stream as std library {{ pr(id="2208") }}

The interface definition of AXI stream is added.

[https://std.veryl-lang.org/axi4_stream_if.html](https://std.veryl-lang.org/axi4_stream_if.html)

# Other Changes

Check out everything that changed in [Release v0.19.0](https://github.com/veryl-lang/veryl/releases/tag/v0.19.0).
