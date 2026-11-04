+++
title = "Announcing Veryl 0.22.1"
+++

The Veryl team has published a new release of Veryl, 0.22.1.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Important Notice

## Stricter `multiple_assignment` check {{ pr(id="3582") }}

Writes to overlapping bits of the same variable from multiple processes through
a dynamic index are now reported as `multiple_assignment`.
Such writes were overlooked before.
If they are intended, for example to infer a dual-port SRAM, add
`#[allow(multiple_assign)]` to the variable declaration.

# New Language Features

## `reset_active` and `reset_inactive` literals {{ pr(id="3547") }}

`reset_active` and `reset_inactive` describe the asserted and de-asserted value
of a reset signal without depending on its polarity.
They are emitted as `1'b1` or `1'b0` according to the polarity of the reset type
they are compared with or assigned to, so a design no longer has to hard-code
`0` or `1` for a reset.

```veryl
module ModuleA (
    i_rst: input  reset_async_low,
    o_a  : output logic          ,
) {
    let rst: reset = reset_active;

    assign o_a = i_rst == reset_inactive;

    inst u: ModuleB (
        i_rst: reset_inactive,
    );
}
```

## `#[inline]` attribute for interface functions {{ pr(id="3642") }}

A call to an interface function marked with `#[inline]` is replaced with the
expression of the function in the emitted SystemVerilog.
This avoids the overhead of function calls on SystemVerilog simulators.

```veryl
interface InterfaceA {
    var ready: logic;
    var valid: logic;

    #[inline]
    function ack () -> logic {
        return ready && valid;
    }
}
```

## `$define` namespace {{ pr(id="3513") }}

Macros defined in SystemVerilog can be referred through the `$define` namespace.
A reference under `$define` is emitted as a macro reference with a backquote.

```veryl
module ModuleA (
    i_a: input logic<$define::WIDTH>,
) {
    const A: u32 = $define::A;
    const B: u32 = $define::PKG::B;
    var   c: $define::TYPE;
}
```

# New Tool Features

## `$tb::queue` testbench component {{ pr(id="3558") }}

`$tb::queue` is a queue for native tests, useful as the expected-value store of
a scoreboard.

```veryl
#[test(test_queue)]
module test_queue {
    var q: $tb::queue::<u32>   ; // unbounded
    var b: $tb::queue::<u8, 16>; // up to 16 elements
    var x: u32                 ;

    initial {
        q.push_back(1);
        q.push_front(0);
        x = q.pop_front(); // 0
        $assert(q.size() == 1);
        q.drop_back(); // remove without reading
        $finish();
    }
}
```

## SystemVerilog filesets {{ pr(id="3564") }}

SystemVerilog files such as third-party IPs can be managed together with a Veryl
project through `[[sv.filesets]]` in `Veryl.toml`.

```toml
[properties]
for_asic = false
width    = 32

[[sv.filesets]]
root         = "ip/foo"
files        = ["rtl/foo_pkg.sv", "rtl/foo.sv"]
include_dirs = ["include"]

[[sv.filesets]]
root      = "ip/foo"
enable_if = "for_asic && width == 32"
files     = ["asic/foo_asic.sv"]
```

The enabled filesets are added to the filelist, including those of dependencies.
`enable_if` is a condition on [project
properties](@/blog/2026-08-03-Announcing-Veryl-0.20.3.md).

# Other Changes

Check out everything that changed in [Release v0.22.1](https://github.com/veryl-lang/veryl/releases/tag/v0.22.1).
