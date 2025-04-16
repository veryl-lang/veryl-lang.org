+++
title = "Announcing Veryl 0.15.0"
+++

The Veryl team has published a new release of Veryl, 0.15.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Breaking Changes

## Simplify if expression notation {{ pr(id="1457") }}

If expression is a relpacement of conditional operator in SystemVerilog, but it is pretty long than conditional operator.
And the `{}` is redundant because only single expression can be placed in `{}`.
Therefore, the notation is changed to more simplified style like conditional operator.

```veryl
// Before
assign a = if b { c } else { d };

// After
assign a = if b ? c : d;
```

We added `veryl migrate` to migrate this change automatically, because it will affect many existing codebase.

```console
// Check how changes will be applied
$ veryl migrate --check

// Migrate
$ veryl migrate
```

## Change dependency syntax {{ pr(id="1373") }}

The notation of `[dependencies]` section in `Veryl.toml` is changed.
This is for multiple project support in a repository. 

```toml
# Before
"https://github.com/veryl-lang/sample" = "0.1.0"

# After
veryl_sample = {github = "veryl-lang/veryl_sample", version = "0.1.0"}
```

## Remove `export` declaration / `ref` direction {{ pr(id="1367") }} {{ pr(id="1351") }}

Veryl compiler can't resolve symbols correctly through `export` declaration, so it is removed until the reasonable use case is found.

`ref` direction is removed because it can't be used in synthesizable RTL.

# New Language Features

## Introduce `connect` operation {{ pr(id="1423") }}

To simplify connection between interface, `connect` operation is introduced.
All members of the interface are connected automatically.

```veryl
module ModuleA (
    mst_if: modport InterfaceA::master,
    slv_if: modport InterfaceA::slave ,
) {
    inst bus_if: InterfaceA;

    connect mst_if <> bus_if.slave;
    connect slv_if <> bus_if.master;
}
```

## Struct constructor support {{ pr(id="1418") }}

To initialize struct, Struct constructor can be used instead of assigning each members.
This is especially useful to initialize `const` because it can't be assigned by each members.

`..default` specifier can speficy the default value for unspecified members in the struct.


```veryl
module ModuleA {
    struct Param {
        a: bit<10>,
        b: bit<10>,
    }

    const p: Param = Param'{
        a: 10,
        b: 10,
    };

    const q: Param = Param'{
        a: 1,
        ..default(0) // means `b: 0`
    };
}
```

## Introduce `bool` type {{ pr(id="1389") }}

`bool` is a type alias of `logic<1>` to express boolean.
`true` and `false` literal which express `1'b1` and `1'b0` can be used.

```veryl
module ModuleA {
    const a: bool = true;
    const b: bool = false;
}
```

## Support default clock and reset {{ pr(id="1386") }}

In some cases, there are some clocks, but only single clock is used in all `always_ff`.
For such case, `default` type modifier can be used to specify the default clock and reset explicitly.

```veryl
module ModuleA (
    i_clk   : input clock,
    i_clk_en: input logic,
) {
    let clk: `_ default clock = i_clk & i_clk_en;

    var a: logic;

    always_ff {
        a = 0;
    }
}
```

## Add `same` direction to modport default member {{ pr(id="1381") }}

`same` direction which copies all members of the existing modport can be used. 

```veryl
interface InterfaceA {
    var a: logic;
    var b: logic;
    var c: logic;

    modport master {
        a: output,
        b: input ,
        c: input ,
    }

    modport driver {
        b: output,
        ..same(master)
    }
}
```

## Support module / interface / package alias {{ pr(id="1342") }} {{ pr(id="1374") }}

To shorten long item with many generic parameters, `alias` can be used.

```veryl
package PkgA::<X: const, Y: const, Z: const> {}

alias package PkgA123 = PkgA::<1, 2, 3>;
```

## Introduce proto package {{ pr(id="1336") }}

As generic bound, proto package can be used.

```veryl
proto package ProtoA {
    type data_a;
    type data_b;
}

package PackageA::<A: const, B: const> for ProtoA {
    type data_a = logic<A>;
    type data_b = logic<B>;
}

module ModuleA::<PKG: ProtoA> {
    let _a: PKG::data_a = 0;
}
```

## Function call with named argument {{ pr(id="1452") }}

Function call with named arguments can be used to make easy to see function with many arguments.

```veryl
module ModuleA {
    function FunctionA (
        a: input logic,
        b: input logic,
        c: input logic,
        d: input logic,
    ) {}

    let _a: logic = FunctionA(
        a: 1,
        b: 1,
        c: 1,
        d: 1,
    );
}
```

# New Tool Features

## `.build` directory

`.build` directory to store build related information is created after `veryl build`.
We recommend to add the following entry to your `.gitignore`.

```
.build/
```

## Add waveform format option / Implement waveform for cocotb {{ pr(id="1388") }}

To specify waveform format, `waveform_format` field in `Veryl.toml` is added.
Waveform dump support for cocotb is added too.

```toml
[test]
waveform_format = "vcd"  # or "fst"
```

## Add `--check` option for `veryl build` {{ pr(id="1348") }}

`veryl build --check` can be used to check whether the generated files will be changed.

## Create git repo and default `.gitignore` at `veryl new/init` {{ pr(id="1437") }}

If `git` command is available, `veryl new` and `veryl init` initialize the project directory as git repository, and put the default `.gitignore`.

## Add `fmt(compact)` attribute {{ pr(id="1335") }}

`fmt(compact)` attribute enables compact formatting without newlines.

```veryl
module ModuleA {
    #[fmt(compact)]
    {
        inst u1: $sv::Module #( A: 1, B: 2 ) ( x: 1, y: _ );
        inst u2: $sv::Module #( A: 1, B: 2 ) ( x: 1, y: _ );
        inst u3: $sv::Module #( A: 1, B: 2 ) ( x: 1, y: _ );
        inst u4: $sv::Module #( A: 1, B: 2 ) ( x: 1, y: _ );
    }
}
```

# Other Changes

Check out everything that changed in [Release v0.15.0](https://github.com/veryl-lang/veryl/releases/tag/v0.15.0).
