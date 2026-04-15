const std = @import("std");

pub fn checkEquality(str1:const u8, str2:const u8) bool {
    // Zig has no operator overloading; equality is an explicit standard library call
    return std.mem.eql(u8, str1, str2);
}
