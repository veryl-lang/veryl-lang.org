+++
title = "Announcing Veryl 0.16.4"
+++

The Veryl team has published a new release of Veryl, 0.16.4.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Language Features

## Support embed identifier {{ pr(id="1836") }}

If you want to refer Veryl's identifier in `embed` declaration, the identifier can be placed with `\{` and `\}`. 
This is useful when you want to use complex identifiers such as generics.

```veryl
module ModuleA {
    embed (inline) sv{{{
        \{ ModuleB::<1> \} u_b ();
    }}}
}
```

## Support bind declaration {{ pr(id="1887") }}

`bind` declaration is supported to specify to bind a module to another module.

```veryl
bind ModuleA <- u: ModuleB (
  i_clk: i_clk,
  i_rst: i_rst,
  i_a  : a    ,
  o_b  : b    ,
);
```

# New Tool Features

## Add `error_count_limit` build option {{ pr(id="1864") }}

By default, Veryl compiler prints all errors. To specify maximum error count, `error_count_limit` can be used.

```toml
[build]
error_count_limit = 10
```

# Other Changes

Check out everything that changed in [Release v0.16.4](https://github.com/veryl-lang/veryl/releases/tag/v0.16.4).
