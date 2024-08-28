+++
title = "Announcing Veryl 0.11.1"
+++

The Veryl team has published a new release of Veryl, 0.11.1.
Veryl is a new hardware description language as an alternate to SystemVerilog.

The latest version of Veryl can be downloaded from [release page](https://github.com/veryl-lang/veryl/releases/latest).

# New Features

## Add sourcemap-resolver to release build {{ pr(id="810") }}

`sourcemap-resolver` binary was added to release package.
It can be used as filter program throught pipe like below:

```console
$ make | sourcemap-resolver
```

By `sourcemap-resolver`, file location in log can be resolved to the location in Veryl.

* Before pipe

```
%Error: /path/test.sv:23:1: syntax error, unexpected endmodule
   23 | endmodule
      | ^~~~~~~~~
```

* After pipe

```
%Error: /path/test.sv:23:1: syntax error, unexpected endmodule
        ^ from: /path/test.veryl:18:18
   23 | endmodule
      | ^~~~~~~~~
```

## Add raw identifier {{ pr(id="806") }}

Some Veryl's keyword can be used as identifier in SystemVerilog.
So instantiating a SystemVerilog module may cause syntax error.

```veryl
module ModuleA (
    i_clk: input clock,
    i_rst: input reset,
) {
    inst u0: $sv::ModuleSV (
        clock: i_clk, //syntax error because `clock` is Veryl's keyword
        reset: i_rst, //syntax error because `reset` is Veryl's keyword
    );
}
```

To fix it, raw identifier was introduced.
It starts with `r#` prefix and transpiled into an identifier without the prefix.

```veryl
module ModuleA (
    i_clk: input clock,
    i_rst: input reset,
) {
    inst u0: $sv::ModuleSV (
        r#clock: i_clk, // transpiled into `.clock(i_clk),`
        r#reset: i_rst, // transpiled into `.reset(i_rst),`
    );
}
```
