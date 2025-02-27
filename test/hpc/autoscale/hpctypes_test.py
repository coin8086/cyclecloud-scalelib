from hpc.autoscale.hpctypes import Memory, add_magnitude_conversion


def test_memory() -> None:
    m = Memory.value_of
    a = m("100g")
    b = m("10g")
    a -= b * 10
    assert m("110g") == m("100g") + m("10g")
    assert m("110g") == m("100g") + (10 * 1024 ** 3)
    assert m("90g") == m("100g") - m("10g")
    assert m("90g") == m("100g") - (10 * 1024 ** 3)
    assert m("90g") == m("100g") - (10.0 * 1024 ** 3)
    assert m("10b") == m("100g") / (10 * 1024 ** 3)
    assert m("20g") == m("100g") / m("5g")
    assert m("33g") == m("100g") // 3
    assert 1024 ** 3 * (100 / 3.0) == m("100g") / 3

    assert m("100g") == m("102400m").convert_to("g")
    assert m("102400m") == m("100g").convert_to("m")
    assert m("100g") == m("100g").convert_to("m").convert_to("g")

    assert m("100g") > m("100k")
    assert m("100k") < m("100g")

    assert m("100g") // 9.99 == m("10g")
    assert m("100g") // 10.01 == m("9g")

    # allow schedulers to add custom conversion
    add_magnitude_conversion("kw", 8 * 1024)
    assert m("2kw") == m("16k")
