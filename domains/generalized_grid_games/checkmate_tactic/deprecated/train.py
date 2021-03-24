from .config import get_config
from gpl.deprecated.model import GPLModel


def main(id, num_episodes):
    parameters = get_config(id)

    gpl = GPLModel(parameters)
    gpl.train()

    for _ in range(num_episodes):
        gpl.step()


if __name__ == "__main__":
    main(id=1, num_episodes=2)