import os
import glob

def all_instances(indexes):
    all_instances = {
        0 : "reach_for_the_star/layout_10x11_0.json",
        1 : "reach_for_the_star/layout_10x6_0.json",
        2 : "reach_for_the_star/layout_10x7_0.json",
        3 : "reach_for_the_star/layout_10x7_1.json",
        4 : "reach_for_the_star/layout_10x7_2.json",
        5 : "reach_for_the_star/layout_10x7_3.json",
        6 : "reach_for_the_star/layout_10x8_0.json",
        7 : "reach_for_the_star/layout_11x6_0.json",
        8 : "reach_for_the_star/layout_12x10_0.json",
        9 : "reach_for_the_star/layout_12x11_0.json",
        10 : "reach_for_the_star/layout_12x6_0.json",
        11 : "reach_for_the_star/layout_12x8_0.json",
        12 : "reach_for_the_star/layout_12x8_1.json",
        13 : "reach_for_the_star/layout_12x8_2.json",
        14 : "reach_for_the_star/layout_12x8_3.json",
        15 : "reach_for_the_star/layout_12x8_4.json",
        16 : "reach_for_the_star/layout_13x7_0.json",
        17 : "reach_for_the_star/layout_13x7_1.json",
        18 : "reach_for_the_star/layout_13x7_2.json",
        19 : "reach_for_the_star/layout_13x8_0.json",
        20 : "reach_for_the_star/layout_15x10_0.json",
        21 : "reach_for_the_star/layout_15x8_0.json",
        22 : "reach_for_the_star/layout_15x9_0.json",
        23 : "reach_for_the_star/layout_15x9_1.json",
        24 : "reach_for_the_star/layout_16x10_0.json",
        25 : "reach_for_the_star/layout_16x9_0.json",
        26 : "reach_for_the_star/layout_19x8_0.json",
        27 : "reach_for_the_star/layout_20x12_0.json",
        28 : "reach_for_the_star/layout_23x12_0.json",
        29 : "reach_for_the_star/layout_25x12_0.json",
        30 : "reach_for_the_star/layout_26x15_0.json",
        31 : "reach_for_the_star/layout_2x2_1.json",
        32 : "reach_for_the_star/layout_3x2_1.json",
        33 : "reach_for_the_star/layout_3x3_1.json",
        34 : "reach_for_the_star/layout_4x3_1.json",
        35 : "reach_for_the_star/layout_4x4_0.json",
        36 : "reach_for_the_star/layout_4x4_1.json",
        37 : "reach_for_the_star/layout_4x5_0.json",
        38 : "reach_for_the_star/layout_4x5_1.json",
        39 : "reach_for_the_star/layout_5x5_0.json",
        40 : "reach_for_the_star/layout_5x5_1.json",
        41 : "reach_for_the_star/layout_5x5_2.json",
        42 : "reach_for_the_star/layout_5x5_3.json",
        43 : "reach_for_the_star/layout_5x5_4.json",
        44 : "reach_for_the_star/layout_5x5_5.json",
        45 : "reach_for_the_star/layout_6x5_0.json",
        46 : "reach_for_the_star/layout_6x5_1.json",
        47 : "reach_for_the_star/layout_6x6_0.json",
        48 : "reach_for_the_star/layout_6x7_0.json",
        49 : "reach_for_the_star/layout_6x7_1.json",
        50 : "reach_for_the_star/layout_6x7_2.json",
        51 : "reach_for_the_star/layout_6x7_3.json",
        52 : "reach_for_the_star/layout_7x5_0.json",
        53 : "reach_for_the_star/layout_7x6_0.json",
        54 : "reach_for_the_star/layout_8x6_0.json",
        55 : "reach_for_the_star/layout_8x6_1.json",
        56 : "reach_for_the_star/layout_8x6_2.json",
        57 : "reach_for_the_star/layout_8x6_3.json",
        58 : "reach_for_the_star/layout_8x6_4.json",
        59 : "reach_for_the_star/layout_9x6_0.json",
        60 : "reach_for_the_star/layout_9x5_0.json",
        61 : "reach_for_the_star/layout_4x6_0.json",
    }
    if indexes == 'a':
        return list(all_instances.values())
    instances=list()
    for i in indexes:
        instances.append(all_instances.get(i))
    return instances


def original_instances(indexes):
    original_instances = {
        0 : "reach_for_the_star/original_instances/layout_10x11_0.json",
        1 : "reach_for_the_star/original_instances/layout_10x8_0.json",
        2 : "reach_for_the_star/original_instances/layout_11x6_0.json",
        3 : "reach_for_the_star/original_instances/layout_12x10_0.json",
        4 : "reach_for_the_star/original_instances/layout_12x11_0.json",
        5 : "reach_for_the_star/original_instances/layout_12x6_0.json",
        6 : "reach_for_the_star/original_instances/layout_12x8_0.json",
        7 : "reach_for_the_star/original_instances/layout_12x8_1.json",
        8 : "reach_for_the_star/original_instances/layout_13x7_0.json",
        9 : "reach_for_the_star/original_instances/layout_13x7_1.json",
        10 : "reach_for_the_star/original_instances/layout_13x7_2.json",
        11 : "reach_for_the_star/original_instances/layout_15x10_0.json",
        12 : "reach_for_the_star/original_instances/layout_15x8_0.json",
        13 : "reach_for_the_star/original_instances/layout_19x8_0.json",
        14 : "reach_for_the_star/original_instances/layout_20x12_0.json",
        15 : "reach_for_the_star/original_instances/layout_23x12_0.json",
        16 : "reach_for_the_star/original_instances/layout_25x12_0.json",
        17 : "reach_for_the_star/original_instances/layout_26x15_0.json",
        18 : "reach_for_the_star/original_instances/layout_7x6_0.json",
        19 : "reach_for_the_star/original_instances/layout_9x6_0.json",
    }
    if indexes == 'a':
        return list(original_instances.values())
    instances = list()
    for i in indexes:
        instances.append(original_instances.get(i))
    return instances

def six_x_six_instances(indexes):
    six_x_six_instances = {
        0 : "reach_for_the_star/6x6/layout_6x6_0.json",
        1 : "reach_for_the_star/6x6/layout_6x6_1.json",
        2 : "reach_for_the_star/6x6/layout_6x6_10.json",
        3 : "reach_for_the_star/6x6/layout_6x6_11.json",
        4 : "reach_for_the_star/6x6/layout_6x6_12.json",
        5 : "reach_for_the_star/6x6/layout_6x6_13.json",
        6 : "reach_for_the_star/6x6/layout_6x6_14.json",
        7 : "reach_for_the_star/6x6/layout_6x6_15.json",
        8 : "reach_for_the_star/6x6/layout_6x6_16.json",
        9 : "reach_for_the_star/6x6/layout_6x6_17.json",
        10 : "reach_for_the_star/6x6/layout_6x6_2.json",
        11 : "reach_for_the_star/6x6/layout_6x6_3.json",
        12 : "reach_for_the_star/6x6/layout_6x6_4.json",
        13 : "reach_for_the_star/6x6/layout_6x6_5.json",
        14 : "reach_for_the_star/6x6/layout_6x6_6.json",
        15 : "reach_for_the_star/6x6/layout_6x6_7.json",
        16 : "reach_for_the_star/6x6/layout_6x6_8.json",
        17 : "reach_for_the_star/6x6/layout_6x6_9.json",
        18: "reach_for_the_star/6x6/layout_6x6_18.json",
    }
    if indexes == 'a':
        return list(six_x_six_instances.values())
    instances = list()
    for i in indexes:
        instances.append(six_x_six_instances.get(i))
    return instances

def five_five_instances(indexes):
    five_five_instances = {
        0 : "reach_for_the_star/5x5/layout_5x5_0.json",
        1 : "reach_for_the_star/5x5/layout_5x5_1.json",
        2 : "reach_for_the_star/5x5/layout_5x5_10.json",
        3 : "reach_for_the_star/5x5/layout_5x5_11.json",
        4 : "reach_for_the_star/5x5/layout_5x5_4.json",
        5 : "reach_for_the_star/5x5/layout_5x5_13.json",
        6 : "reach_for_the_star/5x5/layout_5x5_14.json",
        7 : "reach_for_the_star/5x5/layout_5x5_15.json",
        8 : "reach_for_the_star/5x5/layout_5x5_16.json",
        9 : "reach_for_the_star/5x5/layout_5x5_2.json",
        10 : "reach_for_the_star/5x5/layout_5x5_3.json",
        11 : "reach_for_the_star/5x5/layout_5x5_12.json",
        12 : "reach_for_the_star/5x5/layout_5x5_5.json",
        13 : "reach_for_the_star/5x5/layout_5x5_6.json",
        14 : "reach_for_the_star/5x5/layout_5x5_7.json",
        15 : "reach_for_the_star/5x5/layout_5x5_8.json",
        16 : "reach_for_the_star/5x5/layout_5x5_9.json",
    }
    if indexes == 'a':
        return list(five_five_instances.values())
    instances = list()
    for i in indexes:
        instances.append(five_five_instances.get(i))
    return instances

def four_five_instances(indexes):
    instances = {
        0: "reach_for_the_star/4x5/layout_4x5_0.json",
        1: "reach_for_the_star/4x5/layout_4x5_1.json",
        2: "reach_for_the_star/4x5/layout_4x5_10.json",
        3: "reach_for_the_star/4x5/layout_4x5_11.json",
        4: "reach_for_the_star/4x5/layout_4x5_12.json",
        5: "reach_for_the_star/4x5/layout_4x5_13.json",
        6: "reach_for_the_star/4x5/layout_4x5_14.json",
        7: "reach_for_the_star/4x5/layout_4x5_2.json",
        8: "reach_for_the_star/4x5/layout_4x5_3.json",
        9: "reach_for_the_star/4x5/layout_4x5_4.json",
        10: "reach_for_the_star/4x5/layout_4x5_5.json",
        11: "reach_for_the_star/4x5/layout_4x5_6.json",
        12: "reach_for_the_star/4x5/layout_4x5_7.json",
        13: "reach_for_the_star/4x5/layout_4x5_8.json",
        14: "reach_for_the_star/4x5/layout_4x5_9.json",
    }
    if indexes == 'a':
        return list(instances.values())
    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list

def three_four_instances(indexes):
    instances = {
        0 : "reach_for_the_star/3x4/layout_3x4_0.json",
        1 : "reach_for_the_star/3x4/layout_3x4_1.json",
        2 : "reach_for_the_star/3x4/layout_3x4_2.json",
        3 : "reach_for_the_star/3x4/layout_3x4_3.json",
        4 : "reach_for_the_star/3x4/layout_3x4_4.json",
        5 : "reach_for_the_star/3x4/layout_3x4_5.json",
    }

    if indexes == 'a':
        return list(instances.values())

    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list

def climb_from_left(indexes):
    instances = {
        0: "reach_for_the_star/climb_from_left/cfl_layout_3x4_0.json",
        1: "reach_for_the_star/climb_from_left/cfl_layout_3x4_1.json",
        2: "reach_for_the_star/climb_from_left/cfl_layout_3x4_2.json",
        3: "reach_for_the_star/climb_from_left/cfl_layout_4x5_0.json",
        4: "reach_for_the_star/climb_from_left/cfl_layout_4x5_1.json",
        5: "reach_for_the_star/climb_from_left/cfl_layout_4x5_2.json",
        6: "reach_for_the_star/climb_from_left/cfl_layout_4x5_3.json",
        7: "reach_for_the_star/climb_from_left/cfl_layout_5x5_0.json",
        8: "reach_for_the_star/climb_from_left/cfl_layout_5x5_1.json",
        9: "reach_for_the_star/climb_from_left/cfl_layout_5x5_2.json",
        10: "reach_for_the_star/climb_from_left/cfl_layout_5x5_3.json",
        11: "reach_for_the_star/climb_from_left/cfl_layout_5x5_4.json",
        12: "reach_for_the_star/climb_from_left/cfl_layout_5x6_0.json",
        13: "reach_for_the_star/climb_from_left/cfl_layout_5x6_1.json",
        14: "reach_for_the_star/climb_from_left/cfl_layout_5x6_2.json",
        15: "reach_for_the_star/climb_from_left/cfl_layout_5x6_3.json",
        16: "reach_for_the_star/climb_from_left/cfl_layout_5x6_4.json",
        17: "reach_for_the_star/climb_from_left/cfl_layout_6x6_0.json",
        18: "reach_for_the_star/climb_from_left/cfl_layout_6x6_1.json",
        19: "reach_for_the_star/climb_from_left/cfl_layout_6x6_2.json",
        20: "reach_for_the_star/climb_from_left/cfl_layout_6x6_3.json",
        21: "reach_for_the_star/climb_from_left/cfl_layout_6x6_4.json",
        22: "reach_for_the_star/climb_from_left/cfl_layout_6x6_5.json",
        23: "reach_for_the_star/climb_from_left/cfl_layout_6x6_6.json",
        24: "reach_for_the_star/climb_from_left/cfl_layout_6x6_7.json",
        25: "reach_for_the_star/climb_from_left/cfl_layout_6x7_0.json",
        26: "reach_for_the_star/climb_from_left/cfl_layout_6x7_1.json",
        27: "reach_for_the_star/climb_from_left/cfl_layout_6x7_2.json",
        28: "reach_for_the_star/climb_from_left/cfl_layout_6x7_3.json",
        29: "reach_for_the_star/climb_from_left/cfl_layout_6x7_4.json",
        30: "reach_for_the_star/climb_from_left/cfl_layout_6x7_5.json",
        31: "reach_for_the_star/climb_from_left/cfl_layout_9x5_0.json",
        32: "reach_for_the_star/climb_from_left/cfl_layout_9x5_1.json",
        33: "reach_for_the_star/climb_from_left/cfl_layout_9x7_0.json",
        34: "reach_for_the_star/climb_from_left/cfl_layout_9x7_1.json",
        35: "reach_for_the_star/climb_from_left/cfl_layout_9x7_2.json",
    }

    if indexes == 'a':
        return list(instances.values())

    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list


def climb_from_right(indexes):
    instances = {
        0: "reach_for_the_star/climb_from_right/cfr_layout_3x4_0.json",
        1: "reach_for_the_star/climb_from_right/cfr_layout_3x4_1.json",
        2: "reach_for_the_star/climb_from_right/cfr_layout_3x4_2.json",
        3: "reach_for_the_star/climb_from_right/cfr_layout_4x5_0.json",
        4: "reach_for_the_star/climb_from_right/cfr_layout_4x5_1.json",
        5: "reach_for_the_star/climb_from_right/cfr_layout_4x5_2.json",
        6: "reach_for_the_star/climb_from_right/cfr_layout_4x5_3.json",
        7: "reach_for_the_star/climb_from_right/cfr_layout_5x5_0.json",
        8: "reach_for_the_star/climb_from_right/cfr_layout_5x5_1.json",
        9: "reach_for_the_star/climb_from_right/cfr_layout_5x5_2.json",
        10: "reach_for_the_star/climb_from_right/cfr_layout_5x5_3.json",
        11: "reach_for_the_star/climb_from_right/cfr_layout_5x5_4.json",
        12: "reach_for_the_star/climb_from_right/cfr_layout_5x6_0.json",
        13: "reach_for_the_star/climb_from_right/cfr_layout_5x6_1.json",
        14: "reach_for_the_star/climb_from_right/cfr_layout_5x6_2.json",
        15: "reach_for_the_star/climb_from_right/cfr_layout_5x6_3.json",
        16: "reach_for_the_star/climb_from_right/cfr_layout_5x6_4.json",
        17: "reach_for_the_star/climb_from_right/cfr_layout_6x6_0.json",
        18: "reach_for_the_star/climb_from_right/cfr_layout_6x6_1.json",
        19: "reach_for_the_star/climb_from_right/cfr_layout_6x6_2.json",
        20: "reach_for_the_star/climb_from_right/cfr_layout_6x6_3.json",
        21: "reach_for_the_star/climb_from_right/cfr_layout_6x6_4.json",
        22: "reach_for_the_star/climb_from_right/cfr_layout_6x6_5.json",
        23: "reach_for_the_star/climb_from_right/cfr_layout_6x6_6.json",
        24: "reach_for_the_star/climb_from_right/cfr_layout_6x6_7.json",
        25: "reach_for_the_star/climb_from_right/cfr_layout_6x7_0.json",
        26: "reach_for_the_star/climb_from_right/cfr_layout_6x7_1.json",
        27: "reach_for_the_star/climb_from_right/cfr_layout_6x7_2.json",
        28: "reach_for_the_star/climb_from_right/cfr_layout_6x7_3.json",
        29: "reach_for_the_star/climb_from_right/cfr_layout_6x7_4.json",
        30: "reach_for_the_star/climb_from_right/cfr_layout_6x7_5.json",
        31: "reach_for_the_star/climb_from_right/cfr_layout_9x5_0.json",
        32: "reach_for_the_star/climb_from_right/cfr_layout_9x5_1.json",
        33: "reach_for_the_star/climb_from_right/cfr_layout_9x7_0.json",
        34: "reach_for_the_star/climb_from_right/cfr_layout_9x7_1.json",
        35: "reach_for_the_star/climb_from_right/cfr_layout_9x7_2.json",
    }

    if indexes == 'a':
        return list(instances.values())

    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list

def climb_the_pilar_instances(indexes):
    instances = {
        0: "reach_for_the_star/climb_the_pilar/cp_layout_7x11_0.json",
        1: "reach_for_the_star/climb_the_pilar/cp_layout_7x11_1.json",
        2: "reach_for_the_star/climb_the_pilar/cp_layout_7x11_2.json",
        3: "reach_for_the_star/climb_the_pilar/cp_layout_7x11_3.json",
    }

    if indexes == 'a':
        return list(instances.values())

    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list

def climb_the_pilar_tiny_instances(indexes):
    instances = {
        0 : "reach_for_the_star/climb_the_pilar_tiny/cpt_layout_7x9_0.json",
        1 : "reach_for_the_star/climb_the_pilar_tiny/cpt_layout_7x9_1.json",
        2 : "reach_for_the_star/climb_the_pilar_tiny/cpt_layout_7x9_2.json",
        3 : "reach_for_the_star/climb_the_pilar_tiny/cpt_layout_7x9_3.json",
    }
    if indexes == 'a':
        return list(instances.values())

    instances_list = list()
    for i in indexes:
        instances_list.append(instances.get(i))
    return instances_list


# ROOT = os.path.dirname(os.path.abspath(__file__))
#
# ALL_INSTANCES=[os.path.join("reach_for_the_star", os.path.basename(f)) for f in glob.glob(os.path.join(ROOT, "../benchmarks/reach_for_the_star/*.json"))]
# ORIGINAL_EXAMPLE_INSTANCES=[os.path.join("reach_for_the_star", os.path.basename(f)) for f in glob.glob(os.path.join(ROOT,"../benchmarks/reach_for_the_star/original_instances/*.json"))]
