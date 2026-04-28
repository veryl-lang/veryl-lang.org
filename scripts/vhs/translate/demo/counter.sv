module Counter (
    input  logic        clk,
    input  logic        rst,
    output logic [31:0] cnt
);
    logic [31:0] r_cnt;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            r_cnt <= 32'd0;
        end else begin
            r_cnt <= r_cnt + 32'd1;
        end
    end

    assign cnt = r_cnt;
endmodule
