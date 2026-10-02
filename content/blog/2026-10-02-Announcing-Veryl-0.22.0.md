+++
title = "Announcing Veryl 0.22.0"
+++

The Veryl team has published a new release of Veryl, 0.22.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Breaking Changes

## Zero width and array size are rejected {{ pr(id="3355") }}

A bit width or an array size which evaluates to 0 is now reported as the new
`zero_size` error.
`logic<W>` with `W = 0` is emitted as `logic [-1:0]`, which some SystemVerilog
tools reject and others treat as 2 bits.

A common case is `$clog2(N)` with `N = 1`.
Clip such a width to at least 1 bit, by an `if` expression or by
`clog2_clipped` in the standard library.

```veryl
module ModuleA #(
    param N: u32 = 1,
) (
    // error: zero_size when N is 1
    i_a: input logic<$clog2(N)>,
    // clipped to at least 1 bit
    i_b: input logic<if N >= 2 ? $clog2(N) : 1>       ,
    i_c: input logic<$std::utils::clog2_clipped(N, 1)>,
) {}
```

# New Language Features

## Cast by a parenthesized expression {{ pr(id="3356") }}

A constant expression enclosed in `()` can now be used as the bit width of `as`.
It is emitted as a SystemVerilog size cast.

```veryl
x as (W + 1)
(x - 1) as (W * 2)
```

```systemverilog
(W + 1)'(x)
(W * 2)'((x - 1))
```

Note that the parentheses are required.
The width operand of `as` is a single term, so `x as W + 1` is interpreted as
`(x as W) + 1`.

# New Tool Features

## Concurrent `initial` blocks in native tests {{ pr(id="3363") }}

A test module can now have multiple `initial` blocks, and each block runs as an
independent process like `initial` blocks in SystemVerilog.
While one block waits at `clk.next()`, the other blocks continue.
All blocks waiting for the same clock are resumed at the same edge, and blocks
resumed at the same time run in declaration order.
The `initial` blocks inside the instantiated modules also run as their own
processes.

This makes it easy to split a testbench into a stimulus process and a checker
process.

```veryl
#[test(test_multi_initial)]
module test_multi_initial {
    inst clk: $tb::clock_gen;
    inst rst: $tb::reset_gen ( clk );

    var done: logic;

    initial {
        done = 0;
        rst.assert();
        clk.next(5);
        done = 1;
    }

    initial {
        clk.next(8);
        $assert(done == 1);
        $finish();
    }
}
```

## `$readmemh` to a hierarchical reference {{ pr(id="3360") }}

A hierarchical reference can now be the destination of `$readmemh`, so a memory
inside the DUT can be loaded from a test module.
This is useful to load a program image into the instruction memory of a SoC.

```veryl
module Rom (
    addr: input  logic<2> ,
    data: output logic<32>,
) {
    #[allow(unassign_variable)]
    var mem: logic<32> [4];

    assign data = mem[addr];
}

#[test(test_hier_readmemh)]
module test_hier_readmemh {
    var addr: logic<2> ;
    var data: logic<32>;

    inst dut: Rom ( addr, data );

    initial {
        $readmemh("rom.hex", dut.mem);
        addr = 3;
        $assert(dut.mem[0] == 32'h1);
        $assert(data == 32'h4);
        $finish();
    }
}
```

The destination must be a whole variable, and a part of the variable such as an
element select can't be used.
Because nothing in the DUT assigns the memory, its declaration needs
`#[allow(unassign_variable)]`.

## `Value::as_slice` for verification components {{ pr(id="3368") }}

In [user defined verification components](@/blog/2026-07-14-Verification-Components.md),
`Value::as_u64` can read a value up to 64 bits only.
The new `Value::as_slice` returns all bits as 64-bit words, least significant
word first, so a value wider than 64 bits can be read.
The word layout is the same as the X/Z mask returned by `Value::mask_xz`.

```rust
let words: &[u64] = value.as_slice();
let lower = words[0];
let upper = words[1];
```

# Other Changes

Check out everything that changed in [Release v0.22.0](https://github.com/veryl-lang/veryl/releases/tag/v0.22.0).
