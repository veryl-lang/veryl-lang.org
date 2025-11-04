+++
title = "Announcing Veryl 0.17.0"
+++

The Veryl team has published a new release of Veryl, 0.17.0.
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

## Remove `===` and `!==` operator {{ pr(id="2006") }}

`===` and `!==` operator are removed because they are not synthesizable.
Please use `==` and `!=` instead of them.

## Remove `^~` operator {{ pr(id="2008") }}

Both `~^` and `^~` was XNOR operator.
Now `^~` operator is removed and XNOR operator is `~^`.
This change improves consistency with NAND (`~&`) and NOR (`~|`) operator.
After this change, `^~` is interpreted as combination of `^` and `~` like below.

```veryl
x ^~ y // x XOR (NOT y)
^~ x   // Reduction XOR (NOT x)
```

# New Tool Features

## Add cocotb 2.0 support {{ pr(id="1958") }}

[Cocotb 2.0](https://docs.cocotb.org/en/development/upgrade-2.0.html) has been released and we have added support for it in `veryl test`.

# Information

## DOI of Veryl release

After this version, DOI (Digital Object Identifier) is added to all Veryl release.
If you refer Veryl in your paper, please use the following DOI.

* Concept DOI: [https://doi.org/10.5281/zenodo.17518832](https://doi.org/10.5281/zenodo.17518832)
* v0.17.0 DOI: [https://doi.org/10.5281/zenodo.17518833](https://doi.org/10.5281/zenodo.17518833)

# Other Changes

Check out everything that changed in [Release v0.17.0](https://github.com/veryl-lang/veryl/releases/tag/v0.17.0).
