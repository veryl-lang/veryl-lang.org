+++
title = "Verification components in Rust"
+++

A heads-up ahead of the release: verification components are a major new feature,
not in a stable release yet but arriving in the next version, due in early August. Everything
below already works on the nightly toolchain.

Veryl's native test lets you write testbenches directly in Veryl, driven by the
built-in simulator, with `$tb::clock_gen`, `$tb::reset_gen`, `$assert`, and
`$finish`. You can now bring your own **verification components written in Rust**,
such as a bus functional model, a protocol checker, or a golden model, all driven
by the same simulator under the `$comp` namespace.

A component is ordinary Rust, so a verification model can lean on the language and
its libraries instead of SystemVerilog boilerplate or hand-written DPI-C glue. A
golden model, for instance, can be a handful of lines or a full instruction-set
simulator, checked against the RTL as the test runs.

Here is a checker that watches a request/acknowledge handshake. In a native test
it is instantiated like any module:

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

Its behavior is a plain struct and `impl` block that reads as idiomatic Rust, with
fields for the ports and an `on_clock` hook that runs every cycle (implementation
elided):

```rust
#[derive(Component)]
pub struct ReqAckChecker {
    clk: ClockPort,
    req: InputPort,
    ack: InputPort,
}

#[component_impl]
impl ReqAckChecker {
    fn on_clock(&mut self, ctx: &mut SimCtx) -> Result<()> {
        // check that `ack` follows `req` each cycle
        // ...
    }
}
```

For something closer to real use, [`veryl-lang/vip`](https://github.com/veryl-lang/vip)
is a set of AXI verification components — masters, memory models, and checkers for
AXI4-Lite, AXI4-Stream, AXI4, and AXI3 — all built this way.

## What you can do

- **Clocked behavior.** A clocked component updates on clock edges like an
  `always_ff` process, so a bus functional model or a checker fits into the
  clocked timeline.
- **DUT-internal access.** Its ports can connect straight to signals inside the
  DUT, so you can check internal state without routing it out to the top level.
- **Zero-time methods.** A component can also expose methods that a testbench
  calls from an `initial` block, which is how a golden model or a memory loader
  is driven.
- **Full Rust.** A component is a full Rust program: it can pull in any crate,
  talk over a network socket, pop up a GUI window, or shell out to an external
  tool.
- **Distribution.** Components ride on Veryl's normal package dependencies: a
  package declares its components, and a project that depends on it uses them
  under `$comp`. A component can also ship as a prebuilt, sandboxed wasm binary
  for consumers without a Rust toolchain, though a prebuilt binary is limited to
  plain computation; anything more is built from source instead.

## Getting started

You can try them now on the nightly toolchain with `verylup install nightly`. The
language reference covers the details, from the component API to distribution:
[Writing a Component](https://doc.veryl-lang.org/nightly/book/05_language_reference/13_integrated_test/02_writing_a_component.html)
and [Using a Component](https://doc.veryl-lang.org/nightly/book/05_language_reference/13_integrated_test/01_using_a_component.html).