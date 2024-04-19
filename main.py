from kivy import Config

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '500')

import re
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.uix.divider import MDDivider

import os, sys
from kivy.resources import resource_add_path

math_list = '()*/+-'
syms_list = '×÷+-'
PAGE_NUM = 0


# math stuff -----------------------------------
def multiply(n1, n2):
    try:
        float(n1)
        float(n2)

    except ValueError:
        return f'Error {float(n1)} * {float(n2)}'

    return float(n1) * float(n2)


def division(n1, n2):
    try:
        float(n1) / float(n2)

    except ZeroDivisionError:
        return f'Error {float(n1)} / {float(n2)}'

    return float(n1) / float(n2)


def plus(n1, n2):
    try:
        float(n1)
        float(n2)

    except ValueError:
        return f'Error {float(n1)} + {float(n2)}'

    return float(n1) + float(n2)


def minus(n1, n2):
    try:
        float(n1)
        float(n2)

    except ValueError:
        return f'Error {float(n1)} - {float(n2)}'

    return float(n1) - float(n2)


def mathfunc(equation):
    syms = re.findall(r'[*/+-]+?', str(equation))
    syms = sorted(syms, key=lambda word: [math_list.index(c) for c in word])
    print(syms, 'sorted')
    if not syms:
        return 'Error'
    closest_str = str(syms[0])

    try:
        closest = equation.index(closest_str)
    except ValueError:
        return equation

    if '%' in str(equation):
        perc_sym = equation.index(re.search(r'\d+%', str(equation))[0])
        split = re.split(r'%', str(equation[perc_sym]))[0]
        print(split, 'split')
        perc = float(split) / 100
        return equation[:perc_sym] + [str(perc)] + equation[perc_sym + 1:]

    if equation[closest] == '*':
        multi = str(multiply(equation[closest - 1], equation[closest + 1]))

        if re.fullmatch(r'\d+\.0+', multi):
            multi = str.replace(multi, '.' + str.split(re.fullmatch(r'\d+\.0+', multi)[0], '.')[1], '')

        return equation[:closest - 1] + [multi] + equation[closest + 2:]

    elif equation[closest] == '+':
        pl = str(plus(equation[closest - 1], equation[closest + 1]))

        if re.fullmatch(r'\d+\.0+', pl):
            pl = str.replace(pl, '.' + str.split(re.fullmatch(r'\d+\.0+', pl)[0], '.')[1], '')

        return equation[:closest - 1] + [pl] + equation[closest + 2:]

    elif equation[closest] == '-':
        min = str(minus(equation[closest - 1], equation[closest + 1]))

        if re.fullmatch(r'\d+\.0+', min):
            min = str.replace(min, '.' + str.split(re.fullmatch(r'\d+\.0+', min)[0], '.')[1], '')

        return equation[:closest - 1] + [min] + equation[closest + 2:]

    elif equation[closest] == '/':
        divis = str(division(equation[closest - 1], equation[closest + 1]))

        if re.fullmatch(r'\d+\.0+', divis):
            divis = str.replace(divis, '.' + str.split(re.fullmatch(r'\d+\.0+', divis)[0], '.')[1], '')

        return equation[:closest - 1] + [divis] + equation[closest + 2:]


def calculate(equation):
    actions = []

    for i in range(0, len(re.findall(r'[()*/+-]+?', equation))):
        for y in range(0, len(equation)):
            if equation[y] in math_list:

                if equation[y - 1] != ' ' and y >= 1:
                    equation = equation.replace(equation[y], ' ' + equation[y])

                elif y == 0 and equation[y] == '-':
                    pass

                elif y + 1 < len(equation) and equation[y + 1] != ' ':
                    # print(equation[y], 'there')
                    equation = equation.replace(equation[y], equation[y] + ' ')

            print(equation, 'update')
            if equation[y] == '(':
                if y + 1 < len(equation):
                    pass
                else:
                    print('error (')
                    return 0

            elif equation[y] == ')':
                if y > 1:
                    pass
                else:
                    print('error )')
                    return 0

        print(equation, 'equat')
    eq = str.split(equation, ' ')

    actions.append(str(eq))

    copy_eq = eq
    print(eq, 'eq')
    brackets_count = 0

    for i in range(0, len(eq)):
        if ('(' and ')') in eq:
            if eq.count('(') == eq.count(')'):
                brackets_count = eq.count('(')
            else:
                brackets_count = -1

    if brackets_count > 0:
        print('brackets count > 0')
        for i in range(0, brackets_count):
            bracket1_pos = len(copy_eq) - 1 - copy_eq[::-1].index('(')
            bracket2_pos = copy_eq.index(')')

            if bracket1_pos + 1 != bracket2_pos:
                print(len(re.findall(r'[%+*/-]+?',
                                                 str(copy_eq[bracket1_pos + 1:bracket2_pos]))))

                brackets_eq = eq[bracket1_pos+1:bracket2_pos]
                brackets_len = len(re.findall(r'[%*/+-]', str(brackets_eq)))

                # calc for len
                for j in range(0, brackets_len):
                    brackets_eq = mathfunc(brackets_eq)
                    print(brackets_eq, 'CURR EQ')
                    if j+1 < brackets_len:
                        actions.append('('+str(brackets_eq)+') ' + str(eq[bracket2_pos + 1:]))
                    elif j+1 == brackets_len:
                        actions.append(str(brackets_eq) + str(eq[bracket2_pos + 1:]))
                    print(eq, 'afterCURR EQ')

                eq = eq[:bracket1_pos] + brackets_eq + eq[bracket2_pos + 1:]

                print(eq, 'brackets', brackets_count, actions)
            else:
                print('brackets are empty')

    print('eq before loop', eq)

    for i in range(0, len(re.findall(r'[%*/+-]+?', str(eq)))):
        eq = mathfunc(eq)

        print(eq, 'in main loop')
        actions.append(str(eq))

    print('answer', eq)

    # if 'Error' in str(eq):
    #     print('Error')
    #     return list

    return actions
# -----------------------------

def input_analyze(field, text):
    # doesnt do anything ----------
    equation = field.text

    equation = str.replace(equation, '×', '*')
    equation = str.replace(equation, '÷', '/')
    equation = str.replace(equation, ',', '.')

    print('len - ', len(equation), 'text - ', text)
    # ----------
    if len(equation) > 53:
        return 0

    if (len(field.text) == 0 or 'Input' in field.text or 'Error' in field.text) and str(text) in syms_list and text != '-':
        print('return -')
        return 0

    if len(field.text) > 0 and str(field.text[-1]) in syms_list and str(text) in syms_list:
        print('return sym')
        return 0

    if str(text) == '%' and (str(field.text[-1]) == '%' or str(field.text[-1]) in syms_list):
        print('return %')
        return 0

    elif (len(field.text) == 0 or 'Input' in field.text or 'Error' in field.text) and str(text) == '%':
        return 0

    if str(text) == '1/x':
        ind = re.split(r'[×÷+-]+?', field.text)

        if len(field.text) == 0 or 'Input' in field.text or 'Error' in field.text or field.text[-1] == '-':
            return 0

        if ind[0].startswith('-'):
            print(ind)
            field.text = f'1÷({field.text[0:ind]}'

        elif len(ind) > 1:
            field.text = f'1÷({field.text})'

        else:
            field.text = f'1÷{field.text}'

        return 0

    if str(text) in '()':
        if str(text) == ')' and (len(field.text) == 0 or 'Input' in field.text or 'Error' in field.text):
            return 0

    if 'Input' in field.text or 'Error' in field.text:
        field.text = ''

    split_sym = re.split(r'[×÷+-]+?', field.text)
    if text == ',':
        if (',' and '%') not in split_sym[-1]:
            field.text += text

    else:
        if len(field.text) > 0 and field.text[-1] == '%' and str(text) in '0123456789()':
            field.text += f'×{str(text)}'
        else:
            field.text += str(text)

def solve_render(layout, actions, page_count=0):
    global iters
    layout.clear_widgets()

    act_points = len(actions)
    pages_minus1 = act_points // 6

    # magic til end of func
    if page_count < pages_minus1:
        iters = 5
    elif page_count == pages_minus1:
        iters = (act_points - 5 * page_count)

    print(page_count, '-page count', iters, '-iterations')

    for i in range(0, iters):
        mdscreen = MDScreen(
            MDLabel(
                size_hint=(0.4, 0.125),
                radius=[10, 10, 10, 10],
                theme_bg_color='Custom',
                md_bg_color='darkslategrey',
                pos_hint={'top': 1, 'right': 0.5},
                text=f'Action {(page_count * 5 + i) + 1}',
                theme_font_size='Custom',
                font_size='14sp',
                halign='center',
                valign='top',
            ),
            MDLabel(
                size_hint=(1, 0.85),
                pos_hint={'top': 0.85},
                text=str(actions[page_count * 5 + i]),
                theme_font_size='Custom',
                #theme_bg_color='Custom',
                #md_bg_color='blue',
                font_size=str(100 // 5) + 'sp',
            ),
            size_hint=(1, 0.19),
            #theme_bg_color='Custom',
            #md_bg_color='green',
        )
        layout.add_widget(mdscreen)
        print(i, 'iters')
        if i + 1 == iters:
            # the last iteration
            break

        mddivider = MDDivider()
        layout.add_widget(mddivider)


def change_pages(layout, column, type, actions):
    global PAGE_NUM

    act_points = len(actions)
    pages = act_points // 6 + 1

    if type == '>':
        PAGE_NUM += 1
        solve_render(layout, actions, page_count=PAGE_NUM)

    elif type == '<':
        PAGE_NUM -= 1
        solve_render(layout, actions, page_count=PAGE_NUM)

    column.clear_widgets()
    update(layout, column, actions)

    print(PAGE_NUM, '-PAGE NUM', pages, '-PAGES')

def update(layout, column, actions):
    act_points = len(actions)
    pages = act_points // 6 + 1

    mdlabel = MDLabel(
        text='Solve:',
        halign='center',
        theme_font_name='Custom',
        font_name=MainApp.resource_path('fonts/Prompt-Regular.ttf'),
        theme_font_size='Custom',
        font_size='35sp',
    )
    column.add_widget(mdlabel)

    if PAGE_NUM == 0:
        print('PAGE_NUM == 0')
        mdbutton = MDButton(
            MDButtonText(
                text='>',
                pos_hint={'center_x': .5, 'center_y': .5},
                theme_font_size='Custom',
                font_size='30sp',
                theme_font_name='Custom',
                font_name=MainApp.resource_path('fonts/Prompt-Regular.ttf'),
                theme_text_color='Custom',
                text_color='white',
            ),
            theme_width='Custom',
            theme_height='Custom',
            size_hint=(0.2, 0.9),
            pos_hint={'top': 1, 'right': 0.95},
            theme_bg_color='Custom',
            md_bg_color='darkslategrey',
            elevation_level=1,
        )
        mdbutton.bind(on_release=lambda x: change_pages(layout, column, '>', actions))
        column.add_widget(mdbutton)

    elif 0 < PAGE_NUM + 1 < pages:
        print('0 < PAGE_NUM + 1 < pages')
        mdbutton = MDButton(
            MDButtonText(
                text='<',
                pos_hint={'center_x': .5, 'center_y': .5},
                theme_font_size='Custom',
                font_size='30sp',
                theme_font_name='Custom',
                font_name=MainApp.resource_path('fonts/Prompt-Regular.ttf'),
                theme_text_color='Custom',
                text_color='white',
            ),
            theme_width='Custom',
            theme_height='Custom',
            size_hint=(0.2, 0.9),
            pos_hint={'top': 1, 'right': 0.2},
            theme_bg_color='Custom',
            md_bg_color='darkslategrey',
            elevation_level=1,
        )

        mdbutton2 = MDButton(
            MDButtonText(
                text='>',
                pos_hint={'center_x': .5, 'center_y': .5},
                theme_font_size='Custom',
                font_size='30sp',
                theme_font_name='Custom',
                font_name=MainApp.resource_path('fonts/Prompt-Regular.ttf'),
                theme_text_color='Custom',
                text_color='white',
            ),
            theme_width='Custom',
            theme_height='Custom',
            size_hint=(0.2, 0.9),
            pos_hint={'top': 1, 'right': 0.95},
            theme_bg_color='Custom',
            md_bg_color='darkslategrey',
            elevation_level=1,
        )

        mdbutton.bind(on_release=lambda x: change_pages(layout, column, '<', actions))
        mdbutton2.bind(on_release=lambda x: change_pages(layout, column, '>', actions))
        column.add_widget(mdbutton)
        column.add_widget(mdbutton2)

    elif PAGE_NUM + 1 == pages:
        print('PAGE_NUM + 1 == pages')
        mdbutton = MDButton(
            MDButtonText(
                text='<',
                pos_hint={'center_x': .5, 'center_y': .5},
                theme_font_size='Custom',
                font_size='30sp',
                theme_font_name='Custom',
                font_name=MainApp.resource_path('fonts/Prompt-Regular.ttf'),
                theme_text_color='Custom',
                text_color='white',
            ),
            theme_width='Custom',
            theme_height='Custom',
            size_hint=(0.2, 0.9),
            pos_hint={'top': 1, 'right': 0.2},
            theme_bg_color='Custom',
            md_bg_color='darkslategrey',
            elevation_level=1,
        )

        mdbutton.bind(on_release=lambda x: change_pages(layout, column, '<', actions))
        column.add_widget(mdbutton)


class MainApp(MDApp):

    def build(self):
        self.title = 'Calculator'
        self.icon = self.resource_path('images/app_icon.ico')
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Darkslategrey'

        return Builder.load_file(self.resource_path('math.kv'))

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)

    def on_text(self, text):
        try:
            float(text)
        except ValueError:
            return 0

    def input_text(self, text, isFunc=False):
        input_field = self.root.ids.input_field

        input_analyze(input_field, text)

    def control_buttons(self, func):
        input_field = self.root.ids.input_field
        solve_layout = self.root.ids.slv_layout
        solve_column = self.root.ids.slv_col

        if 'Input' not in input_field.text:

            if func == 'backspace':
                input_field.text = input_field.text[:-1]

                if len(input_field.text) == 0:
                    input_field.text = 'Input'

            elif func == 'delete':
                input_field.text = 'Input'

            elif func == 'chunk_del':
                c_chunk = re.findall(r'[%×÷+-]+|[()]+|\d+', input_field.text)

                if c_chunk:
                    input_field.text = input_field.text.replace(c_chunk[-1], '', 1)

                if input_field.text == '':
                    input_field.text = 'Input'

            elif func == 'result':
                equation = input_field.text

                # convert to math syms
                for i in range(0, len(syms_list)):
                    equation = equation.replace(syms_list[i], math_list[i + 2])

                if equation[-1] in '*/+-':
                    input_field.text = 'Error'
                    return 0

                actions = calculate(equation)
                try:
                    act_points = len(actions)
                except TypeError:
                    print('returning list')
                    act_points = len(list(actions))

                pages = act_points // 6 + 1

                # convert back and unpack
                for i in range(act_points):
                    for y in range(0, len(math_list)):
                        equation = equation.replace(math_list[y], syms_list[y - 2])
                    # unpack
                    for let in actions[i]:
                        if let in "'[],":
                            actions[i] = str.replace(actions[i], let, '')

                    if i + 1 == act_points:
                        input_field.text = str(actions[-1])
                        actions[i] = 'Result: ' + actions[i]

                solve_render(solve_layout, actions, page_count=PAGE_NUM)
                solve_column.clear_widgets()

                if act_points > 5:
                    # show the buttons
                    update(solve_layout, solve_column, actions)

                elif act_points <= 5:
                    mdlabel = MDLabel(
                        text='Solve:',
                        halign='center',
                        theme_font_name='Custom',
                        font_name=self.resource_path('fonts/Prompt-Regular.ttf'),
                        theme_font_size='Custom',
                        font_size='35sp',
                    )
                    solve_column.add_widget(mdlabel)
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path((os.path.join(sys._MEIPASS)))
        
    MainApp().run()
