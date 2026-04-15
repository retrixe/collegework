const Instance = struct {
    val: i32,

    // Methods are just functions that take `self` as the first parameter
    fn method(self: *Instance) void { 
        self.val += 1; 
    }
};

// Inside the hot loop:
// instance.method();
