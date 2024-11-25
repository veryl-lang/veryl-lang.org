+++
title = "Announcing Veryl 0.13.3"
+++

The Veryl team has published a new release of Veryl, 0.13.3.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Features

## Support width cast {{ pr(id="1095") }}

Bit width cast is added. Now arbitrary expression is not allowed yet as the width, and `based` and `baseless` number are only allowed.

```veryl
assign a = x as 2;
assign b = x as 10'h2;
```

## Support generic interface with modport {{ pr(id="1089") }}

Generic interface with modport which means arbitrary interface which has the specified modport are supported.

```veryl
module ModuleA (
    bus_if: interface::slave,
) {
}
```

## Remove map and doc files by `clean` command {{ pr(id="1061") }}

`veryl clean` command becomes to clean the generated map files and document files.

```
$ veryl clean
```

## Add pre-defined vector types {{ pr(id="1044") }}

Some frequent vector types are added to the standard library.
They are combination of 8/16/32/64bit, signed/unsigned and bit/logic.

```veryl
module ModuleA {
    var a: $std::types::ul8; // 8bit unsigned logic 
    var b: $std::types::il8; // 8bit signed   logic
    var c: $std::types::ub8; // 8bit unsigned bit
    var d: $std::types::ib8; // 8bit signed   bit
}
```

## `cond_type` attribute {{ pr(id="1043") }}

To specify `unique`, `unique0` and `priority` in SystemVerilog, `cond_type` attribute is added.
The attribute can be annotated to `case` or `if` statement.

* `unique`: There are no overlapping items. Error if no item matches.
* `unique0`: There are no overlapping items. No error if no item matches.
* `priority`: The first match is used only. Error if no item matches.

```veryl
#[cond_type(unique)]
case a {

}


#[cond_type(priority)]
case a {
}

#[cond_type(unique0)]
if a {
} else if b {
} else {
}
```

These attributes enable more aggressive optimization in synthesis, but if the expected condition is not complied, the result of synthesis will be broken.
So these attributes are ignored by default, and if there is the following configuration, Veryl compiler emits them.

```toml
[build]
emit_cond_type = true
```

# Other Changes

Check out everything that changed in [Release v0.13.3](https://github.com/veryl-lang/veryl/releases/tag/v0.13.3).
