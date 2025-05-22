module AddAndIncrement (a, b, start, product);
    input reg [7:0] a;
    input reg [7:0] b;
    input reg start;
    output reg [15:0] product;
    reg [7:0] count;
    reg clk;
    integer state;

    initial begin
        clk = 0;
        state = 1;
    end

    always begin
        clk = ~clk;
        #5;
    end

    always @(posedge clk) begin
        case (state)

            1: begin
                product <= 0;
                count <= 0;
                if (start == 0) begin
                    state <= 1;
                end else begin
                    state <= 2;
                end
            end

            2: begin
                if (count < b) begin
                        product <= product + a;
                        count <= count + 1;
                        if (count == b) begin
                            state <= 1;
                        end else begin
                            state <= 2;
                        end
                end else begin
                    if (count == b) begin
                        state <= 1;
                    end else begin
                        state <= 2;
                    end
                end
            end

        endcase
    end

endmodule