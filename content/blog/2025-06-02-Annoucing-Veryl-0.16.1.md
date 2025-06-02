+++
title = "Announcing Veryl 0.16.1"
+++

The Veryl team has published a new release of Veryl, 0.16.1.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Language Features

## Support flattened array modport/instance {{ pr(id="1566") }}

Some EDA tools don't support multi-dimentional array modport/instance.
To support such tools, `flatten_array_interface` can be used.

```toml
[build]
flatten_array_interface = true
```

The following is an example of code generation.

* Veryl

```veryl
inst if_a: InterfaceA[2, 3];
```

* SystemVerilog

```verilog
InterfaceA if_a[6]();
```

## Add a build option to hashed mangle-name {{ pr(id="1614") }}

If an generic instance has many arguments, the mangled name becomes too long.
To shorten such names, `hashed_mangled_name` can be used.

```toml
[build]
hashed_mangled_name = true
```

Example:

* Un-hashed name: `prj___PkgA__0__1__2__3__4__5__6__7`
* Hashed name: `prj___PkgA__3894375d1deadabb`

# Other Changes

Check out everything that changed in [Release v0.16.1](https://github.com/veryl-lang/veryl/releases/tag/v0.16.1).
