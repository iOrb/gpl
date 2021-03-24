
def all_instances(indexes):
    instances = {
        0: "stop_the_fall/layout_10x11_0.json",
        1: "stop_the_fall/layout_10x11_1.json",
        2: "stop_the_fall/layout_11x10_0.json",
        3: "stop_the_fall/layout_11x16_0.json",
        4: "stop_the_fall/layout_12x10_0.json",
        5: "stop_the_fall/layout_12x11_0.json",
        6: "stop_the_fall/layout_12x11_1.json",
        7: "stop_the_fall/layout_12x12_0.json",
        8: "stop_the_fall/layout_12x13_0.json",
        9: "stop_the_fall/layout_12x14_0.json",
        10: "stop_the_fall/layout_12x21_0.json",
        11: "stop_the_fall/layout_12x8_0.json",
        12: "stop_the_fall/layout_13x12_0.json",
        13: "stop_the_fall/layout_14x9_0.json",
        14: "stop_the_fall/layout_15x16_0.json",
        15: "stop_the_fall/layout_16x11_0.json",
        16: "stop_the_fall/layout_17x30_0.json",
        17: "stop_the_fall/layout_2x3_0.json",
        18: "stop_the_fall/layout_2x5_0.json",
        19: "stop_the_fall/layout_5x15_0.json",
        20: "stop_the_fall/layout_5x5_0.json",
        21: "stop_the_fall/layout_7x15_0.json",
        22: "stop_the_fall/layout_7x8_0.json",
        23: "stop_the_fall/layout_5x5_1.json",
        24: "stop_the_fall/layout_2x4_0.json",
        25: "stop_the_fall/layout_7x8_1.json",
    }
    if indexes == 'a':
        return list(instances.values())
    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list


def five_five_instances(indexes):
    instances = {
        0: "stop_the_fall/5x5/cfr_layout_5x5_0.json",
        1: "stop_the_fall/5x5/cfr_layout_5x5_1.json",
        2: "stop_the_fall/5x5/cfr_layout_5x5_2.json",
        3: "stop_the_fall/5x5/cfr_layout_5x5_3.json",
        4: "stop_the_fall/5x5/cfr_layout_5x5_4.json",
        5: "stop_the_fall/5x5/cfr_layout_5x5_5.json",
        6: "stop_the_fall/5x5/cfr_layout_5x5_6.json",
        7: "stop_the_fall/5x5/cfr_layout_5x5_7.json",
        8: "stop_the_fall/5x5/cfr_layout_6x6_7.json",
    }
    if indexes == 'a':
        return list(instances.values())
    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list



