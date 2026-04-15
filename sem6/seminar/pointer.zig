fn getValue(closure: *Closure) Value {
    // Zig pointers share the same clean ergonomics as safe slices
    return closure.upvalues[1];
}
