struct Instance { val: i32 }

impl Instance {
    #[inline(never)]
    fn method(&mut self) { 
        self.val += 1; 
    }
}

// Inside the hot loop:
// instance.method();
