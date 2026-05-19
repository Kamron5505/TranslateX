from aiogram.fsm.state import State, StatesGroup


class TranslateStates(StatesGroup):
    """Состояния для перевода"""
    waiting_for_source_lang = State()
    waiting_for_target_lang = State()
    waiting_for_text = State()


class AdminStates(StatesGroup):
    """Состояния для админ панели"""
    waiting_for_broadcast = State()
    waiting_for_ban_user_id = State()
    waiting_for_unban_user_id = State()
    confirm_broadcast = State()
