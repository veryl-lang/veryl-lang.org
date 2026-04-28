```veryl
/// Selects one of two input data buses.
module DataSelector #(
    param Width: u32 = 8,
) (
    i_clk : input  clock           , // dedicated clock type
    i_rst : input  reset           , // dedicated reset type
    i_sel : input  logic           ,
    i_data: input  logic<Width> [2], // [] = unpacked array
    o_data: output logic<Width>    , // <> = packed array
) {
    var r_data: logic<Width>;

    // a lone clock/reset can be omitted from `always_ff`
    always_ff {
        // `if_reset` hides reset polarity (sync/async, neg/pos)
        if_reset {
            r_data = 0;
        } else if i_sel {
            r_data = i_data[0];
        } else {
            r_data = i_data[1];
        }
    }

    assign o_data = r_data;
}
```
