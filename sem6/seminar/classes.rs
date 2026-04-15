trait Animal { fn speak(&self) -> &str; }
struct Dog;
impl Animal for Dog { fn speak(&self) -> &str { "Woof" } }

// Requires Box (heap allocation) for dynamic sizes
let zoo: Vec<Box<dyn Animal>> = vec!;

for animal in &zoo {
    animal.speak();
}
