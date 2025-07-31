from aiogram.fsm.state import State, StatesGroup


class MakeMemeFsm(StatesGroup):
    choosing_template = State()
    entering_text = State()
