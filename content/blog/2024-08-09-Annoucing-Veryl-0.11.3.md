+++
title = "Announcing Veryl 0.11.3"
+++

The Veryl team has published a new release of Veryl, 0.11.3.
Veryl is a new hardware description language as an alternate to SystemVerilog.

The latest version of Veryl can be downloaded from [release page](https://github.com/veryl-lang/veryl/releases/latest).

# New Features

## Improve naming lint {{ pr(id="858") }} {{ pr(id="870") }}

Some missing rules of naming lint was added.
They are suffix rules and rules for function argument.

```toml
[lint.naming]
suffix_enum = "_enum"
```

## Check missing clock domain {{ pr(id="864") }}

If there are some clocks in a module, clock domain annotation became mandatory.
The following code causes `missing_clock_domain` error.

```veryl
module ModuleA (
    clk0: input clock, // should be `clk0: input 'a clock`
    clk1: input clock, // should be `clk1: input 'b clock`
) {
}
```

If the two clocks belong the same clock domain, implicit clock domain can be specified like below:

```veryl
module ModuleA (
    clk0: input '_ clock,
    clk1: input '_ clock,
) {
}
```

# Other Changes

Check out everything that changed in [Release v0.11.3](https://github.com/veryl-lang/veryl/releases/tag/v0.11.3).
