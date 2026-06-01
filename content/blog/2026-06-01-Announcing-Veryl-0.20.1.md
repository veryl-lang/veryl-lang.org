+++
title = "Announcing Veryl 0.20.1"
+++

The Veryl team has published a new release of Veryl, 0.20.1.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Language Features

## Enum member import {{ pr(id="2599") }}

Enum members can now be imported via `import`, so they can be referenced without
the enclosing enum's namespace prefix.
This is particularly useful when an enum is used heavily inside a single scope.

```veryl
package PackageA {
    enum EnumA: logic<3> {
        A,
        B,
        C,
    }
}

module ModuleA (
    i_a: input  PackageA::EnumA,
    o_d: output logic         ,
) {
    import PackageA::EnumA::*;

    // Members can be referenced directly after `import`.
    assign o_d = inside i_a {A, B, C};
}
```

# New Tool Features

## Combinational loop detection {{ pr(id="2610") }}

The analyzer now reports combinational loops at compile time, including loops
that traverse function calls and submodule instances.
Catching these statically avoids relying on the downstream simulator or synthesis
tool to discover the cycle.

```veryl
module ModuleA (
    a: input  logic<8>,
    b: output logic<8>,
) {
    var c: logic<8>;
    assign b = c;
    assign c = b;   // error: combinational loop detected
}
```

## Wadler/Lindig based formatter {{ pr(id="2614") }}

The formatter has been rewritten on top of a Wadler/Lindig style pretty printer.
Line breaks are now decided by the target line width rather than purely by syntax,
so long expressions wrap into a readable shape instead of overflowing on a single
line.
The target width is configurable via `format.max_width` in `Veryl.toml`
(default: 120).

```veryl
// before
let a: logic<8> = aaaaaaaaaaaa + bbbbbbbbbbbb + cccccccccccc + dddddddddddd + eeeeeeeeeeee;

// after
let a: logic<8> =
    aaaaaaaaaaaa + bbbbbbbbbbbb + cccccccccccc + dddddddddddd
    + eeeeeeeeeeee;
```

In addition, several long-standing formatter bugs around `case` expressions and
related constructs have been fixed as part of the rewrite.

## C compiler backend for the native simulator {{ pr(id="2662") }}

The native simulator gains a new `cc` backend that emits C code and compiles it
with a system C compiler in the background, producing a more heavily optimized
binary than the existing Cranelift JIT path.
The simulation starts immediately on the Cranelift output and then transparently
switches over to the C-compiled binary once it is ready, combining low startup
latency with high steady-state throughput.

```
$ veryl test --backend cc
```

The backend used during a run can be selected via `--backend {interpret,cranelift,cc}`.
If no C compiler is available, the backend falls back to Cranelift automatically.
See [the previous post](@/blog/2026-05-26-Veryl-Simulator-Performance.md) for
performance numbers from this combined backend setup.

## `--define` support for `veryl test` {{ pr(id="2597") }}

`veryl test` now accepts `--define` on the command line, and `test.defines` in
`Veryl.toml`, so testbenches can be parameterized via macros in the same way as
`veryl build`.

```toml
# Veryl.toml
[test]
defines = ["SIM_FAST"]
```

```
$ veryl test --define EXTRA_TRACE
```

## Gitoxide as the default Git backend {{ pr(id="2640") }}

The metadata layer now uses [`gitoxide`](https://github.com/GitoxideLabs/gitoxide)
by default for resolving Git dependencies, instead of shelling out to the system
`git` command.
This removes the hard runtime requirement on an external `git` binary &mdash; useful
in minimal container images and other environments where `git` is not preinstalled.
If `gitoxide` cannot handle a particular repository, Veryl transparently falls
back to the system `git` command when it is available.

The backend can be selected explicitly with the `VERYL_GIT_BACKEND` environment
variable (`auto`, `gitoxide`, or `command`).

# Other Changes

Check out everything that changed in [Release v0.20.1](https://github.com/veryl-lang/veryl/releases/tag/v0.20.1).
