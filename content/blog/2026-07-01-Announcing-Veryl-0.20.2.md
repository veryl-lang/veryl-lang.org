+++
title = "Announcing Veryl 0.20.2"
+++

The Veryl team has published a new release of Veryl, 0.20.2.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Tool Features

## SRAM inference for large arrays {{ pr(id="2895") }}

The synthesizer now infers SRAM blocks for large memory arrays instead of
expanding them into per-bit flip-flops with address decode and multiplexers.
A reset-less array with dynamic read/write addressing is recognized as a memory
and lowered to a single RAM block, which matches how such arrays are mapped to
on-chip memory macros in real designs.

```veryl
module Mem (
    clk  : input  clock     ,
    we   : input  logic     ,
    waddr: input  logic<6>  ,
    wdata: input  logic<32> ,
    raddr: input  logic<6>  ,
    rdata: output logic<32> ,
) {
    var mem: logic<32> [64];

    always_ff (clk) {
        if we {
            mem[waddr] = wdata;
        }
    }
    assign rdata = mem[raddr];
}
```

The `64 x 32` array above becomes one RAM block rather than 2048 flip-flops.
Because real SRAM has no reset, an array that is cleared on reset is intentionally
kept as flip-flops, and arrays smaller than a bit-count floor also stay as
flip-flops since the macro periphery would not pay off.

## Derived clock support in the simulator {{ pr(id="2679") }}

The native simulator now handles derived clocks &mdash; clocks produced from
another clock rather than driven directly by a top-level port.
Gated clocks, flip-flop-divided clocks, and simply copied clocks are all modeled
correctly, so designs that gate or divide their clock can be simulated without
reaching for an external tool.

```veryl
module ModuleA (
    i_clk: input  '_ clock   ,
    i_rst: input  '_ reset   ,
    i_en : input  '_ logic   ,
    o_cnt: output    logic<8>,
) {
    // A gated clock derived from the input clock.
    let clk_g: '_ clock = i_clk & i_en;

    always_ff (clk_g, i_rst) {
        if_reset {
            o_cnt = 0;
        } else {
            o_cnt += 1;   // advances only while i_en is asserted
        }
    }
}
```

## `$tb::file` for native testbench file output {{ pr(id="2860") }}

Native testbenches gain a `$tb::file` handle type for writing output files,
consistent with the existing `$tb` testbench components.
A handle is declared with `var` inside a `#[test]` module and supports
`open`, `append`, `write`, `flush`, and `close`.
The `write` formatting matches `$display`, so the same format strings can be used.

```veryl
#[test(test_file)]
module test_file {
    var f: $tb::file;

    initial {
        f.open("out.txt");
        f.write("hex=%h dec=%d\n", 8'hAB, 8'd42);
        f.close();
    }
}
```

`$tb::file` is testbench-only: declaring it outside a `#[test]` module is a
compile-time error.

## Incremental build with disk cache {{ pr(id="2815") }}

`veryl build` now keeps a true incremental build cache on disk, persisting the
symbol table and intermediate representation between runs.
The earlier incremental build skipped only some analyzer stages, which was not
enough for large projects; caching the analyzed results lets unchanged sources
be reused across builds, so rebuilds after a small edit are noticeably faster.

```
$ veryl build
```

## `--base-dir` for `veryl build` {{ pr(id="2730") }}

`veryl build` accepts a new `--base-dir <DIR>` option that redirects the
generated outputs (`.sv`, `.sv.map`) to a caller-specified directory while
sources keep resolving against the project path.
This makes it easier to integrate Veryl into external build systems such as
xmake or `build.rs`, where outputs need to land outside the project tree.
Without the flag, the output layout is byte-for-byte unchanged.

```
$ veryl build --base-dir /path/to/out
```

Relative paths are resolved against the current working directory.

## Metadata output for external tools {{ pr(id="2934") }}

`veryl metadata` can now emit a stable, versioned JSON description of the resolved
project graph, aimed at external tools that want to reuse Veryl's dependency
resolution and cache instead of reimplementing a parallel resolver.
The output includes the root and dependency metadata, each dependency's source
identity, and its local cache path.
Custom fields under `[metadata.<tool>]` in `Veryl.toml` are reserved and
preserved, so an external tool can carry its own configuration alongside the
project.

```
$ veryl metadata --format json --format-version 2
```

## Verilator arguments forwarded to cocotb runners {{ pr(id="2761") }}

When running cocotb testbenches on the Verilator backend, the runner now forwards
the build and simulation arguments configured in the `[test.verilator]` section
of `Veryl.toml`.
Previously there was no way to pass extra Verilator arguments through the cocotb
path.

```toml
# Veryl.toml
[test.verilator]
compile_args  = ["--trace"]
simulate_args = ["+verbose"]
```

# Other Changes

Check out everything that changed in [Release v0.20.2](https://github.com/veryl-lang/veryl/releases/tag/v0.20.2).
