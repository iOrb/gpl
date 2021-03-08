
def all_instances(indexes):
    instances = {
        0: "two_pile_nim/layout_2x10_0.json",
        1: "two_pile_nim/layout_2x11_0.json",
        2: "two_pile_nim/layout_2x12_0.json",
        3: "two_pile_nim/layout_2x13_0.json",
        4: "two_pile_nim/layout_2x14_0.json",
        5: "two_pile_nim/layout_2x16_0.json",
        6: "two_pile_nim/layout_2x16_1.json",
        7: "two_pile_nim/layout_2x17_0.json",
        8: "two_pile_nim/layout_2x18_0.json",
        9: "two_pile_nim/layout_2x19_0.json",
        10: "two_pile_nim/layout_2x2_1.json",
        11: "two_pile_nim/layout_2x3_0.json",
        12: "two_pile_nim/layout_2x3_1.json",
        13: "two_pile_nim/layout_2x3_2.json",
        14: "two_pile_nim/layout_2x4_0.json",
        15: "two_pile_nim/layout_2x5_0.json",
        16: "two_pile_nim/layout_2x5_1.json",
        17: "two_pile_nim/layout_2x5_2.json",
        18: "two_pile_nim/layout_2x6_0.json",
        19: "two_pile_nim/layout_2x7_0.json",
        20: "two_pile_nim/layout_2x7_1.json",
        21: "two_pile_nim/layout_2x2_0.json",
    }
    if indexes=='a':
        return list(instances.values())

    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list