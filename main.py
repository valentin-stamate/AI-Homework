from exploration import Exploration
from state import State


def main():
    state = State(4)
    State.valid_transition(state, 1, 3).show()

    # Exploration.start()


if __name__ == '__main__':
    main()
