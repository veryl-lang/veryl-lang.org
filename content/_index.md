+++
title = "Veryl Hardware Description Language"
sort_by = "weight"
+++

# Concept

Veryl is a hardware description language based on SystemVerilog, providing the following advantages:

## __Optimized Syntax__
Veryl adopts syntax optimized for logic design while being based on a familiar basic syntax for SystemVerilog experts.
This optimization includes guarantees for synthesizability, ensuring consistency between simulation results, and providing numerous syntax simplifications for common idioms.
This approach enables ease of learning, improves the reliability and efficiency of the design process, and facilitates ease of code writing.

## __Interoperability__
Designed with interoperability with SystemVerilog in mind, Veryl allows smooth integration and partial replacement with existing SystemVerilog components and projects.
Furthermore, SystemVerilog source code transpiled from Veryl retains high readability, enabling seamless integration and debugging.

## __Productivity__
Veryl comes with a rich set of development support tools, including package managers, build tools, real-time checkers compatible with major editors such as VSCode, Vim, Emacs, automatic completion, and automatic formatting.
These tools accelerate the development process and significantly enhance productivity.

With these features, Veryl provides powerful support for designers to efficiently and productively conduct high-quality hardware design.

# Code Examples

## Module Definition

```veryl
// module definition
module ModuleA #(
    param ParamA: u32 = 10,
    const ParamB: u32 = 10, // trailing comma is allowed
) (
    i_clk : input  clock            , // `clock` is a special type for clock
    i_rst : input  reset            , // `reset` is a special type for reset
    i_sel : input  logic            ,
    i_data: input  logic<ParamA> [2], // `[]` means unpacked array in SystemVerilog
    o_data: output logic<ParamA>    , // `<>` means packed array in SystemVerilog
) {
    // const parameter declaration
    //   `param` is not allowed in module
    const ParamC: u32 = 10;

    // variable declaration
    var r_data0: logic<ParamA>;
    var r_data1: logic<ParamA>;
    var r_data2: logic<ParamA>;

    // value binding
    let _w_data2: logic<ParamA> = i_data;

    // always_ff statement with reset
    //   `always_ff` can take a mandatory clock and a optional reset
    //   `if_reset` means `if (i_rst)`. This conceals reset porality
    //   `()` of `if` is not required
    //   `=` in `always_ff` is non-blocking assignment
    always_ff (i_clk, i_rst) {
        if_reset {
            r_data0 = 0;
        } else if i_sel {
            r_data0 = i_data[0];
        } else {
            r_data0 = i_data[1];
        }
    }

    // always_ff statement without reset
    always_ff (i_clk) {
        r_data1 = r_data0;
    }

    // clock and reset can be omitted
    // if there is a single clock and reset in the module
    always_ff {
        r_data2 = r_data1;
    }

    assign o_data = r_data1;
}
```

## Interface Definition

```veryl
// interface definition
interface InterfaceA #(
    param ParamA: u32 = 1,
    param ParamB: u32 = 1,
) {
    const ParamC: u32 = 1;

    var a: logic<ParamA>;
    var b: logic<ParamA>;
    var c: logic<ParamA>;

    // modport definition
    modport master {
        a: input ,
        b: input ,
        c: output,
    }

    modport slave {
        a: input ,
        b: input ,
        c: output,
    }
}

module ModuleA (
    i_clk: input clock,
    i_rst: input reset,
    // port declaration by modport
    intf_a_mst: modport InterfaceA::master,
    intf_a_slv: modport InterfaceA::slave ,
) {
    // interface instantiation
    inst u_intf_a: InterfaceA [10];
}
```

## Package Definition

```veryl
// package definition
package PackageA {
    const ParamA: u32 = 1;
    const ParamB: u32 = 1;

    function FuncA (
        a: input logic<ParamA>,
    ) -> logic<ParamA> {
        return a + 1;
    }
}

module ModuleA {
    let a : logic<10> = PackageA::ParamA;
    let _b: logic<10> = PackageA::FuncA(a);
}
```

# Features

## Real-time diagnostics {#real-time-diagnostics}

Issues such as undefined, unused, or unassigned variables are notified in real-time while editing in the editor.
In the following example, adding the `_` prefix to variables flagged as unused explicitly indicates their unused status, suppressing warnings.

![Real-time diagnostics demo](./img/diagnostics.gif)

## Auto formatting {#auto-formatting}

In addition to the automatic formatting feature integrated with the editor,
formatting through the command line and formatting checks in CI are also possible.

![Auto formatting demo](./img/format.gif)

## Integrated test {#integrated-test}

Testbenches can be written directly in Veryl using its native testbench syntax,
and executed through the `veryl test` command.
`$tb::clock_gen` and `$tb::reset_gen` provide clock and reset generation,
and `initial` blocks describe test scenarios.
Individual tests can be skipped with the `#[ignore]` attribute.

```veryl
#[test(test_counter)]
module test_counter {
    inst clk: $tb::clock_gen;
    inst rst: $tb::reset_gen (
        clk: clk,
    );

    var cnt: logic<32>;

    inst dut: Counter (
        clk: clk,
        rst: rst,
        cnt: cnt,
    );

    initial {
        rst.assert(clk);
        clk.next  (10);
        $assert   (cnt == 32'd10);
        $finish   ();
    }
}
```

```console
$ veryl test
[INFO ]    Executing test (test_counter)
[INFO ]    Succeeded test (test_counter)
[INFO ]    Completed tests : 1 passed, 0 failed
```

Existing test code written in SystemVerilog or [cocotb](https://www.cocotb.org)
can also be embedded in Veryl code as a fallback.

```veryl
#[test(test1)]
embed (inline) sv{{{
    module test1;
        initial begin
            assert (0) else $error("error");
        end
    endmodule
}}}
```

## Dependency management {#dependency-management}

Veryl includes a built-in dependency management feature,
allowing for easy incorporation of libraries by simply adding the repository path and version of the library on project settings like below.

```toml
[dependencies]
"https://github.com/veryl-lang/sample" = "0.1.0"
```

## Standard library {#standard-library}

Veryl ships a standard library providing generic interface and package definitions for common bus protocols.
Parameterize the package once, then reuse the interface across modules.

```veryl
alias package axi3_pkg = $std::axi3_pkg::<32, 4, 8>;

module ModuleA (
    slv_if: modport $std::axi3_if::<axi3_pkg>::slave,
) {}
```

The standard library currently includes AXI3, AXI4, AXI4-Lite, and AXI-Stream interfaces.
See the [standard library reference](https://std.veryl-lang.org) for the full list.

## Generics {#generics}

Code generation through generics achieves more reusable code than traditional parameter override.
Parameters in function like the following example, but also module names of instantiation, type names of struct definition, and so on can be parameterized.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
function automatic logic [20-1:0] FuncA_20 (
    input logic [20-1:0] a
);
    return a + 1;
endfunction

function automatic logic [10-1:0] FuncA_10 (
    input logic [10-1:0] a
);
    return a + 1;
endfunction

logic [10-1:0] a;
logic [20-1:0] b;
always_comb begin
    a = FuncA_10(1);
    b = FuncA_20(1);
end
```

</td>
<td>

```veryl
function FuncA::<T: const> (
    a: input logic<T>,
) -> logic<T> {
    return a + 1;
}

var a: logic<10>;
var b: logic<10>;
always_comb {
    a = FuncA::<10>(1);
    b = FuncA::<20>(1);
}
```
 
</td>
</tr>
</table>

## Integer types {#integer-types}

In addition to `u32` / `i32` / `u64` / `i64`, Veryl provides fixed-width primitive types
`u8`, `u16`, `i8`, `i16` for smaller bit widths, and `p8`, `p16`, `p32`, `p64` for
positive-only integers (restricted to non-negative values).

```veryl
let a: u8  = 0;
let b: u16 = 0;
let c: i8  = 0;
let d: i16 = 0;

module ModuleA {
    const X: p32 = 10;
}
```

## Inferable enum width {#inferable-enum-width}

When the base type of an `enum` is omitted, it previously defaulted to `logic`.
A new syntax lets you specify the base type while still inferring its width from the variants.

```veryl
enum A: bit<_> {
   X,
   Y,
}

enum B: logic<_> {
   X,
   Y,
}
```

## Global function {#global-function}

Functions can be defined at the project root, outside of `module`, `interface`, and `package`.
Global functions support generic type parameters and can be exposed with `pub`.

```veryl
pub function add::<W: u32> (
    a: input logic<W>,
    b: input logic<W>,
) -> logic<W> {
    return a + b;
}

module ModuleA #(
    param WIDTH: u32 = 8,
) (
    i_a: input  logic<WIDTH>,
    i_b: input  logic<WIDTH>,
    o_c: output logic<WIDTH>,
) {
    assign o_c = add::<WIDTH>(i_a, i_b);
}
```

## Clock Domain Annotation {#clock-domain-annotation}

If there are some clocks in a module, explicit clock domain annotation and `unsafe (cdc)` block at the clock domain boundaries are required.
By the annotation, Veryl compiler detects unexpected clock domain crossing as error, and explicit `unsafe (cdc)` block eases to review clock domain crossing.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
module ModuleA (
    input  i_clk_a,
    input  i_dat_a,
    output o_dat_a,
    input  i_clk_b,
    input  i_dat_b,
    output o_dat_b
);
    // Carefully!!!
    // From i_clk_a to i_clk_b
    assign o_dat_b = i_dat_a;
endmodule
```

</td>
<td>

```veryl
module ModuleA (
    i_clk_a: input  `a clock,
    i_dat_a: input  `a logic,
    i_dat_a: output `a logic,
    i_clk_b: input  `b clock,
    i_dat_b: input  `b logic,
    i_dat_b: output `b logic,
) {
    unsafe (cdc) {
        assign o_dat_b = i_dat_a;
    }
}
```
 
</td>
</tr>
</table>

Variables without explicit clock domain annotation can be inferred from their context.
For example, when a variable is assigned from a signal with a known clock domain, the variable's domain is automatically inferred.

```veryl
module ModuleA (
    i_clk_a: input  'a clock,
    i_rst_a: input  'a reset,
    i_dat_a: input  'a logic,
    o_dat_a: output 'a logic,
) {
    var x: logic;
    assign x = i_dat_a;   // x is inferred as 'a domain
    assign o_dat_a = x;
}
```

## Abstraction of clock and reset {#abstraction-of-clock-and-reset}

There is no need to specify the polarity and synchronicity of the clock and reset in the syntax;
these can be specified during build-time configuration.
This allows generating code for both ASICs with negative asynchronous reset
and FPGAs with positive synchronous reset from the same Veryl code.

Additionally, explicit `clock` and `reset` type enables to check whether clock and reset are correctly connected to registers.
If there is a single clock and reset in the module, the connection can be omitted.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
module ModuleA (
    input logic i_clk,
    input logic i_rst_n
);

always_ff @ (posedge i_clk or negedge i_rst_n) begin
    if (!i_rst_n) begin
    end else begin
    end
end

endmodule
```

</td>
<td>

```veryl
module ModuleA (
    i_clk: input clock,
    i_rst: input reset,
){
    always_ff {
        if_reset {
        } else {
        }
    }
}
```
 
</td>
</tr>
</table>

## Visibility control {#visibility-control}

Modules without the `pub` keyword cannot be referenced from outside the project
and are not included in automatic documentation generation.
This allows distinguishing between what should be exposed externally from the project and internal implementations.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
module ModuleA;
endmodule

module ModuleB;
endmodule
```

</td>
<td>

```veryl
pub module ModuleA {
}

module ModuleB {
}
```
 
</td>
</tr>
</table>

## Documentation comment {#documentation-comment}

Writing module descriptions as documentation comments allows for automatic documentation generation.
You can use not only plain text but also the following formats:

* [Markdown](https://www.markdownguide.org)
* Waveform using [WaveDrom](https://wavedrom.com)
* Diagram using [Mermaid](https://mermaid.js.org)

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
// Comment
module ModuleA;
endmodule
```

</td>
<td>

```veryl
/// Documentation comment written by Markdown
///
/// * list
/// * list
/// 
/// ```wavedrom
/// { signal: [{ name: "Alfa", wave: "01.zx=ud.23.456789" }] }
/// ```
module ModuleA {
}
```
 
</td>
</tr>
</table>

## `let` statement {#let-statement}

There is a dedicated `let` statement available for binding values simultaneously with variable declaration,
which can be used in various contexts that were not supported in SystemVerilog.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
logic tmp;
always_ff @ (posedge i_clk) begin
    tmp = b + 1;
    x <= tmp;
end
```

</td>
<td>

```veryl
always_ff {
    let tmp: logic = b + 1;
    x = tmp;
}
```
 
</td>
</tr>
</table>

## `if` / `case` expression {#if--case-expression}

By adopting `if` and `case` expressions instead of the ternary operator,
readability improves, especially when comparing a large number of items.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
logic a;
assign a = X == 0 ? Y0 :
           X == 1 ? Y1 :
           X == 2 ? Y2 : 
                    Y3;
```

</td>
<td>

```veryl
var a: logic;
assign a = case X {
    0      : Y0,
    1      : Y1,
    2      : Y2,
    default: Y3,
};
```
 
</td>
</tr>
</table>

## Range-based `for` / `inside` / `outside` {#range-based-for--inside--outside}

With notation representing closed intervals `..=` and half-open intervals `..`,
it is possible to uniformly describe ranges using `for`, `inside`, and `outside` (which denotes the inverse of `inside`).

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
for (int i = 0; i < 10; i++) begin
    a[i] =   X[i] inside {[1:10]};
    b[i] = !(X[i] inside {[1:10]});
end
```

</td>
<td>

```veryl
for i: u32 in 0..10 {
    a[i] = inside  X[i] {1..=10};
    b[i] = outside X[i] {1..=10};
}
```
 
</td>
</tr>
</table>

## `<>` operator {#connect-operator}

`<>` operator can connect two interfaces. It simplifies SystemVerilog's interface connection requiring each member assignments.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
always_comb begin
    mst_if0.cmd   = bus_if0.cmd;
    bus_if0.ready = mst_if0.ready;
end

always_comb begin
    mst_if1.cmd   = bus_if1.cmd;
    bus_if1.ready = mst_if1.ready;
end
```

</td>
<td>

```veryl
connect mst_if0 <> bus_if0.slave;

always_comb {
    mst_if1 <> bus_if1.slave;
}
```

</td>
</tr>
</table>

## Trailing comma {#trailing-comma}

Trailing comma is a syntax where a comma is placed after the last element in a list.
It facilitates the addition and removal of elements and reduces unnecessary differences in version control systems.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
module ModuleA (
    input  a,
    input  b,
    output o
);
endmodule
```

</td>
<td>

```veryl
module ModuleA (
    a: input  logic,
    b: input  logic,
    o: output logic,
) {
}
```
 
</td>
</tr>
</table>

## Named block {#named-block}

You can define named blocks to limit the scope of variables.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
if (1) begin: BlockA
end
```

</td>
<td>

```veryl
:BlockA {
}
```
 
</td>
</tr>
</table>

## `msb` notation {#msb-notation}

The `msb` notation, indicating the most significant bit, eliminates the need to calculate the most significant bit from parameters, making intentions clearer.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
logic a;
logic [WIDTH-1:0] X;
assign a = X[WIDTH-1];
```

</td>
<td>

```veryl
var a: logic;
var X: logic<WIDTH>;
assign a = X[msb];
```
 
</td>
</tr>
</table>

## `repeat` of concatenation {#repeat-of-concatenation}

By adopting the explicit `repeat` syntax as a repetition description in bit concatenation,
readability improves over complex combinations of `{}`.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
logic [31:0] a;
assign a = {{2{X[9:0]}}, {12{Y}}};
```

</td>
<td>

```veryl
var a: logic<32>;
assign a = {X[9:0] repeat 2, Y repeat 12};
```
 
</td>
</tr>
</table>

## Compound assignment operator in `always_ff` {#compound-assignment-operator-in-always_ff}

There is no dedicated non-blocking assignment operator;
within `always_ff`, non-blocking assignments are inferred, while within `always_comb`, blocking assignments are inferred.
Therefore, various compound assignment operators can be used within `always_ff` just like within `always_comb`.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
always_ff @ (posedge i_clk) begin
    if (a) begin
        x <= x + 1;
    end
end
```

</td>
<td>

```veryl
always_ff {
    if a {
        x += 1;
    }
}
```
 
</td>
</tr>
</table>

## Individual namespace of enum variant {#individual-namespace-of-enum-variant}

Variants of an enum are defined within separate namespaces for each enum,
thus preventing unintended name collisions.

<table class="sv-compare">
<tr>
<th>SystemVerilog</th>
<th>Veryl</th>
</tr>
<tr>
<td>

```verilog
typedef enum logic[1:0] {
    MemberA,
    MemberB
} EnumA;

EnumA a;
assign a = MemberA;
```

</td>
<td>

```veryl
enum EnumA: logic<2> {
    MemberA,
    MemberB
}

var a: EnumA;
assign a = EnumA::MemberA;
```
 
</td>
</tr>
</table>
