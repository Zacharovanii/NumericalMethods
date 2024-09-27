from aiogram.utils.keyboard import *


class ButtonText:
    HELLO = 'Hello!'
    HELP = 'Help me!'


class FuncKb:
    def __init__(self):
        self.buttons = [
            [
                InlineKeyboardButton(text='(', callback_data='do_('),
                InlineKeyboardButton(text='x', callback_data='num_x'),
                InlineKeyboardButton(text='ba', callback_data='do_backspace'),
                InlineKeyboardButton(text='/', callback_data='num_/')
            ],
            [
                InlineKeyboardButton(text='7', callback_data='num_7'),
                InlineKeyboardButton(text='8', callback_data='num_8'),
                InlineKeyboardButton(text='9', callback_data='num_9'),
                InlineKeyboardButton(text='*', callback_data='num_*')
            ],
            [
                InlineKeyboardButton(text='4', callback_data='num_4'),
                InlineKeyboardButton(text='5', callback_data='num_5'),
                InlineKeyboardButton(text='6', callback_data='num_6'),
                InlineKeyboardButton(text='+', callback_data='num_+')
            ],
            [
                InlineKeyboardButton(text='1', callback_data='num_1'),
                InlineKeyboardButton(text='2', callback_data='num_2'),
                InlineKeyboardButton(text='3', callback_data='num_3'),
                InlineKeyboardButton(text='-', callback_data='num_-')
            ],
            [
                InlineKeyboardButton(text='C', callback_data='do_clear'),
                InlineKeyboardButton(text='0', callback_data='num_0'),
                InlineKeyboardButton(text='.', callback_data='num_.'),
                InlineKeyboardButton(text='^', callback_data='do_pow')
            ],
            [
                InlineKeyboardButton(text='done', callback_data='do_done')
            ]
        ]

        self.kb = InlineKeyboardMarkup(inline_keyboard=self.buttons)

        self.func = ''
        self.botFunc = ''

    def pressedPower(self):
        self.func += "**"
        self.botFunc += '^'

    def pressedDone(self):
        print('done')
        self.clearFunc()

    def pressedBackspace(self):
        self.func = self.func[:-1]
        self.botFunc = self.botFunc[:-1]

    def pressedBracket(self):
        sym = self.buttons[0][0].text
        self + sym
        if sym == '(':
            sym = ')'
        else:
            sym = '('
        self.buttons[0][0] = InlineKeyboardButton(text=sym, callback_data=f'do_{sym}')
        self.kb.inline_keyboard = self.buttons

    def clearFunc(self):
        self.func = ''
        self.botFunc = ''

    def getMarkup(self):
        return self.kb

    def getText(self):
        return f'Ваша функция:\t\n{self.botFunc}'

    def __add__(self, other: str):
        self.func += other
        self.botFunc += other


def get_on_start_kb():
    button_hello = KeyboardButton(text=ButtonText.HELLO)
    button_help = KeyboardButton(text=ButtonText.HELP)
    first_row = [button_hello]
    second_row = [button_help]
    buttons_row = [first_row, second_row]
    markup = ReplyKeyboardMarkup(keyboard=[*buttons_row], input_field_placeholder='Добро пожаловать!')
    return markup

