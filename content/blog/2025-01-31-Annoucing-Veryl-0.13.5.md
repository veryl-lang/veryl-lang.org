+++
title = "Announcing Veryl 0.13.5"
+++

The Veryl team has published a new release of Veryl, 0.13.5.
Veryl is a new hardware description language as an alternate to SystemVerilog.

If you have a previous version of Veryl installed via `verylup`, you can get the latest version with:

```
$ verylup update
```

If you don't have it already, you can get `verylup` from [release page](https://github.com/veryl-lang/verylup/releases/latest).

# New Features

## Support to override dependencies with local path {{ pr(id="1206") }}

Sometimes, using dependencies of locally modified version becomes necessary.
In the case, overriding dependencies by local path can be used like below:

```toml
[dependencies]
"https://github.com/veryl-lang/sample" = {version = "0.1.0", path = "../sample"}
```

This means that if there is `../sample`, it is used, and if not, it is pulled from the Git repository.

## Introduce inst generic boundary {{ pr(id="1192") }}

Now instance can be spacified as generics boundary.
The boundary is written like `inst X`.

```veryl
module ModuleA {
    function FuncA::<IF: inst InterfaceA> () -> logic {
        return IF.a;
    }

    inst u: InterfaceA;
    let x: logic = FuncA::<u>();
}

interface InterfaceA {
    var a: logic;
}
```

# Other Changes

Check out everything that changed in [Release v0.13.5](https://github.com/veryl-lang/veryl/releases/tag/v0.13.5).
