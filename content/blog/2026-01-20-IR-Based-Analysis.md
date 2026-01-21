+++
title = "Semantic Analysis based on Intermediate Representation"
+++

We plan to introduce a new semantic analyzer based on intermediate representation at the next release.
This enables the following features.

* Bit-wise latch / unassign detection
* More detailed type check considering parameter override and generics
* Performance improvement

For example, the new analyzer can detect the following error.

```veryl
var a: logic<2>;
always_comb {
    if x {
        a = 1;
    } else {
        // a[0] is latch error
        a[1] = 1;
    }
}
```

About performance improvement, we got the following results.

* Small testcase (unit tests of Veryl compiler): 448ms to 330ms (+36%)
* Large testcase (A real project with 66K lines): 68s to 14s (+386%)


Additionally, the introduced intermediate representation can be used for native Veryl simulator.
We plan to work on implementing it after releasing the new version.

## Important change

The new analyzer can handle several errors which can't be detected by the previous version.

Some tools, including Verilator, ignore these error, so existing Veryl files may contain this error.
In that case, you'll need to fix your code, as it will no longer compile after an update to the Veryl compiler.

Here are some common errors we see in Veryl code on GitHub:

### Refering before definition

In the following code, `a` is referred before it's definition.

```veryl
let b: logic = a;
var a: logic;
```

The next version Veryl compiler detects the following error.

```
Error: referring_before_definition ()

  × a is referred before it is defined.
   ╭─[.../test.veryl:2:20]
 1 │ module ModuleA {
 2 │     let b: logic = a;
   ·                    ┬
   ·                    ╰── Error location
 3 │     var a: logic;
   ╰────
  help: move definition before reference point
```

### Multiple assignment of interface member

In the following code, `p` is driven by both `u0` and `u1`.
Actually `u0` only drives `p.x` and `u1` only drives `p.y`, so it is not multiple assignment exactly.
However new Veryl compiler treats this case as multiple assignment.
This is because determining multiple assignment depending on the module implementation requires traversing the entire instance hierarchy,
which is expensive and makes the location of the error and the cause of the error far apart, making the error message difficult to interpret.

In this case, you can divide `master` modport into `master_x` and `master_y` to resolve this error.

```veryl
interface InterfaceA {
    var x: logic;
    var y: logic;

    modport master {
        x: output,
        y: output,
    }
}

module ModuleA {
    inst p: InterfaceA;

    inst u0: ModuleB ( p, );
    inst u1: ModuleC ( p, );
}

module ModuleB (
    p: modport InterfaceA::master,
) {
    assign p.x = 0;
}

module ModuleC (
    p: modport InterfaceA::master,
) {
    assign p.y = 0;
}
```

## Release plan

We plan to release the next version including the new analyzer at the beginning of Feb. 2026.
If you want to try it before the release, you can use nightly compiler like below after 2026-01-22 02:00 (UTC).

```
$verylup install nightly
$veryl +nightly --version
veryl 0.17.2-nightly (f63dc84 2026-01-20)
```

The new analyzer may introduce false positive error because it replaces the whole analyzer by new code.
If you find any unexpected behaviour, please open an [issue](https://github.com/veryl-lang/veryl/issues) on GitHub.
