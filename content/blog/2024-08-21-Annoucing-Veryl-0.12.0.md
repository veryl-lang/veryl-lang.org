+++
title = "Announcing Veryl 0.12.0"
+++

The Veryl team has published a new release of Veryl, 0.12.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

The latest version of Veryl can be downloaded from [release page](https://github.com/veryl-lang/veryl/releases/latest).

# Breaking Changes

## Forbid continuous casting {{ pr(id="887") }}

Until Veryl 0.12.0, casting by `as` could be continuous, but it is forbidden by Veryl 0.12.0.
If continuous casting is required, it can be achieved by inserting `()`.

```veryl
// Syntax error
assign a = x as u32 as i32;
// OK
assign a = (x as u32) as i32;
```

## Change symbol of clock domain annotation {{ pr(id="883") }}

Until Veryl 0.12.0, clock domain annotation used single quotation mark like `'x`.
Veryl 0.12.0 changes it to backtick mark like `` `x ``.

```veryl
// Syntax error
var a: 'x clock;
// OK
var a: `x clock;
```

# New Features

## Expand `inside` operation {{ pr(id="873") }}

Some EDA tools doesn't support `inside` operation.
For these tools, `expand_inside_operation` configuration of `Veryl.toml` can be used like below:

```toml
[build]
expand_inside_operation = true
```

If the configuration is enabled, `inside` operations in the generated SystemVerilog are expanded like below:

* Default

```veryl
assign a = inside 1 + 2 / 3 {0, 0..10, 1..=10};
```

* Expand

```veryl
assign a = ((1 + 2 / 3) ==? 0) ||
           ((1 + 2 / 3) >= 0 && (1 + 2 / 3) < 10) ||
           ((1 + 2 / 3) >= 0 && (1 + 2 / 3) <= 10);
```

## Waveform dump support through `veryl test --wave` {{ pr(id="898") }}

Waveform dump in integrated test is supported.
If `--wave` option is specified at `veryl test`, `[test name].vcd` files are generated.
The generation place is the same as generated SystemVerilog code by default.
It can be configured through `waveform_target` in `Veryl.toml`.

```toml
[test]
waveform_target = {type = "directory", path = "[dst dir]"}
```

## Cocotb support for integrated test {{ pr(id="899") }}

As the way of `embed` and language specifier, `cocotb` and `py` are supported now.
If `cocotb` is specified, the embeded code are interpreted as cocotb code and executed through external Python3 environment.
cocotb requires to specify the name of top module, so it should be specified through the second argument of `#[test]` attribute.

To use this feature, `python3` environment in which `cocotb` 1.9.0 is installed is required.

```veryl
#[test(test1, ModuleA)]
embed (cocotb) py{{{
import cocotb

@cocotb.test()
async def test(dut):
    dut.i_d.value = 0
}}}

```

## Embed standard library into compiler {{ pr(id="878") }}

Standard library is embeded into Veryl compiler, and it can be used through `std` namespace.
For example, `std::fifo` is FIFO module in standard library, and can be used without adding dependency like below.
All list and documentation is [https://std.veryl-lang.org](https://std.veryl-lang.org).

```veryl
module ModuleA {
    inst u: std::fifo (
        i_clk        : _,
        i_rst        : _,
        i_clear      : _,
        o_empty      : _,
        o_almost_full: _,
        o_full       : _,
        o_word_count : _,
        i_push       : _,
        i_data       : _,
        i_pop        : _,
        o_data       : _,
    );
}
```

The public API of standard library is not stable until Veryl 1.0.
If there is any idea or suggestion, please open issue or pull request at [https://github.com/veryl-lang/std](https://github.com/veryl-lang/std).
