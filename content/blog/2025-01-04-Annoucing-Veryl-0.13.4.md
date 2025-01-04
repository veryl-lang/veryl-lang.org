+++
title = "Announcing Veryl 0.13.4"
+++

The Veryl team has published a new release of Veryl, 0.13.4.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Features

## Support port default value {{ pr(id="1164") }}

Ports of module becomes to be able to have default value.
Ports which have default value can be omitted at the instantiation, and the default values are assigned to the omitted ports.

```veryl
module ModuleA (
    a: input  logic    ,
    b: input  logic = 1, // default value
    x: output logic    ,
    y: output logic = _, // default value
) {
    assign x = a;
    assign y = b;
}

module ModubeB {
    inst instA: ModuleA (
        a: 1,
        // b is omitted
        x: _,
        // y is omitted
    );
}
```

## Add mux/demux modules to std library {{ pr(id="1148") }}

Multiplexer and demultiplexer are added to the standard library.

```veryl
inst u_mux: $std::mux (
    i_select: _,
    i_data  : _,
    o_data  : _,
);

inst u_demux: $std::demux (
    i_select: _,
    i_data  : _,
    o_data  : _,
);
```

## Apply ifdef attributes in statement block {{ pr(id="1136") }}

`ifdef` attribute can be used in statement block.

```veryl
always_comb {
    #[ifdef(DEFINE_A)]
    {
        a = 1;
        b = 1;
    }
    #[ifdef(DEFINE_B)]
    c = 1;
}
```

## Support relative path dependency {{ pr(id="1099") }}

Dependencies to the project through local relative paths can be specified.

```toml
[dependencies]
"../../library/path" = "0.1.0"
```


# Other Changes

Check out everything that changed in [Release v0.13.4](https://github.com/veryl-lang/veryl/releases/tag/v0.13.4).
