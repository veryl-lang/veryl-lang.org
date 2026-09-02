+++
title = "Announcing Veryl 0.21.0"
+++

The Veryl team has published a new release of Veryl, 0.21.0.
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

## Non-portable constructs need an explicit opt-in {{ pr(id="3268") }}

Some constructs are valid on FPGA but not on ASIC.
Two new `allow` items opt in to them, written on the declaration of the variable
they concern.

`initial_assign` allows the variable to be assigned in an `initial` block, which
relies on the target device initializing it at configuration time.
Assignment through an output argument of a function call, such as `$readmemh`
and `$readmemb`, is covered as well.

On the other hand, ASIC synthesizers ignore an `initial` block, so such an
assignment is no longer accepted on its own.
It passed without any check until Veryl 0.20.3, and is now reported as
`invalid_initial_assign` without the attribute.
To migrate, add the attribute to the declaration.
`veryl migrate` rewrites the `$readmemh` / `$readmemb` case automatically, and
the other assignments need the attribute by hand.

```veryl
// before
var count: logic<16>       ;
var rom  : logic<32> [1024];

initial {
    count = '0;
    $readmemh("rom.hex", rom);
}

// after
#[allow(initial_assign)]
var count: logic<16>;

#[allow(initial_assign)]
var rom: logic<32> [1024];

initial {
    count = '0;
    $readmemh("rom.hex", rom);
}
```

`multiple_assign` allows the variable to be assigned from more than one process,
as true dual port SRAM inference on FPGA requires.
It relaxes the existing `multiple_assignment` error, so it needs no migration.

```veryl
module ModuleB (
    i_clk0 : input  'a clock    ,
    i_clk1 : input  'b clock    ,
    i_en0  : input  'a logic    ,
    i_en1  : input  'b logic    ,
    i_addr0: input  'a logic<5> ,
    i_addr1: input  'b logic<5> ,
    i_data0: input  'a logic<32>,
    i_data1: input  'b logic<32>,
    o_data : output 'a logic<32>,
) {
    #[allow(multiple_assign)]
    var ram: 'a logic<32> [32];

    always_ff (i_clk0) {
        if i_en0 {
            ram[i_addr0] = i_data0;
        }
    }

    unsafe (cdc) {
        always_ff (i_clk1) {
            if i_en1 {
                ram[i_addr1] = i_data1;
            }
        }
    }

    assign o_data = ram[i_addr0];
}
```

SystemVerilog forbids a variable written by an `always_ff` from being written by
any other process, so an `always_ff` which writes a variable with either
attribute is emitted as a plain `always`.

To keep these constructs out of a project whose target does not support them,
whether they are accepted from dependencies is decided by the consumer through
the new `[lint.portability]` section of `Veryl.toml`.

```toml
[lint.portability]
allow_in_dependencies = ["initial_assign"]
```

In your own code the attribute is always honored: you wrote it, it is your call.
In the code of a dependency it is rejected as `non_portable_dependency` unless it
is listed here, and the default is to accept nothing.
So an ASIC project can't absorb an FPGA-only library without noticing, while an
FPGA user pulling an FPGA library adds one line.

# New Language Features

## Component namespace import {{ pr(id="3198") }} {{ pr(id="3261") }} {{ pr(id="3262") }}

A component itself, which is a package, module or interface, can now be imported
under its own name.
The imported name is used as a qualifier at the use site, so a component of a
dependency can be referenced without repeating the project name.

```veryl
import veryl_sample::sample_pkg;
import veryl_sample::sample_if;
import veryl_sample::sample_module;

module ModuleC {
    const A: u32 = sample_pkg::PARAM_A;

    inst u_if: sample_if;
    inst u: sample_module (
        o_a: u_if.a,
    );
}
```

A generic component is imported as its definition, and the generic arguments are
given at the use site.

```veryl
import veryl_sample::generic_pkg;

module ModuleD {
    const B: u32 = generic_pkg::<32>::PARAM_B;
}
```

A `proto package` can be imported in the same way, and the imported name can be
used as a generic bound.
The other prototypes like `proto module` and `proto interface` can't be imported.

```veryl
import veryl_sample::sample_proto_pkg;

module ModuleE::<PKG: sample_proto_pkg> {
    let _a: logic<PKG::WIDTH> = 0;
}
```

A function declared at the project scope, which means outside any module,
interface and package, can be imported through the project name too.

```veryl
import veryl_sample::sample_func;

module ModuleF {
    let _a: logic<8> = sample_func::<8>(8'd1);
}
```

## Generic argument inference from module ports {{ pr(id="3197") }}

The generic arguments of a function call can be omitted when they are inferred
from the declared type of the call arguments.
The inference accepted a local variable or a parameter, and now a module port
drives it in the same way.

```veryl
module ModuleG (
    i_d: input logic<8>,
) {
    function FuncId::<T: u32> (
        x: input logic<T>,
    ) -> logic<T> {
        return x;
    }

    // T is inferred to be 8 from the port's declared width.
    let _r: logic<8> = FuncId(i_d);
}
```

# Improvements

## Combinational loop analysis {{ pr(id="3161") }}

The combinational loop detector has been rebuilt on statement-ordered SSA with
sparse bit and array partitions.

Successive assignments to a module-scope variable inside a single `always_comb`
were reported as a loop, because the reads were not matched with the definition
which actually reaches them.
The block below is feed-forward under the blocking assignment semantics of
`always_comb`, and is no longer reported.

```veryl
module ModuleH (
    a: output logic,
) {
    var b: logic;

    always_comb {
        a = 0;
        b = a;
        a = b;
    }
}
```

Arrays of more than 65536 elements were skipped by the analysis entirely, since
the per-element expansion was proportional to the declared shape.
The partitions are now built sparsely, so element identity is preserved for
large and multidimensional arrays without enumerating that shape, and the size
cutoff is gone.
When a flattened width, array size, or positional offset tracked by the analysis
exceeds the supported range, it is reported as the new
`combinational_loop_position_overflow` error instead of being silently dropped.

This is the initial implementation of the new analysis.
Remaining false positives and false negatives, richer function and interface
summaries, and latch diagnostics will be improved incrementally.

# Other Changes

Check out everything that changed in [Release v0.21.0](https://github.com/veryl-lang/veryl/releases/tag/v0.21.0).
