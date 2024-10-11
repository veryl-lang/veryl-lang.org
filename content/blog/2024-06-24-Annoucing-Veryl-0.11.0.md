+++
title = "Announcing Veryl 0.11.0"
+++

The Veryl team has published a new release of Veryl, 0.11.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

The latest version of Veryl can be downloaded from [release page](https://github.com/veryl-lang/veryl/releases/latest).

# Breaking Changes

## Clock domain annotation support {{ pr(id="789") }}

If there are some clocks in a module, clock domain annotation is required.
Clock domain annotation represents which clock domain each port belongs to.
Additionally, assignment over different clock domains requires `unsafe (cdc)` block.

```veryl
module ModuleA (
    // clock domain 'a
    i_clk_a: input  'a clock,
    i_dat_a: input  'a logic,
    o_dat_a: output 'a logic,

    // clock domain 'b
    i_clk_b: input  'b clock,
    i_dat_b: input  'b logic,
    o_dat_b: output 'b logic,
) {
    unsafe (cdc) {
        // assignment from 'a domain to 'b domain
        assign o_dat_b = i_dat_a;
    }
}
```

# New Features

## Support importing functions into modport {{ pr(id="742") }}

Function in interface can be imported through `import` direction in `modport` declaration.

```veryl
interface InterfaceA {
    var a: logic;

    function get_a () -> logic {
        return a;
    }

    modport slave {
        a    : input ,
        get_a: import,
    }
}
```

## Add signed literal support {{ pr(id="770") }}

Signed literal with `s` prefix is supported.

```veryl
module ModuleA {
    local a: u32 = 32'sb1111;
    local b: u32 = 32'so7777;
    local c: u32 = 32'sd9999;
    local d: u32 = 32'shffff;
}
```

## Enhance case statement/expression {{ pr(id="783") }}

As case item, range expression and expression with constant value can be used.
`switch` which has arbitrary expression as the condition items is added too.

```veryl
module Module16 {
    local P: bit = 1;

    var a: logic;
    var b: logic;
    let x: logic = 1;
    let y: logic = 1;

    always_comb {
        case x {
            5..=7  : a = 1;
            P - 1  : a = 1;
            // Error because y is not constant value
            //y - 1  : a = 1;
            default: a = 1;
        }
    }

    always_comb {
        switch {
            // arbitrary expression includuing variable can be used
            y == 0 : b = 1;
            default: b = 1;
        }
    }
}
```

# Other Changes

Check out everything that changed in [Release v0.11.0](https://github.com/veryl-lang/veryl/releases/tag/v0.11.0).
