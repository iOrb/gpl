from .utils import compute_instance_filename


def all_instances(indexes):
    instances = {
        0: "checkmate_tactic/layout_10x10_0.json",
        1: "checkmate_tactic/layout_12x5_0.json",
        2: "checkmate_tactic/layout_12x8_0.json",
        3: "checkmate_tactic/layout_12x9_0.json",
        4: "checkmate_tactic/layout_12x9_1.json",
        5: "checkmate_tactic/layout_13x14_0.json",
        6: "checkmate_tactic/layout_13x19_0.json",
        7: "checkmate_tactic/layout_14x14_0.json",
        8: "checkmate_tactic/layout_14x17_0.json",
        9: "checkmate_tactic/layout_15x6_0.json",
        10: "checkmate_tactic/layout_17x10_0.json",
        11: "checkmate_tactic/layout_17x12_0.json",
        12: "checkmate_tactic/layout_18x10_0.json",
        13: "checkmate_tactic/layout_19x10_0.json",
        14: "checkmate_tactic/layout_19x13_0.json",
        15: "checkmate_tactic/layout_2x3_0.json",
        16: "checkmate_tactic/layout_3x3_0.json",
        17: "checkmate_tactic/layout_4x4_0.json",
        18: "checkmate_tactic/layout_5x14_0.json",
        19: "checkmate_tactic/layout_7x16_0.json",
        20: "checkmate_tactic/layout_8x6_0.json",
        21: "checkmate_tactic/layout_9x14_0.json",
        22: "checkmate_tactic/layout_9x9_0.json",
        23: "checkmate_tactic/layout_4x5_0.json",
        24: "checkmate_tactic/layout_3x4_0.json",
        25: "checkmate_tactic/layout_2x2_0.json",
    }
    return select_instances(indexes, instances)


def four_four_instances(indexes):
    instances = {
        0 : "checkmate_tactic/4x4/layout_4x4_0.json",
        1 : "checkmate_tactic/4x4/layout_4x4_1.json",
        2 : "checkmate_tactic/4x4/layout_4x4_2.json",
        3 : "checkmate_tactic/4x4/layout_4x4_3.json",
        4 : "checkmate_tactic/4x4/layout_4x4_4.json",
        5 : "checkmate_tactic/4x4/layout_4x4_5.json",
        6 : "checkmate_tactic/4x4/layout_4x4_6.json",
        7 : "checkmate_tactic/4x4/layout_4x4_7.json",
        8 : "checkmate_tactic/4x4/layout_4x4_8.json",
        9 : "checkmate_tactic/4x4/layout_4x4_9.json",
    }
    return select_instances(indexes, instances)


def break_instances(indexes):
    instances = {
        0: "checkmate_tactic/break_points/bp_layout_5x5_0.json",
        1: "checkmate_tactic/break_points/bp_layout_5x5_1.json",
        2: "checkmate_tactic/break_points/bp_layout_5x5_2.json",
        3: "checkmate_tactic/break_points/bp_layout_5x5_3.json",
        4: "checkmate_tactic/break_points/bp_layout_5x5_4.json",
        5: "checkmate_tactic/break_points/bp_layout_5x5_5.json",
        6: "checkmate_tactic/break_points/bp_layout_5x5_6.json",
        7: "checkmate_tactic/break_points/bp_layout_5x5_7.json",
    }
    return select_instances(indexes, instances)


def select_instances(indexes, instances):
    if indexes == 'a':
        ins = list(instances.values())
    else:
        ins = list()
        for i in indexes:
            ins.append(instances.get(i))

    return compute_instance_filename(ins)



