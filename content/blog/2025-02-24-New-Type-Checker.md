+++
title = "New Type Checker"
+++

With the new type checker currently under development, it will become possible to perform various type checks that were previously impossible.
As an initial implementation, the following checks are scheduled to be introduced in the next version:

* Mismatch in array dimensions during assignment
* Assigning a 4-state value to a 2-state type
* Out-of-range selection for arrays or bits
* Interface mismatch during port connection

Furthermore, the Veryl compiler will track parameter overrides across all instances,
including those with recursion, ensuring that it can reliably catch issues that only occur with specific overrides.

For example,

```veryl
module ModuleX #(
    param A: u32 = 1,
) {
    let a : logic<2> = 1;
    let _b: logic<2> = a[A]; // This bit select causes out-of-range error when A > 2
}

module ModuleY #(
    param A: u32 = 1,
) {
    inst u: ModuleX #(A,);
}

module ModuleZ {
    inst u: ModuleY #(A: 3,);
}
```

it will display a warning as follows:

```
Warning: invalid_select (https://doc.veryl-lang.org/book/07_appendix/02_semantic_error.html#invalid_select)

  ⚠ invalid select caused by out of range [3:3] > 2
   ╭─[.../test.veryl:5:24]
 4 │     let a : logic<2> = 1;
 5 │     let _b: logic<2> = a[A]; // This bit select causes out-of-range error when A > 2
   ·                        ──┬─
   ·                          ╰── Error location
 6 │ }
   ╰────
    ╭─[.../test.veryl:11:10]
 10 │ ) {
 11 │     inst u: ModuleX #(A,);
    ·          ┬
    ·          ╰── instantiated at
 12 │ }
    ╰────
    ╭─[.../test.veryl:15:10]
 14 │ module ModuleZ {
 15 │     inst u: ModuleY #(A: 3,);
    ·          ┬
    ·          ╰── instantiated at
 16 │ }
    ╰────
  help:
```

We believe such warnings should ideally be treated as errors.
However, due to the potential for false positives caused by the type checker’s current imperfections,
they will remain warnings until the implementation stabilizes, with plans to upgrade them to errors in the future.

Checks related to bit-width, such as bit-width mismatches during assignment or carry overflow in operations, are ready for implementation.
However, we are still deliberating on the policy regarding which checks should be performed.
Those interested in this issue are encouraged to refer to [the Issue page](https://github.com/veryl-lang/veryl/issues/1257).

The next version, which includes these features, may introduce breaking changes due to significant updates to the checking functionality and is planned to be v0.14.0.
It is scheduled for release within 1-2 weeks, so please look forward to it.
