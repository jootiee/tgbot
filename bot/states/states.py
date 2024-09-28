from aiogram.fsm.state import State, StatesGroup


class Subscriber(StatesGroup):
    user_id = State()
    duration = State()


class Suspend(StatesGroup):
    user_id = State()

    
class Resume(StatesGroup):
    user_id = State()


class NewUser(StatesGroup):
    user_id = State()
    duration = State()

