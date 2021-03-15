import os
import gym
from lgp.utils import serialize_layout, unserialize_layout


ROOT = os.path.dirname(os.path.abspath(__file__))


def generate_original_instances(n):
    instances = list(range(n))
    base_class_name = "ReachForTheStar"
    i = 0
    for ins in instances:
        task_instance = ins
        env_name = "{}{}-v0".format(base_class_name, task_instance)
        env = gym.make(env_name)
        state = env.reset()
        save_instance(state, i)


def save_instance(layout, i):
    w = len(layout[0])
    h = len(layout)
    fn = check_and_rename(layout, os.path.join(ROOT, f"layout_{w}x{h}"), i)
    serialize_layout(layout, fn)


def check_and_rename(layout, base_file_name, i):
    file_name = f"{base_file_name}_{i}.json"

    if not os.path.exists(file_name):
        return file_name
    else:
        # check if existing file contains the same info,
        if (layout == unserialize_layout(file_name)).all():
            # overwrite if contain the same layout
            return file_name
        else:
            # rename if contain the NOT same layout, and check again
            return check_and_rename(layout, base_file_name, i + 1)


if __name__=='__main__':
    generate_original_instances(n=20)