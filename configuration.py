program_families = ["assert_zero", "memory", "memory_wide", "range/u8", "range/u16", "range/u32", "xor/u8", "xor/u16", "xor/u32"]

sizes_per_program_family = {
    "assert_zero": [100, 1000, 10000, 100000, 1000000],
    "memory": [100, 500, 1000, 3000],
    "memory_wide": [100, 500, 1000, 3000],
    "range/u8": [1000, 2000, 5000, 10000, 20000],
    "range/u16": [1000, 2000, 5000, 10000, 20000],
    "range/u32": [1000, 2000, 5000, 10000, 20000],
    "xor/u8": [1000, 2000, 5000, 10000, 20000],
    "xor/u16": [1000, 2000, 5000, 10000, 20000],
    "xor/u32": [1000, 2000, 5000, 10000, 20000],
}

basic_implementations = ["noirky2-bits", "noirky2-bits-nozk", "bb"]
implementations_with_variations = ["noirky2-bits", "noirky2-bits-nozk", "bb", "noirky2-limb", "noirky2-limb-nozk"]

backends_per_program_family = {
    "assert_zero": basic_implementations,


    "memory": basic_implementations,
    "memory_wide": basic_implementations,
    "range/u8": implementations_with_variations,
    "range/u16": implementations_with_variations,
    "range/u32": implementations_with_variations,
    "xor/u8": implementations_with_variations,
    "xor/u16": implementations_with_variations,
    "xor/u32": implementations_with_variations,
}