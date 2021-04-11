import os
from gpl.defaults import BENCHMARK_DIR

def compute_instance_filename(instances):
    return [os.path.join(BENCHMARK_DIR, i) for i in instances]