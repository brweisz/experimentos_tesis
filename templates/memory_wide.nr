fn main(
    idx: Field,
    val: Field,
) -> pub Field {
    let mut arr: [Field; N] = [0; N];
    for _ in 0..100 {
        arr[idx] = val;
        assert(arr[idx] == val);
    }
    arr[idx]
}
