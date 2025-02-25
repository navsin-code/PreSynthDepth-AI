module comparator_3bit (
    input [2:0] A,   // 3-bit input A
    input [2:0] B,   // 3-bit input B
    output A_gt_B,   // Output: A > B
    output A_lt_B,   // Output: A < B
    output A_eq_B    // Output: A == B
);
    
    assign A_gt_B = (A > B) ? 1 : 0;
    assign A_lt_B = (A < B) ? 1 : 0;
    assign A_eq_B = (A == B) ? 1 : 0;

endmodule
