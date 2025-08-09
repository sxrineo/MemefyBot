from aiogram.fsm.state import State, StatesGroup


class MakeMemeFsm(StatesGroup):
    choosing_template = State()
    entering_first_text = State()
    entering_second_text = State()

