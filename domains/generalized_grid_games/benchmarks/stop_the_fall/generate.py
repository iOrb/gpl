import os
from lgp.utils import serialize_layout, unserialize_layout
from layouts import LAYOUTS


ROOT = os.path.dirname(os.path.abspath(__file__))


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


def main():
    i = 0
    for layout in LAYOUTS:
        w = len(layout[0])
        h = len(layout)
        fn = check_and_rename(layout, os.path.join(ROOT, f"layout_{w}x{h}"), i)
        serialize_layout(layout, fn)


if __name__ == "__main__":
    main()

