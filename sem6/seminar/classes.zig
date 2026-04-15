const Animal = union(enum) {
    Dog: void,
    Cat: void,

    pub fn speak(self: Animal)const u8 {
        return switch (self) { 
           .Dog => "Woof",
           .Cat => "Meow",
        };
    }
};

// Values can be contiguous in memory (no hidden heap boxing)
const zoo = [_]Animal{.{.Dog = {} } };

for (zoo) |animal| {
    _ = animal.speak();
}
