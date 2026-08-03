+++
title = "Announcing Veryl 0.20.3"
+++

The Veryl team has published a new release of Veryl, 0.20.3.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Important Notice

## Base-less literal in concatenation {{ pr(id="3049") }}

A base-less literal like `123` used as an operand of a concatenation is now
reported as `invalid_unsized_literal`.

```veryl
assign y = {a, 123};   // error
assign y = {a, 8'd123};
```

Such a literal was accepted before, but it was emitted verbatim as an unsized
literal, which is forbidden in a concatenation by the SystemVerilog LRM and
rejected by some tools.
Existing code which relies on it needs to give the literal an explicit width.
A base-less replication count like `{a repeat 2}` keeps working as before.

# New Language Features

## `mixin` declaration for interfaces {{ pr(id="2996") }}

An interface can now incorporate the members of other interfaces through a
`mixin` declaration.
All members &mdash; variables, functions, and modports &mdash; of the mixed-in
interface are expanded as if they were declared directly in the interface.

For example, the channels of a bus protocol can be defined as separate interfaces
and reused across multiple bus interfaces.

```veryl
interface Command::<ADDR_WIDTH: u32, DATA_WIDTH: u32> {
    var cmd_valid: logic            ;
    var cmd_addr : logic<ADDR_WIDTH>;
    var cmd_data : logic<DATA_WIDTH>;

    modport mp_cmd {
        cmd_valid: output,
        cmd_addr : output,
        cmd_data : output,
    }
}

interface Response::<DATA_WIDTH: u32> {
    var rsp_valid: logic            ;
    var rsp_data : logic<DATA_WIDTH>;

    modport mp_rsp {
        rsp_valid: input,
        rsp_data : input,
    }
}

interface MemoryBus::<ADDR_WIDTH: u32, DATA_WIDTH: u32> {
    mixin Command::<ADDR_WIDTH, DATA_WIDTH>;
    mixin Response::<DATA_WIDTH>;

    modport master {
        ..same(mp_cmd, mp_rsp)
    }

    modport slave {
        ..converse(mp_cmd, mp_rsp)
    }
}
```

As shown above, a generic interface can be mixed in by giving its generic
arguments.

## Project property {{ pr(id="2968") }} {{ pr(id="3119") }}

A project property is a compile time constant given through `Veryl.toml` instead
of source code.
Properties are defined in the `[properties]` section, and their values are
integers or booleans.

```toml
[properties]
DATA_WIDTH   = 32
ENABLE_DEBUG = false
```

They are referenced through the `$prop` namespace, and can be used wherever a
constant expression can be used.

```veryl
module ModuleA {
    var a: logic<$prop::DATA_WIDTH>;

    if $prop::ENABLE_DEBUG :g_debug {
        // debug logic
    }
}
```

## Brace list in `import` {{ pr(id="3053") }}

Multiple symbols can be imported from a single package at once by listing them
in braces, in the same style as Rust.

```veryl
module ModuleA {
    import PackageA::{paramA, paramB};
}
```

# New Tool Features

## User defined verification components {{ pr(id="2985") }}

Verification components written in Rust &mdash; a bus functional model, a
protocol checker, or a golden model &mdash; can now be driven by the native
simulator under the `$comp` namespace.
A component is ordinary Rust, so it can pull in any crate instead of relying on
SystemVerilog boilerplate or hand-written DPI-C glue.

```veryl
#[test(test_req_ack)]
module test_req_ack {
    inst clk: $tb::clock_gen;
    inst rst: $tb::reset_gen ( clk );

    var req: logic;
    var ack: logic;

    inst dut: Peripheral ( clk, rst, req, ack );

    inst chk: $comp::req_ack_checker ( clk, req, ack );

    initial {
        rst.assert();
        req = 1;
        clk.next(16);
        $finish();
    }
}
```

It is covered in detail by a dedicated article:
[Verification components in Rust](@/blog/2026-07-14-Verification-Components.md).
[`veryl-lang/vip`](https://github.com/veryl-lang/vip), a set of AXI verification
components, is built this way.

## Hierarchical reference in native tests {{ pr(id="2974") }}

Signals inside the DUT can be read from an `initial` block of a test module
through a hierarchical path.
The path starts at an instance of the test module and goes through nested
instances by `.`, so internal signals no longer have to be routed to the top
level just to be observed.

```veryl
#[test(test_hier)]
module test_hier {
    inst clk: $tb::clock_gen;
    inst rst: $tb::reset_gen ( clk );

    var din: logic<4>;

    inst dut: Top ( clk, rst, din );

    initial {
        rst.assert();
        din = 4'b0001;
        clk.next();
        $assert(dut.u_sub.internal_reg == 4'h2, "unexpected value");
        $display("internal_reg = %h", dut.u_sub.internal_reg);
        $finish();
    }
}
```

## `$tb::random` testbench component {{ pr(id="3078") }}

`$tb::random` is a random-number generator for native tests.
The type of the generated value is given as a generic argument.

```veryl
#[test(test_random)]
module test_random {
    var r: $tb::random::<u32>;
    var x: u32;

    initial {
        r.seed(42);              // set the seed
        x = r.get();             // uniform over the full u32 range
        x = r.get_range(10, 20); // 10 <= x <= 20
        $finish();
    }
}
```

The seed used by a run is printed, and giving it back through `--seed` or
`[test].seed` reproduces the same sequence.

## Four-state native test {{ pr(id="2984") }}

Native tests can be run in four-state (X/Z) mode.
By default a value which is not assigned is read as `0`; under a four-state run,
it is read as `x` instead, which surfaces missing initialization and incomplete
resets.

```
$ veryl test --4state
```

It can also be enabled through `Veryl.toml`:

```toml
[test]
four_state = true
```

## The `examples` directory {{ pr(id="2978") }}

The `examples` directory at the project root is now reserved as a place for usage
examples and testbenches.

```
$ tree
.
|-- examples
|   `-- example_top.veryl
|-- src
|   `-- module_a.veryl
`-- Veryl.toml
```

Files under `examples` are analyzed and checked like ordinary sources, and
`#[test]` modules in them are executed by `veryl test`.
They are excluded from code generation and the generated document, and ignored
entirely when the project is consumed as a dependency.
So examples can be kept in the repository without leaking into the deliverables
of the projects which depend on it.

## External subcommand {{ pr(id="2935") }}

The `veryl` command can be extended by tools distributed separately from Veryl,
in the same way as `cargo`.
If the given subcommand is not a built-in one, `veryl` searches `PATH` for an
executable named `veryl-<subcommand>` and executes it.

```
$ veryl import foo.sv
```

The command above executes `veryl-import foo.sv` if `veryl-import` is found on
`PATH`, so such a tool can be used as if it was a built-in subcommand.
`veryl --list` shows all available commands including the external ones.

## JSON report for `veryl synth` and `veryl test` {{ pr(id="3074") }}

`--format json` makes `veryl synth` and `veryl test` write a machine-readable
report to stdout instead of the human-readable summary, which is useful to
consume the results from CI or other tools.

```
$ veryl synth --format json
```

```
{
  "format_version": 1,
  "top": "Counter",
  "library": "sky130",
  "status": "ok",
  "cells": 19,
  "ffs": 8,
  "area": { "total": 302.5, "combinational": 122.5, "sequential": 180.0, "memory": 0.0 },
  "timing": { "delay_ns": 0.38, "depth": 4, "from": "cnt[3]", "to": "cnt[6]" },
  "power": { "total_mw": 0.0239, "leakage_mw": 0.0000271, "dynamic_mw": 0.0239, "clock_freq_mhz": 100.0, "activity": 0.1 }
}
```

For `veryl test`, the report lists the pass/fail status, message, and runtime of
each test.

## Registry registration on publish {{ pr(id="3015") }} {{ pr(id="3013") }}

The client-side integration with the [official package
registry](@/blog/2026-07-21-Official-Package-Registry.md) has landed.
A project which declares its `repository` can be registered by `veryl register`,
and `veryl publish` can register it too through `register` in the `[publish]`
section of `Veryl.toml`.

```toml
[project]
name       = "my_ip"
version    = "0.1.0"
repository = "https://github.com/you/my_ip"
categories = ["interconnect", "verification"]

[publish]
register = true
```

The new `categories` field of the `[project]` section lists the categories which
the project belongs to, and the registry uses them to classify the project.

# New Standard Library

## ECC encoder / decoder {{ pr(id="3087") }}

`$std::ecc_encoder` and `$std::ecc_decoder` provide Hamming-code based ECC with
single error correction and double error detection.

# Other Changes

Check out everything that changed in [Release v0.20.3](https://github.com/veryl-lang/veryl/releases/tag/v0.20.3).
