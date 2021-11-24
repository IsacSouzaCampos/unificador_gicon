import PySimpleGUI as sg


class View:
    def __init__(self):
        self.window = None

    def start_main_window(self):
        sg.theme('default1')
        layout = [[sg.Text('Processando...', pad=((60, 60), (1, 1)))]]
        self.window = sg.Window('Unificador', layout, disable_close=True, finalize=True)

    def close_main_window(self):
        self.window.close()

    @staticmethod
    def error_1(e):
        sg.popup(f'Erro ao ler o arquivo {e}')
        print(e)

    @staticmethod
    def error_2():
        sg.popup('Problema ao abrir arquivo "resultado.txt".')
