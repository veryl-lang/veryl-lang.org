+++
title = "Announcing Veryl 0.14.0"
+++

The Veryl team has published a new release of Veryl, 0.14.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Breaking Changes

## New type checker {{ pr(id="1216") }} {{ pr(id="1239") }} {{ pr(id="1240") }} {{ pr(id="1264") }}

New type checker is introduced to enable the following checks.

* Mismatch in array dimensions during assignment
* Assigning a 4-state value to a 2-state type
* Out-of-range selection for arrays or bits
* Interface mismatch during port connection

Please see the following blog for the detailed information.

[https://veryl-lang.org/blog/new-type-checker/](https://veryl-lang.org/blog/new-type-checker/)

This is not a breaking chage ideally, but the existing code may be broken by mistakes of new checker.
If there is any mistake, please open an [issue](https://github.com/veryl-lang/veryl/issues).


## Remove variable declaration from package {{ pr(id="1305") }}

Variable declaration in package is removed because it is not synthesizable.

```veryl
package PackageA {
    var X: logic; // Error
}
```

# New Features

## LSP support for file renaming and deleting {{ pr(id="1226") }}

veryl-ls becomes to support file renaming and deleting to avoid unexpected errors caused by these file operation.

## Support clock domain annotation for interface instance {{ pr(id="1279") }}

Interface instances can have clock domain annotation as the same as normal variables.

```veryl
var x: `a logic;

inst intf: `a InterfaceA;
```

## Add `align` attribute {{ pr(id="1283") }}

To improve readability of complex expression, `align` attribute was added.
For example, by adding `#[align(number)]`, all numbers in expression is aligned.

```veryl
module ModuleA {
    #[align(number, identifier)]
    let _c : logic = {
        a  [0 ] repeat 1 , a  [0 ] repeat 1 ,
        aa [1 ] repeat 8 , aa [1 ] repeat 8 ,
        aaa[2 ] repeat 16, aaa[2 ] repeat 16,
    };
}
```

## Support default member of modport {{ pr(id="1288") }}

Default member syntax `..[direction]` is introduced to make modport definition concise.
In most cases, the direction of slave-like modport is converse of master-like modport.
So the special direction `converse([modport_name])` is useful to make clear the definition of master/slave pair.

```veryl
interface InterfaceA {
    var a: logic;
    var b: logic;

    modport master {
        a: output,
        b: input ,
    }

    modport slave {
        ..converse(master)
    }

    modport monitor {
        ..input
    }
```

## Enable `assign` to concatenation {{ pr(id="1298") }}

Concatenation can be used as the left hand side of `assign` declaration.

```veryl
assign {a, b} = 1;
```

# Other Changes

Check out everything that changed in [Release v0.14.0](https://github.com/veryl-lang/veryl/releases/tag/v0.14.0).
