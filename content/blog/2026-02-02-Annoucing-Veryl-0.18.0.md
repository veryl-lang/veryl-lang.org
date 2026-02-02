+++
title = "Announcing Veryl 0.18.0"
+++

The Veryl team has published a new release of Veryl, 0.18.0.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# Breaking Changes

To migrate some syntax changes, `veryl migrate` can be used:

<details>

```console
// Check how changes will be applied
$ veryl migrate --check

// Migrate
$ veryl migrate
```

</details>

## Allow concatenation assignment in always, and add `block` keyword {{ pr(id="2175") }}

Bit concatenation in left-hand side of `always_comb` and `always_ff` is allowed now.

```veryl
always_comb {
    {a, b} = 1;
}
```

On the other hand, this feature conflicts the existing statement grouping syntax by `{}`.
So new `block` keyword is introduced to avoid the conflicts.

```veryl
always_comb {
    // grouping by `{}` is not allowed
    //{
    //    a = 1;
    //    b = 1;
    //}

    block {
        a = 1;
        b = 1;
    }
}
```

## Split `bool` type to `bbool` and `lbool` types {{ pr(id="2186") }}

Using `bool` in const context caused assigning 4-state variable to 2-state variable because `bool` is type alias of `logic<1>`.

```veryl
const flag: bool = true;
const X: u32 = if flag ? 10 : 20; // 4-state variable is used in const context
```

To avoid this mismatch, `bbool` and `lbool` is introduced instead of `bool`.

* `bbool`: the type alias of `bit<1>`
* `lbool`: the type alias of `logic<1>`

```veryl
const flag: bbool = true;
const X: u32 = if flag ? 10 : 20;
```

# New Language Features

## `#[allow(unassign_variable)]` attribute {{ pr(id="2147") }}

By IR-based semantic analyzer, unassign check was enhanced.
If you want to disable the check, `#[allow(unassign_variable)]` attribute can be used.

```veryl
#[allow(unassign_variable)]
module Module A {
}
```

# New Tool Features

## Introduce IR-based semantic analyzer {{ pr(id="2005") }}

The new IR-based semantic analyzer is introduced.
Please refer the following post for the detailed changes.

[Semantic Analysis based on Intermediate Representation](http://veryl-lang.org/blog/ir-based-analysis/)

# Other Changes

Check out everything that changed in [Release v0.18.0](https://github.com/veryl-lang/veryl/releases/tag/v0.18.0).
