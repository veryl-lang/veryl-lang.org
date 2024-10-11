+++
title = "Announcing Veryl 0.13.0"
+++

The Veryl team has published a new release of Veryl, 0.13.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Breaking Changes

## Bounded generic parameter {{ pr(id="917") }}

Until Veryl 0.13.0, generic parameter couldn't have any restriction.
So Veryl compiler couldn't judge whether the passed parameter is correct at the instantiation,
and it generated the complicated error message.

```veryl
module ModuleA {
    inst u: GenericModule::<X /* X is OK??? */> (
    };
}
```

Veryl 0.13.0 adds the following bounds to generic parameter.

* `const`
* `type`
* module prototype

`const` means a constant value, `type` means any type. The example `const` and `type` is below:


```veryl
// Generic module with const generic parameter
module ModuleA::<X: const> {
}

// Generic module with type generic parameter
module ModuleB::<X: type> {
}
```

Module prototype is more complicated, it shows what a module for the generic parameter should has as parameters and ports.
The following `ProtoA` shows a module should have `A` and `i_clk`, and `ModuleA` satisfies the restriction.
So `ModuleA` can be used as generic parameter of `ModuleB` which is bounded by `ProtoA`.

```veryl
// Module prorotype
proto ProtoA #(
    param A: u32 = 1,
) (
    i_clk: input clock,
);

// ModuleA satisfies ProtoA
module ModuleA for ProtoA #(
    param A: u32 = 1,
) (
    i_clk: input clock,
) {
}

// Generic module with module prototype
module ModuleB::<X: ProtoA> {
}

module ModuleC {
    // ModuleA can be used as the generic parameter
    inst u: ModuleB::<ModuleA>;
}
```

## Change from `std` to `$std` {{ pr(id="930") }}

Veryl 0.13.0 change the namespace of standard library from `std` to `$std`.
This is because it clears that it is built-in namespace, and reduces conflict with general identifiers.

## Change `local` to `const` {{ pr(id="932") }}

`local` keyword is derived from `localparam` of SystemVerilog.
The naming is confusable becasue `local` looks "local scoped" and actually `local` of package can be seen globally.
So Veryl 0.13.0 changes `local` to `const` because `const` is used for this usage in general programming languages.

```veryl
module #(
    param X: u32 = 1    ,
    const Y: u32 = X + 1,
) {
    const Z: u32 = 1;
}
```

# New Features

## Support untyped enum declaration {{ pr(id="902") }}

If the type is omitted in enum declaration, Veryl compiler inserts appropriate type automatically.

```veryl
enum A {
  FOO,
  BAR,
  BAZ,
}

// This is equivalence with the above code
enum A: logic<2> {
  FOO,
  BAR,
  BAZ,
}
```

## Mermaid support for documentation comment {{ pr(id="904") }}

[Mermaid](https://mermaid.js.org) is syntax to write diagrams.
If ```` ```mermaid ```` is used in documentation comment, the code block is interpreted as Mermaid,
and the generated diagram is shown in documentation.

```veryl
/// ```mermaid
/// graph TD;
///     A-->B;
///     A-->C;
///     B-->D;
///     C-->D;
/// ```
```

## Add `enum_encoding` attribute {{ pr(id="915") }}

Encoding of variant values in enum can be specified through `enum_encoding` attribute.
The available encodings are `sequential`, `onehot` and `gray`.

```veryl
#[enum_encoding(sequential)]
enum A {
  FOO,
  BAR,
}

#[enum_encoding(onehot)]
enum B {
  FOO,
  BAR,
}

#[enum_encoding(gray)]
enum C {
  FOO,
  BAR,
}
```

## Completion of modport and struct member {{ pr(id="934") }}

`veryl-ls` supports completion of modport and struct member.

```veryl
struct A {
    x: logic,
    y: logic,
}

var a: A;
let b: logic = a.
//              | `x` and `y` will be listed as completion candidates at inputting this period
```

# Other Changes

Check out everything that changed in [Release v0.13.0](https://github.com/veryl-lang/veryl/releases/tag/v0.13.0).
