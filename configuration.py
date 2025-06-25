program_families = ["assert_zero", "memory", "range/u8", "range/u16", "range/u32", "xor/u8", "xor/u16", "xor/u32"]
n_values = [1, 10, 100]

# sizes_per_program_family = {
#     "assert_zero": [1000, 10000, 100000, 1000000],
#     "memory": [100, 1000, 10000],
#     "range/u8": [100, 1000, 10000, 100000],
#     "range/u16": [100, 1000, 10000, 100000],
#     "range/u32": [100, 1000, 10000, 100000],
#     "xor/u8": [100, 1000, 10000, 100000],
#     "xor/u16": [100, 1000, 10000, 100000],
#     "xor/u32": [100, 1000, 10000, 100000],
# }

sizes_per_program_family = {
    "assert_zero": [1, 10],
    "memory": [1, 10],
    "range/u8": [1, 10],
    "range/u16": [1, 10],
    "range/u32": [1, 10],
    "xor/u8": [1, 10],
    "xor/u16": [1, 10],
    "xor/u32": [1, 10],
}

basic_implementations = ["noirky2-bits", "noirky2-bits-nozk", "bb"]
implementations_with_variations = ["noirky2-bits", "noirky2-bits-nozk", "bb", "noirky2-limb", "noirky2-limb-nozk"]

backends_per_program_family = {
    "assert_zero": basic_implementations,
    "memory": basic_implementations,
    "range/u8": implementations_with_variations,
    "range/u16": implementations_with_variations,
    "range/u32": implementations_with_variations,
    "xor/u8": implementations_with_variations,
    "xor/u16": implementations_with_variations,
    "xor/u32": implementations_with_variations,
}