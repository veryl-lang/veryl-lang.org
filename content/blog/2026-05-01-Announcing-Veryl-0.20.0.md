+++
title = "Announcing Veryl 0.20.0"
+++

The Veryl team has published a new release of Veryl, 0.20.0.
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

## Remove type specification on `for` iterator {{ pr(id="2516") }}

The iterator variable in `for` no longer accepts a type specification.
`i32` is always used as the iterator type, which is more than sufficient for any
practical hardware loop bound and matches the syntax of `generate for`.

To migrate, drop the type annotation on the iterator. `veryl migrate` rewrites this
automatically.

```veryl
// before
for i: u32 in 0..10 {
    a[i] = '0;
}

// after
for i in 0..10 {
    a[i] = '0;
}
```

## `$tb::reset_gen` takes a `clk` port {{ pr(id="2574") }}

`$tb::reset_gen` now binds to its clock at instantiation time instead of receiving the
clock as an argument to each `assert` call. Reset timing is always bound to a specific
clock in practice, so this makes the binding explicit at the connection site.

To migrate, move the clock from the `assert` argument list to the `reset_gen` instance
port list.

```veryl
// before
inst rst: $tb::reset_gen();

initial {
    rst.assert(clk);
    // ...
}

// after
inst rst: $tb::reset_gen(clk);

initial {
    rst.assert();
    // ...
}
```

# New Language Features

## Type inference {{ pr(id="2478") }}

Type annotations on `let`, `const`, and `var` declarations are now optional.
The type is inferred from the right-hand side expression, or for `var` declarations,
from the first subsequent assignment.

```veryl
module ModuleA {
    let _a: logic<8> = 0;

    // Variable reference: type copied from the referenced variable.
    let _b = _a;

    // Sized literal: type implied by the literal itself.
    let _c = 8'd255;

    // const declarations also support inference.
    const _D = 16'd100;

    // var without annotation: inferred from the first assignment,
    // including assignments inside always_comb blocks.
    var _e;
    always_comb {
        _e = _a;
    }
}
```

## Introduce `gen` declaration {{ pr(id="2412") }}

A new `gen` declaration lets generic modules compute values &mdash; including derived
types &mdash; that can themselves be passed as generic arguments to inner instances.

```veryl
module ModuleA::<W: u32, T: type> (
    a: output logic<W>,
    b: output T       ,
) {
    always_comb {
        a = '0;
        b = '0;
    }
}

module ModuleB::<A: u32, B: u32, C: u32> {
    gen W: u32  = A + B;
    gen T: type = logic<C>;

    inst u: ModuleA::<W, T> (a: _, b: _);
}
```

# New Tool Features

## Logic synthesis support {{ pr(id="2553") }}

`veryl synth` performs a lightweight gate-level synthesis directly from the toolchain
and reports area, critical-path timing, and power for the chosen top module.

```
$ veryl synth --top Counter
synth: Counter — 137 gates, 32 FFs
library: SKY130 (SkyWater 130nm) / sky130_fd_sc_hd / tt_025C_1v80
summary:
  area:        1542.50 um²  (comb 822.50, seq 720.00)
  timing:        0.540 ns       6 levels  r_cnt[15] → r_cnt[24]
  power:         0.0990 mW   (leak 0.0001 mW, dyn 0.0989 mW)
                 @ f_clk = 100 MHz, activity = 0.10
```

Cell area, delay, and power figures are calibrated against public Liberty data from
open PDKs &mdash; SKY130 (SkyWater 130nm), ASAP7, GF180MCU, and IHP SG13G2 &mdash; so
estimates are based on real silicon ratios rather than abstract gate counts.
The numbers are intended as reference values for early-stage exploration, not signoff.

## SystemVerilog → Veryl translator {{ pr(id="2480") }}

`veryl translate` converts SystemVerilog source files to equivalent Veryl, helpful for
incrementally migrating existing designs.

```
$ veryl translate counter.sv
$ ls counter.veryl
counter.veryl
```

## Improve `$assert` / `$assert_continue` in testbench {{ pr(id="2578") }}

Native testbench assertions now report values and source locations on failure,
making test debugging significantly easier.

## Configurable newline style {{ pr(id="2470") }}

The formatter and the SystemVerilog translator now preserve the newline style of the
input file by default. Files originally written with CRLF stay CRLF after formatting
or translation, instead of being silently rewritten to LF. The behavior is
configurable via `format.newline_style` in `Veryl.toml`.

# New Standard Library

## Add utility functions {{ pr(id="2444") }} {{ pr(id="2447") }} {{ pr(id="2451") }} {{ pr(id="2577") }}

The following utility functions have been added under `$std::utils`:

- `min`, `max` &mdash; element-wise minimum/maximum
- `zero_extend`, `one_extend`, `sign_extend`, `truncate` &mdash; width manipulation primitives
- `select_*`, `dispatch_*` &mdash; mux/demux building blocks usable outside of the `mux` and `demux` modules
- `clog2_clipped` &mdash; a clipped variant of `clog2` that stays well-defined for small ranges

# Other Changes

Check out everything that changed in [Release v0.20.0](https://github.com/veryl-lang/veryl/releases/tag/v0.20.0).
