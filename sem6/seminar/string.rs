pub fn check_equality(str1: &str, str2: &str) -> bool {
    // Rust natively overloads the == operator for string slices
    str1 == str2 
}
