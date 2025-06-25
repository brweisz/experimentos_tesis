fn main(
    a: [Field; N],
) -> pub Field {
    let mut acc: Field = 0;
    for i in 0..N {
        acc += a[i];
        acc *= a[i];
    }
    acc
}

