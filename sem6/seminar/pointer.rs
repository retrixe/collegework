unsafe fn get_value(closure: *mut Closure) -> Value {
    // Raw pointers lack indexing ergonomics and bounds checking
    *(*closure).upvalues.offset(1)
}
