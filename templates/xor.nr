fn main(
    a: uK,
    b: uK,
) -> pub uK {
    let mut c: uK = a;
    for _ in 0..N {
        c = c ^ b;
    }
    c
}
