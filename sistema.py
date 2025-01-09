from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
import locale
import subprocess
import platform
import pandas as pd
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
import hashlib
import shutil
import os
from kivy.uix.progressbar import ProgressBar
import arquivos_de_inicializacao
import convertertxt_em_pdf
import time
# import total_a_recolher

Window.size = (1000, 600)  # Define o tamanho da janela
class Login(Screen):
    pass

class Loginsenha(Screen):
    pass

class Logincadastro(Screen):
    pass

class FirstScreen(Screen):
    dados_enrol_scroll_text3 = StringProperty("")
    dados_enrol_scroll_text4 = StringProperty("")
    dados_enrol_scroll_text5 = StringProperty("")
    dados_enrol_scroll_text6 = StringProperty("")
    dados_enrol_scroll_text7 = StringProperty("")
    dados_enrol_scroll_text8 = StringProperty("")
    dados_enrol_scroll_text9 = StringProperty("")
    dados_enrol_scroll_text10 = StringProperty("")
    dados_enrol_scroll_text11 = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carregar_dados()  # Carrega os dados ao iniciar a tela

    def on_enter(self):
        self.carregar_dados()  # Atualiza os dados toda vez que a tela é exibida

    def carregar_dados(self):
        self.dados()
        self.atualizar_dados3()
        arquivos_de_inicializacao.arquivos_iniciais()
        
    def dados(self):
        # Carregar o DataFrame
        df = pd.read_csv('LISTA ENROLADORES.txt', delimiter=' ', header=None, names=[
            'Data', 'Enrolador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'], encoding='latin1', on_bad_lines='skip')

        # Função para converter valores para float
        def extrair_valor(valor):
            try:
                # Remover caracteres não numéricos e converter para float
                valor_str = str(valor).strip()
                if valor_str:
                    return float(valor_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', ''))
                return 0.0
            except ValueError:
                return 0.0

        # Aplicar a função de conversão à coluna "Valor Total"
        df['Val Total'] = df['Val Total'].apply(extrair_valor)

        self.soma_valor_total = df['Val Total'].sum()
        self.enrolador_qt = df.groupby('Enrolador')['Val Total'].sum().reset_index()
        self.enrolador_total =  self.enrolador_qt['Enrolador'].count()
        
        with open('Orçamento enrolador.txt', 'w', encoding="utf-8") as orcamento:
            orcamento.write(str(f'{self.soma_valor_total:.2f}'))

        #exibindo o valor por funcionário
        # print('RESULTADO FINANCEIRO DE CADA ENROLADOR: \n')
        self.result = df.groupby('Enrolador')['Val Total'].sum().reset_index()
        self.result['Val Total'] = self.result['Val Total'].apply(lambda x: f"{x:.2f}")        # Exibindo o resultado
        table_data = self.result.values.tolist()

        # Criando a tabela com centralização
        self.data_table = MDDataTable(
            column_data=[
                ("Enrolador", dp(30)),
                ("Val Total", dp(30)),
            ],
            row_data=[
                (str(row[0]), str(row[1])) for row in table_data
            ],
            rows_num=60
        )

        # Adicionar a tabela ao layout
        #self.add_widget(self.data_table)

        # print(self.result)
        # print(f'Total de enroladoes: {self.result['Enrolador'].count()}')

        with open('LISTA VALE TOTAL.txt', 'r') as file:
            linhas = file.readlines()

        dados_limpos3 = [linha.replace('[', '').replace(']', '').split() for linha in linhas]
        df3 = pd.DataFrame(dados_limpos3, columns=['Data', 'Nome', 'Descrição', 'Valor'])
        #print('\n                VALES NO TOTAL:')
        df3['Valor'] = pd.to_numeric(df3['Valor'])
        # print(df3)
        self.totalvale = self.soma_vale_total = df3['Valor'].sum()

        # print('\nOBJETOS GERAIS DE CADA ENROLADOR: \n')
        self.resultenrolador = df.groupby('Enrolador').agg({'Objeto': 'sum','Qtde': 'sum'}).reset_index()
        # print(self.resultenrolador)

        self.objeto_total = df[df['Objeto']] = df['Qtde'].apply(extrair_valor)
        self.soma_objeto_total = self.objeto_total.sum()
        # print(f'*Objetos no Geral: {self.soma_objeto_total} unidades')
        
        self.objeto = df[df['Objeto']] = df['Qtde'].apply(extrair_valor)
        self.objeto_mais_enrolado = self.objeto.max()
        self.objeto_menos_enrolado = self.objeto.min()

        self.maior_ocorrencia = df.groupby('Objeto')['Qtde'].count()
        self.numero_ocorrencia = self.maior_ocorrencia.max()
        self.nome_ocorrencia = self.maior_ocorrencia.idxmax()

        self.menor_ocorrencia = df.groupby('Objeto')['Qtde'].count()
        self.numero_ocorrencia2 = self.menor_ocorrencia.min()
        self.nome_ocorrencia2 = self.menor_ocorrencia.idxmin()

        #Cálculo para os soldadores
        df2 = pd.read_csv('LISTA SOLDADORES.txt', delimiter=' ', header=None, names=[
            'Data', 'Soldador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'], encoding='latin1', on_bad_lines='skip')
        # Resetar os índices do DataFrame
        #df2.reset_index(drop=True, inplace=True)
        df2['Val Total'] = df2['Val Total'].apply(extrair_valor)
        # Somar os valores da coluna "Valor Total"
        self.soma_valor_total2 = df2['Val Total'].sum()
        self.soldador_qt = df2.groupby('Soldador')['Val Total'].sum().reset_index()
        self.soldador_total =  self.soldador_qt['Soldador'].count()

        self.pagar_total = (self.soma_valor_total + self.soma_valor_total2) - self.soma_vale_total

        self.atualizar_dados3()
        
    def atualizar_dados3(self):
        totalvalor = str(f'{self.soma_valor_total:.2f}')
        soldadorvalor = str(f'{self.soma_valor_total2:.2f}')
        totalvale = str(f'{self.totalvale:.2f}')
        totalpagar = str(f'{self.pagar_total:.2f}')
        maisobjeto = str(f'{self.objeto_mais_enrolado:.0f}')
        menorobjeto = str(f'{self.objeto_menos_enrolado:.0f}')
        maiorocorrencia = str(f'{self.numero_ocorrencia}')
        nomemaiorocorrencia = str(f'{self.nome_ocorrencia}')
        menorocorrencia = str(f'{self.numero_ocorrencia2}')
        nomemenorocorrencia = str(f'{self.nome_ocorrencia2}')
        enroladorqtde = str(f'{self.enrolador_total - 1}')
        soldadorqtde = str(f'{self.soldador_total - 1}')

        self.dados_enrol_scroll_text3 = f"__________________________________________________________\n\n    Valor Total dos Enroladores: R$ {totalvalor}"
        self.dados_enrol_scroll_text10 = f" Valor Total dos Soldadores:   R$ {soldadorvalor}"
        self.dados_enrol_scroll_text4 = f" Valor Pago Vale:                             R$ {totalvale}"
        self.dados_enrol_scroll_text5 = f"    Valor a Pagar:                                R$ {totalpagar}\n__________________________________________________________"
        self.dados_enrol_scroll_text6 = f"Maior quantidade enrolada: {maisobjeto} unidades"
        self.dados_enrol_scroll_text7 = f"Menor quantidade enrolada: {menorobjeto} unidades"
        self.dados_enrol_scroll_text8 = f"Maior ocorrência de um objeto: {maiorocorrencia} {nomemaiorocorrencia}"
        self.dados_enrol_scroll_text9 = f"Menor ocorrência de um objeto: {menorocorrencia} {nomemenorocorrencia}"
        self.dados_enrol_scroll_text11 = f"Enroladores: {enroladorqtde}   Soldadores: {soldadorqtde}"

class SecondScreen(Screen):
    pass

class TerceiraTela(Screen):
    pass

class DadosEnroladores(Screen):

    dados_enrol_scroll_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carregar_dados2()  # Carrega os dados ao iniciar a tela

    def on_enter(self):
        self.carregar_dados2()  # Atualiza os dados toda vez que a tela é exibida

    def carregar_dados2(self):
        self.dados2()
        self.atualizar_dados()
    
    def dados2(self):
        with open('LISTA ENROLADORES.txt', 'r') as file:
            linhas = file.readlines()
        
        # Remover as chaves e dividir os dados
        dados_limpios = [linha.replace('[', '').replace(']', '').split() for linha in linhas]

        # Criar o DataFrame
        df = pd.DataFrame(dados_limpios, columns=['Data', 'Enrolador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'])

        # Convertendo colunas numéricas para o tipo correto
        df['Qtde'] = pd.to_numeric(df['Qtde'])
        df['Val unit'] = pd.to_numeric(df['Val unit'])
        df['Val Total'] = pd.to_numeric(df['Val Total'])

        # Filtrar os dados para os objetos "Veneza" e "Banqueta"

        self.qtde_veneza = df[df['Objeto'] == 'Veneza']['Qtde'].sum()
        self.qtde_banqueta = df[df['Objeto'] == 'Banqueta']['Qtde'].sum()
        self.qtde_leticia = df[df['Objeto'] == 'Letícia']['Qtde'].sum()
        self.qtde_balanco = df[df['Objeto'] == 'Balanço']['Qtde'].sum()
        self.qtde_centrocomum = df[df['Objeto'] == 'Ccomum']['Qtde'].sum()
        self.qtde_centroleticia = df[df['Objeto'] == 'Cletícia']['Qtde'].sum()
        self.qtde_centroluxo = df[df['Objeto'] == 'Cluxo']['Qtde'].sum()

        # Exibir os resultados no terminal
        # print(f"Quantidade total de Veneza: {self.qtde_veneza} unidades/{self.qtde_veneza/4} jogos")
        # print(f"Quantidade total de Banqueta: {self.qtde_banqueta} unidades")
        # print(f"Quantidade total de Letícia: {self.qtde_leticia} unidades/{self.qtde_leticia/4} jogos")
        # print(f"Quantidade total de Balanço: {self.qtde_balanco} unidades")
        # print(f"Quantidade total de Centro Comum: {self.qtde_centrocomum} unidades")
        # print(f"Quantidade total de Centro Letícia: {self.qtde_centroleticia} unidades")
        # print(f"Quantidade total de Centro Luxo: {self.qtde_centroluxo} unidades")
        with open(f'LISTA TOTAL OBJETO.txt', 'w') as totalfeito:
            totalfeito.write(f'{self.qtde_veneza:.0f} {self.qtde_banqueta:.0f} {self.qtde_leticia:.0f} {self.qtde_balanco:.0f} {self.qtde_centrocomum:.0f} {self.qtde_centroleticia:.0f} {self.qtde_centroluxo:.0f}')
        
        self.qtde_jogoven1 = self.qtde_veneza/4
        self.jogolet = self.qtde_leticia/4
        self.atualizar_dados()
    
    def atualizar_dados(self):
        qtde_ven1 = str(f'{self.qtde_veneza:.0f}')
        qtde_jogoven2 = str(f'{self.qtde_jogoven1:.0f}')
        qtde_ban1 = str(f'{self.qtde_banqueta:.0f}')
        qtde_let1 = str(f'{self.qtde_leticia:.0f}')
        jogolet2 = str(f'{self.jogolet:.0f}')
        qtde_bal1 = str(f'{self.qtde_balanco:.0f}')
        qtde_ccomum = str(f'{self.qtde_centrocomum:.0f}')
        qtde_clet = str(f'{self.qtde_centroleticia:.0f}')
        qtde_cluxo = str(f'{self.qtde_centroluxo:.0f}')
        self.dados_enrol_scroll_text = f"1. Quantidade total de Veneza: {qtde_ven1} unidades/{qtde_jogoven2} jogos\n2. Quantidade total de Banqueta: {qtde_ban1} unidades\n3. Quantidade total de Letícia: {qtde_let1} unidades/{jogolet2} jogos\n4. Quantidade total de Balanço: {qtde_bal1} unidades\n5. Quantidade total de Centro Comum: {qtde_ccomum} unidades\n6. Quantidade total de Centro Letícia: {qtde_clet} unidades\n7. Quantidade total de Centro Luxo: {qtde_cluxo} unidades"

class DadosSoldadores(Screen):

    dados_enrol_scroll_text2 = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carregar_dados3()  # Carrega os dados ao iniciar a tela

    def on_enter(self):
        self.carregar_dados3()  # Atualiza os dados toda vez que a tela é exibida

    def carregar_dados3(self):
        self.dados3()
        self.atualizar_dados2()

    def dados3(self):
        with open('LISTA SOLDADORES.txt', 'r') as file:
            linhas = file.readlines()

        # Remover as chaves e dividir os dados
        dados_limpios = [linha.replace('[', '').replace(']', '').split() for linha in linhas]

        # Criar o DataFrame
        df = pd.DataFrame(dados_limpios, columns=['Data', 'Enrolador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'])

        # Convertendo colunas numéricas para o tipo correto
        df['Qtde'] = pd.to_numeric(df['Qtde'])
        df['Val unit'] = pd.to_numeric(df['Val unit'])
        df['Val Total'] = pd.to_numeric(df['Val Total'])

        # Filtrar os dados para os objetos "Veneza" e "Banqueta"

        self.qtde_veneza = df[df['Objeto'] == 'Veneza']['Qtde'].sum()
        self.qtde_banqueta = df[df['Objeto'] == 'Banqueta']['Qtde'].sum()
        self.qtde_leticia = df[df['Objeto'] == 'Letícia']['Qtde'].sum()
        self.qtde_balanco = df[df['Objeto'] == 'Balanço']['Qtde'].sum()
        self.qtde_centrocomum = df[df['Objeto'] == 'Ccomum']['Qtde'].sum()
        self.qtde_centroleticia = df[df['Objeto'] == 'Cletícia']['Qtde'].sum()
        self.qtde_centroluxo = df[df['Objeto'] == 'Cluxo']['Qtde'].sum()

        # Exibir os resultados no terminal
        # print(f"Quantidade total de Veneza: {self.qtde_veneza} unidades/{self.qtde_veneza/4} jogos")
        # print(f"Quantidade total de Banqueta: {self.qtde_banqueta} unidades")
        # print(f"Quantidade total de Letícia: {self.qtde_leticia} unidades/{self.qtde_leticia/4} jogos")
        # print(f"Quantidade total de Balanço: {self.qtde_balanco} unidades")
        # print(f"Quantidade total de Centro Comum: {self.qtde_centrocomum} unidades")
        # print(f"Quantidade total de Centro Letícia: {self.qtde_centroleticia} unidades")
        # print(f"Quantidade total de Centro Luxo: {self.qtde_centroluxo} unidades")
        with open(f'LISTA TOTAL OBJETO2.txt', 'w') as totalfeito:
            totalfeito.write(f'{self.qtde_veneza:.0f} {self.qtde_banqueta:.0f} {self.qtde_leticia:.0f} {self.qtde_balanco:.0f} {self.qtde_centrocomum:.0f} {self.qtde_centroleticia:.0f} {self.qtde_centroluxo:.0f}')
        
        self.qtde_jogoven1 = self.qtde_veneza/4
        self.jogolet = self.qtde_leticia/4
        self.atualizar_dados2()
    
    def atualizar_dados2(self):
        qtde_ven1 = str(f'{self.qtde_veneza:.0f}')
        qtde_jogoven2 = str(f'{self.qtde_jogoven1:.0f}')
        qtde_ban1 = str(f'{self.qtde_banqueta:.0f}')
        qtde_let1 = str(f'{self.qtde_leticia:.0f}')
        jogolet2 = str(f'{self.jogolet:.0f}')
        qtde_bal1 = str(f'{self.qtde_balanco:.0f}')
        qtde_ccomum = str(f'{self.qtde_centrocomum:.0f}')
        qtde_clet = str(f'{self.qtde_centroleticia:.0f}')
        qtde_cluxo = str(f'{self.qtde_centroluxo:.0f}')
        self.dados_enrol_scroll_text2 = f"1. Quantidade total de Veneza: {qtde_ven1} unidades/{qtde_jogoven2} jogos\n2. Quantidade total de Banqueta: {qtde_ban1} unidades\n3. Quantidade total de Letícia: {qtde_let1} unidades/{jogolet2} jogos\n4. Quantidade total de Balanço: {qtde_bal1} unidades\n5. Quantidade total de Centro Comum: {qtde_ccomum} unidades\n6. Quantidade total de Centro Letícia: {qtde_clet} unidades\n7. Quantidade total de Centro Luxo: {qtde_cluxo} unidades"

class DadosEntrega(Screen):
    
    dados_enrol_scroll_texten = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carregar_dados4()  # Carrega os dados ao iniciar a tela

    def on_enter(self):
        self.carregar_dados4()  # Atualiza os dados toda vez que a tela é exibida

    def carregar_dados4(self):
        self.dados4()
        self.atualizar_dados4()
    
    def dados4(self):
        with open('LISTA ENTREGA OBJETOS.txt', 'r') as file:
            linhas = file.readlines()
        
        # Remover as chaves e dividir os dados
        dados_limpios = [linha.replace('[', '').replace(']', '').split() for linha in linhas]

        # Criar o DataFrame
        df = pd.DataFrame(dados_limpios, columns=['Data', 'Enrolador', 'Objeto', 'Qtde'])

        # Convertendo colunas numéricas para o tipo correto
        df['Qtde'] = pd.to_numeric(df['Qtde'])

        # Filtrar os dados para os objetos "Veneza" e "Banqueta"

        self.qtde_veneza4 = df[df['Objeto'] == 'Veneza']['Qtde'].sum()
        self.qtde_banqueta4 = df[df['Objeto'] == 'Banqueta']['Qtde'].sum()
        self.qtde_leticia4 = df[df['Objeto'] == 'Letícia']['Qtde'].sum()
        self.qtde_balanco4 = df[df['Objeto'] == 'Balanço']['Qtde'].sum()
        self.qtde_centrocomum4 = df[df['Objeto'] == 'Ccomum']['Qtde'].sum()
        self.qtde_centroleticia4 = df[df['Objeto'] == 'Cletícia']['Qtde'].sum()
        self.qtde_centroluxo4 = df[df['Objeto'] == 'Cluxo']['Qtde'].sum()
        self.qtde_jogoven4 = self.qtde_veneza4/4
        self.jogolet4 = self.qtde_leticia4/4
        self.atualizar_dados4()
    
    def atualizar_dados4(self):
        qtde_ven4 = str(f'{self.qtde_veneza4:.0f}')
        qtde_jogoven4 = str(f'{self.qtde_jogoven4:.0f}')
        qtde_ban4 = str(f'{self.qtde_banqueta4:.0f}')
        qtde_let4 = str(f'{self.qtde_leticia4:.0f}')
        jogolet4 = str(f'{self.jogolet4:.0f}')
        qtde_bal4 = str(f'{self.qtde_balanco4:.0f}')
        qtde_ccomum4 = str(f'{self.qtde_centrocomum4:.0f}')
        qtde_clet4 = str(f'{self.qtde_centroleticia4:.0f}')
        qtde_cluxo4 = str(f'{self.qtde_centroluxo4:.0f}')
        self.dados_enrol_scroll_texten = f"1. Quantidade total de Veneza: {qtde_ven4} unidades/{qtde_jogoven4} jogos\n2. Quantidade total de Banqueta: {qtde_ban4} unidades\n3. Quantidade total de Letícia: {qtde_let4} unidades/{jogolet4} jogos\n4. Quantidade total de Balanço: {qtde_bal4} unidades\n5. Quantidade total de Centro Comum: {qtde_ccomum4} unidades\n6. Quantidade total de Centro Letícia: {qtde_clet4} unidades\n7. Quantidade total de Centro Luxo: {qtde_cluxo4} unidades"

class DadosEntregar(Screen):
    dados_enrol_scroll_texten2 = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carregar_dados5()  # Carrega os dados ao iniciar a tela

    def on_enter(self):
        self.carregar_dados5()  # Atualiza os dados toda vez que a tela é exibida

    def carregar_dados5(self):
        self.dados5()
        self.atualizar_dados5()
    
    def dados5(self):
        with open('LISTA ENTREGA OBJETOS.txt', 'r') as file:
            linhas = file.readlines()
        
        # Remover as chaves e dividir os dados
        dados_limpios = [linha.replace('[', '').replace(']', '').split() for linha in linhas]

        # Criar o DataFrame
        df = pd.DataFrame(dados_limpios, columns=['Data', 'Enrolador', 'Objeto', 'Qtde'])

        # Convertendo colunas numéricas para o tipo correto
        df['Qtde'] = pd.to_numeric(df['Qtde'])

        # Filtrar os dados para os objetos "Veneza" e "Banqueta"

        self.qtde_veneza5 = df[df['Objeto'] == 'Veneza']['Qtde'].sum()
        self.qtde_banqueta5 = df[df['Objeto'] == 'Banqueta']['Qtde'].sum()
        self.qtde_leticia5 = df[df['Objeto'] == 'Letícia']['Qtde'].sum()
        self.qtde_balanco5 = df[df['Objeto'] == 'Balanço']['Qtde'].sum()
        self.qtde_centrocomum5 = df[df['Objeto'] == 'Ccomum']['Qtde'].sum()
        self.qtde_centroleticia5 = df[df['Objeto'] == 'Cletícia']['Qtde'].sum()
        self.qtde_centroluxo5 = df[df['Objeto'] == 'Cluxo']['Qtde'].sum()
        self.qtde_jogoven5 = self.qtde_veneza5/4
        self.jogolet5 = self.qtde_leticia5/4

        # Segue a lista de enroladores para que haja a subtração entre esta lista e a lista de cadeiras entregues
        with open('LISTA ENROLADORES.txt', 'r') as file2:
            linhas2 = file2.readlines()
        
        dados_limpios2 = [linha.replace('[', '').replace(']', '').split() for linha in linhas2]

        df2 = pd.DataFrame(dados_limpios2, columns=['Data', 'Enrolador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'])

        df2['Qtde'] = pd.to_numeric(df2['Qtde'])
        df2['Val unit'] = pd.to_numeric(df2['Val unit'])
        df2['Val Total'] = pd.to_numeric(df2['Val Total'])

        self.qtde_veneza6 = df2[df2['Objeto'] == 'Veneza']['Qtde'].sum()
        self.qtde_banqueta6 = df2[df2['Objeto'] == 'Banqueta']['Qtde'].sum()
        self.qtde_leticia6 = df2[df2['Objeto'] == 'Letícia']['Qtde'].sum()
        self.qtde_balanco6 = df2[df2['Objeto'] == 'Balanço']['Qtde'].sum()
        self.qtde_centrocomum6 = df2[df2['Objeto'] == 'Ccomum']['Qtde'].sum()
        self.qtde_centroleticia6 = df2[df2['Objeto'] == 'Cletícia']['Qtde'].sum()
        self.qtde_centroluxo6 = df2[df2['Objeto'] == 'Cluxo']['Qtde'].sum()
        # Fim da lista da quantidade geral da produção dos enroladores

        self.qtde_veneza7 = self.qtde_veneza6 - self.qtde_veneza5
        self.qtde_banqueta7 = self.qtde_banqueta6 - self.qtde_banqueta5
        self.qtde_leticia7 = self.qtde_leticia6 - self.qtde_leticia5
        self.qtde_balanco7 = self.qtde_balanco6 - self.qtde_balanco5
        self.qtde_centrocomum7 = self.qtde_centrocomum6 - self.qtde_centrocomum5
        self.qtde_centroleticia7 = self.qtde_centroleticia6 - self.qtde_centroleticia5
        self.qtde_centroluxo7 = self.qtde_centroluxo6 - self.qtde_centroluxo5
        self.qtde_jogoven7 = self.qtde_veneza7/4
        self.jogolet7 = self.qtde_leticia7/4
        self.atualizar_dados5()

    
    def atualizar_dados5(self):
        qtde_ven7 = str(f'{self.qtde_veneza7:.0f}')
        qtde_jogoven7 = str(f'{self.qtde_jogoven7:.0f}')
        qtde_ban7 = str(f'{self.qtde_banqueta7:.0f}')
        qtde_let7 = str(f'{self.qtde_leticia7:.0f}')
        jogolet7 = str(f'{self.jogolet7:.0f}')
        qtde_bal7 = str(f'{self.qtde_balanco7:.0f}')
        qtde_ccomum7 = str(f'{self.qtde_centrocomum7:.0f}')
        qtde_clet7 = str(f'{self.qtde_centroleticia7:.0f}')
        qtde_cluxo7 = str(f'{self.qtde_centroluxo7:.0f}')
        self.dados_enrol_scroll_texten2 = f"1. Quantidade total de Veneza: {qtde_ven7} unidades/{qtde_jogoven7} jogos\n2. Quantidade total de Banqueta: {qtde_ban7} unidades\n3. Quantidade total de Letícia: {qtde_let7} unidades/{jogolet7} jogos\n4. Quantidade total de Balanço: {qtde_bal7} unidades\n5. Quantidade total de Centro Comum: {qtde_ccomum7} unidades\n6. Quantidade total de Centro Letícia: {qtde_clet7} unidades\n7. Quantidade total de Centro Luxo: {qtde_cluxo7} unidades"


class Vale(Screen):
    pass

class Pesquisar(Screen):
    pass

class Pesquisasol(Screen):
    pass

class Pesquisavale(Screen):
    pass

class EntregaEnrolador(Screen):
    pass

class Pesquisaentrega(Screen):
    pass

class OrcamentoEnrolador(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carregar_dados()  # Carrega os dados ao iniciar a tela

    def on_enter(self):
        self.carregar_dados()  # Atualiza os dados toda vez que a tela é exibida

    def carregar_dados(self):
        self.valor_indenrol()
        self.valor_indensol()

    def valor_indenrol(self):
        # Carregar o DataFrame
        df = pd.read_csv('LISTA ENROLADORES.txt', delimiter=' ', header=None, names=[
            'Data', 'Enrolador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'], encoding='latin1', on_bad_lines='skip')

        # Função para converter valores para float
        def extrair_valor(valor):
            try:
                # Remover caracteres não numéricos e converter para float
                valor_str = str(valor).strip()
                if valor_str:
                    return float(valor_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', ''))
                return 0.0
            except ValueError:
                return 0.0
    
        def extrair_valor2(chave):
            try:
                # Remover caracteres não numéricos e converter para float
                valor_str = str(chave).strip()
                if valor_str:
                    return str(valor_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', ''))
                return 0.0
            except ValueError:
                return 0.0

        # Aplicar a função de conversão à coluna "Valor Total"
        df['Val Total'] = df['Val Total'].apply(extrair_valor)

        self.soma_valor_total = df['Val Total'].sum()
        df['Enrolador'] = df['Enrolador'].apply(extrair_valor2)
        
        self.result = df.groupby('Enrolador')['Val Total'].sum().reset_index()
        self.result['Val Total'] = self.result['Val Total'].apply(lambda x: f"{x:.2f}")      # Exibindo o resultado
        table_data = self.result.values.tolist()

        #Criando a tabela com centralização
        self.data_table = MDDataTable(
            column_data=[
                ("Enrolador", dp(30)),
                ("Val Total", dp(30)),
            ],
            row_data=[
                (str(row[0]), str(row[1])) for row in table_data
            ],
            rows_num=60,
            size_hint=(None, None),  # Defina size_hint como None para customizar o tamanho
            size=(dp(300), dp(450)),  # Ajuste o tamanho conforme necessário
            pos_hint={'center_x': 0.3, 'center_y': 0.5} # Centraliza o data_table
        )

        #Adicionar a tabela ao layout definido no arquivo .kv
        #self.ids.box_tabela.add_widget(self.data_table)
        self.add_widget(self.data_table)

        #total do valor dos enroladores
        totalvalor2 = str(f'{self.soma_valor_total:.2f}')
        self.valor_indensol()
        self.dados_enrol_scroll_text15 = f"Total Enrol: R$ {totalvalor2}                                                                   {self.dados_enrol_scroll_text16}"

    def valor_indensol(self):
        # Carregar o DataFrame
        df = pd.read_csv('LISTA SOLDADORES.txt', delimiter=' ', header=None, names=[
            'Data', 'Soldador', 'Objeto', 'Qtde', 'Val unit', 'Val Total'], encoding='latin1', on_bad_lines='skip')

        # Função para converter valores para float
        def extrair_valor(valor):
            try:
                # Remover caracteres não numéricos e converter para float
                valor_str = str(valor).strip()
                if valor_str:
                    return float(valor_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', ''))
                return 0.0
            except ValueError:
                return 0.0

        def extrair_valor2(chave):
            try:
                # Remover caracteres não numéricos e converter para float
                valor_str = str(chave).strip()
                if valor_str:
                    return str(valor_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', ''))
                return 0.0
            except ValueError:
                return 0.0

        # Aplicar a função de conversão à coluna "Valor Total"
        df['Val Total'] = df['Val Total'].apply(extrair_valor)

        self.soma_valor_total = df['Val Total'].sum()
        df['Soldador'] = df['Soldador'].apply(extrair_valor2)

        self.result = df.groupby('Soldador')['Val Total'].sum().reset_index()
        self.result['Val Total'] = self.result['Val Total'].apply(lambda x: f"{x:.2f}")        # Exibindo o resultado
        table_data = self.result.values.tolist()

        #Criando a tabela com centralização
        self.data_table2 = MDDataTable(
            column_data=[
                ("Soldador", dp(30)),
                ("Val Total", dp(30)),
            ],
            row_data=[
                (str(row[0]), str(row[1])) for row in table_data
            ],
            rows_num=60,
            size_hint=(None, None),  # Defina size_hint como None para customizar o tamanho
            size=(dp(300), dp(450)),  # Ajuste o tamanho conforme necessário
            pos_hint={'center_x': 0.7, 'center_y': 0.5} # Centraliza o data_table
        )

        #Adicionar a tabela ao layout definido no arquivo .kv
        #self.ids.box_tabela.add_widget(self.data_table)
        self.add_widget(self.data_table2)

        # Somar os valores da coluna "Valor Total"
        self.totalsol2 = str(f'{self.soma_valor_total:.2f}')
        self.dados_enrol_scroll_text16 = f"Total Sold: R$ {self.totalsol2}"

class Backup(Screen):
    pass

class MainApp(MDApp):
    is_password_hidden = BooleanProperty(True)  # Define inicialmente como oculto
    texto = StringProperty("\nVISÃO GERAL")
    dialog = None
    dialog2 = None
    dialog3 = None
    dialog4 = None
    dialogsol5 = None
    dialogbk6 = None
    normal_color = [1.00, 0.76, 0.03, 1]
    hover_color = [0.75, 0.85, 0.85, 1]

    def build(self):
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        self.icon = 'cadeira.png'
        self.title = 'SISTEMA DA FÁBRICA ART & FIBRAS CADEIRAS'
        self.menu_items = [
            {"text": "1 Produção Enroladores", "on_release": lambda x="Item 1": self.dados_enrol('segunda') or self.menu.dismiss()},
            {"text": "2 Produção Soldadores", "on_release": lambda x="Item 2": self.dados_enrol('terceira') or self.menu.dismiss()},
            {"text": "3 Recolhimento das Cadeiras", "on_release": lambda x="Item 2": self.dados_enrol('entregaenrolador') or self.menu.dismiss()},
            {"text": "4 Dados", "trailing_icon": "chevron-right", "on_release": self.open_sub_menu3},
            {"text": "5 Vale", "trailing_icon": "cash", "on_release": lambda x="Item 5": self.dados_enrol('vale') or self.menu.dismiss()},
            {"text": "6 Orçamento", "trailing_icon": "chevron-right", "on_release": self.open_sub_menu},
            {"text": "7 Pesquisar", "trailing_icon": "chevron-right", "on_release": self.open_sub_menu2},
            {"text": "Login", "trailing_icon": "login", "on_release": lambda x="Item 9": self.dados_enrol('loginsenha') or self.menu.dismiss()},
            {"text": "Backup", "trailing_icon": "cloud-upload", "on_release": lambda x="Item 10": self.dados_enrol('backup') or self.menu.dismiss()},
            {"text": "Zerar os arquivos", "trailing_icon": "cloud-upload", "on_release": self.deletar_arquivos_txt},
            {"text": "Sobre", "trailing_icon": "information", "on_release": self.verificar_campossobre},
        ]
        self.menu = MDDropdownMenu(
            items=self.menu_items,
            md_bg_color="#FFEEBC",
            width_mult=4,
            elevation=3,
        )

        self.sub_menu_items = [
            {"text": "1 Planilha Valor Descrição", "on_release": lambda x="Planilha Valor Descrição": self.dados_enrol('orcamentoenrolador') or self.sub_menu.dismiss() or self.menu.dismiss()},
            {"text": "2 Gráficos", "on_release": lambda x="Gráficos": self.submenu_callback(x) or self.sub_menu.dismiss() or self.menu.dismiss()},
        ]

        self.sub_menu = MDDropdownMenu(
            items=self.sub_menu_items,
            width_mult=4,
            position="bottom",
            elevation=3,
        )

        self.sub_menu_items2 = [
            {"text": "1 Pesquisa Enroladores", "on_release": lambda x="Pesquisa Enroladores": self.dados_enrol('pesquisar') or self.sub_menu2.dismiss() or self.menu.dismiss()},
            {"text": "2 Pesquisa Soldadores", "on_release": lambda x="Pesquisa Soldadores": self.dados_enrol('pesquisasol') or self.sub_menu2.dismiss() or self.menu.dismiss()},
            {"text": "3 Pesquisa Vale", "on_release": lambda x="Pesquisa Vale": self.dados_enrol('pesquisavale') or self.sub_menu2.dismiss() or self.menu.dismiss()},
            {"text": "4 Pesquisa Recolhimento", "on_release": lambda x="Pesquisa Vale": self.dados_enrol('pesquisaentrega') or self.sub_menu2.dismiss() or self.menu.dismiss()},
        ]

        self.sub_menu_items3 = [
            {"text": "1 Dados Enroladores", "on_release": lambda x="Item 3": self.dados_enrol('dadosenrol') or self.sub_menu3.dismiss() or self.menu.dismiss()},
            {"text": "2 Dados Soldadores", "on_release": lambda x="Item 4": self.dados_sol('dadossol') or self.sub_menu3.dismiss() or self.menu.dismiss()},
            {"text": "3 Dados Recolhimento", "on_release": lambda x="Item 5": self.dados_sol('dadosentrega') or self.sub_menu3.dismiss() or self.menu.dismiss()},
            {"text": "4 Objetos a Recolher", "on_release": lambda x="Item 6": self.dados_sol('dadosentregar') or self.sub_menu3.dismiss() or self.menu.dismiss()},
        ]

        self.sub_menu2 = MDDropdownMenu(
            items=self.sub_menu_items2,
            width_mult=4,
            position="bottom",
            elevation=3,
        )

        self.sub_menu3 = MDDropdownMenu(
            items=self.sub_menu_items3,
            width_mult=4,
            position="bottom",
            elevation=3,
        )
        Window.bind(mouse_pos=self.on_mouse_pos)  # Vincula o rastreamento do mouse
        return Builder.load_file("sistema.kv")
    
    def toggle_password_visibility(self):
        # Alterna entre visível e oculto
        self.is_password_hidden = not self.is_password_hidden

    def on_mouse_pos(self, window, pos):
        screen = self.root.get_screen('principal')  # Acessa a tela 'principal'
        screen2 = self.root.get_screen('segunda')
        screen3 = self.root.get_screen('terceira')
        screen4 = self.root.get_screen('entregaenrolador')
        screen5 = self.root.get_screen('vale')
        screen6 = self.root.get_screen('pesquisar')
        screen7 = self.root.get_screen('pesquisasol')
        screen8 = self.root.get_screen('pesquisavale')
        screen9 = self.root.get_screen('pesquisaentrega')
        screen10 = self.root.get_screen('entregaenrolador')
        screen11 = self.root.get_screen('logininicial')
        screen12 = self.root.get_screen('loginsenha')
        screen13 = self.root.get_screen('logincadastro')
        screen14 = self.root.get_screen('backup')
        # Lista de botões a serem verificados
        buttons = [screen.ids.enr1, screen.ids.sold1, screen.ids.entreg1,
                   screen2.ids.buttonenrolador, screen3.ids.buttonsoldador, screen4.ids.buttonentrega,
                   screen5.ids.buttonfun, screen6.ids.pesquisarenrolador, screen7.ids.pesquisarsoldador, 
                   screen8.ids.pesquisarvale, screen9.ids.pesquisarentregar, screen10.ids.buttonentrega,
                   screen11.ids.entrar, screen11.ids.cadastrar, screen12.ids.cadastrar2,
                   screen13.ids.setavoltar2, screen13.ids.cadastrar3, screen14.ids.backup_botao, screen14.ids.backup_restaurar]
        
        cursor_set = False  # Inicializa o cursor_set como False

        for button in buttons:
            if button.collide_point(*pos):
                button.md_bg_color = self.hover_color
                Window.set_system_cursor('hand')  # Muda para a mãozinha
                cursor_set = True  # Marca que o cursor foi alterado
            else:
                button.md_bg_color = self.normal_color
        
        # Verifica se nenhum botão foi encontrado sob o cursor
        if not cursor_set:
            Window.set_system_cursor('arrow')  # Volta para o cursor padrão

    def open_menu(self, button):
        self.menu.caller = button
        self.menu.open()

    def open_sub_menu(self, *args):
        # Define o caller do submenu como o mesmo do menu principal
        self.sub_menu.caller = self.menu.caller

        # Posiciona o submenu ao lado direito do item "Orçamento"
        caller = self.menu.caller
        window_width = Window.width

        # Coordenadas do caller
        caller_x, caller_y = caller.to_window(caller.x, caller.y)
        
        # Calcula a nova posição do submenu
        submenu_x = caller_x + caller.width  # Posiciona ao lado direito do item
        submenu_y = caller_y  # Mesma altura do item

        # Se o submenu ultrapassar a tela, ajusta para caber
        if submenu_x + self.sub_menu.width_mult * 56 > window_width:
            submenu_x = window_width - self.sub_menu.width_mult * 56

        # Ajusta a posição do submenu e abre
        Clock.schedule_once(lambda dt: self.sub_menu.open())

        # Define a posição manualmente
        self.sub_menu._tar_x = submenu_x
        self.sub_menu._tar_y = submenu_y
    
    def submenu_callback(self, text_item):
        self.sub_menu.dismiss()
        Snackbar(text=f"Selecionado no submenu: {text_item}").open()

    def open_sub_menu2(self, *args):
        # Define o caller do submenu como o mesmo do menu principal
        self.sub_menu2.caller = self.menu.caller

        # Posiciona o submenu ao lado direito do item "Orçamento"
        caller = self.menu.caller
        window_width = Window.width

        # Coordenadas do caller
        caller_x, caller_y = caller.to_window(caller.x, caller.y)
        
        # Calcula a nova posição do submenu
        submenu2_x = caller_x + caller.width  # Posiciona ao lado direito do item
        submenu2_y = caller_y  # Mesma altura do item

        # Se o submenu ultrapassar a tela, ajusta para caber
        if submenu2_x + self.sub_menu2.width_mult * 56 > window_width:
            submenu2_x = window_width - self.sub_menu2.width_mult * 56

        # Ajusta a posição do submenu e abre
        Clock.schedule_once(lambda dt: self.sub_menu2.open())

        # Define a posição manualmente
        self.sub_menu2._tar_x = submenu2_x
        self.sub_menu2._tar_y = submenu2_y

    def open_sub_menu3(self, *args):
        # Define o caller do submenu como o mesmo do menu principal
        self.sub_menu3.caller = self.menu.caller

        # Posiciona o submenu ao lado direito do item "Orçamento"
        caller = self.menu.caller
        window_width = Window.width

        # Coordenadas do caller
        caller_x, caller_y = caller.to_window(caller.x, caller.y)
        
        # Calcula a nova posição do submenu
        submenu3_x = caller_x + caller.width  # Posiciona ao lado direito do item
        submenu3_y = caller_y  # Mesma altura do item

        # Se o submenu ultrapassar a tela, ajusta para caber
        if submenu3_x + self.sub_menu2.width_mult * 56 > window_width:
            submenu3_x = window_width - self.sub_menu2.width_mult * 56

        # Ajusta a posição do submenu e abre
        Clock.schedule_once(lambda dt: self.sub_menu3.open())

        # Define a posição manualmente
        self.sub_menu3._tar_x = submenu3_x
        self.sub_menu3._tar_y = submenu3_y
    
    def submenu_callback2(self, text_item):
        self.sub_menu2.dismiss()
        Snackbar(text=f"Selecionado no submenu: {text_item}").open()

    def sair_programa(self, *args):
        self.stop()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=f"Selecionado: {text_item}").open()

    def dados_enrol(self, screen_name):
        self.root.current = screen_name

    def dados_sol(self, screen_name):
        self.root.current = screen_name

    def change_screen(self, screen_name):
        self.root.current = screen_name
    
    def verificar_campos(self):
            # Obtendo os valores dos campos
            self.campo1 = self.root.get_screen('segunda').ids.enrolador_input.text
            self.campo2 = self.root.get_screen('segunda').ids.list_objeto.text
            try:
                self.campo3 = int(self.root.get_screen('segunda').ids.qtde_input.text)
            except ValueError:
                # Tratamento caso o valor não seja um número
                self.campo3 = 0  # ou qualquer outro valor padrão
            try:
                self.campo4 = float(self.root.get_screen('segunda').ids.valor_unitario.text)
            except ValueError:
                # Tratamento caso o valor não seja um número
                self.campo4 = 0  # ou qualquer outro valor padrão

            self.somatorio = self.campo4 * self.campo3

            if self.campo1 and self.campo2 and self.campo3 and self.campo4:
                # Se todos os campos estiverem preenchidos
                self.mostrar_dialogo_sucesso()
                self.enrolador_individual()
                self.campo1 = self.root.get_screen('segunda').ids.enrolador_input.text=""
                self.campo2 = self.root.get_screen('segunda').ids.list_objeto.text=""
                self.campo3 = self.root.get_screen('segunda').ids.qtde_input.text=""
                self.campo4 = self.root.get_screen('segunda').ids.valor_unitario.text=""
                convertertxt_em_pdf.conversao_txtpdf(self.arquivo_txt, self.arquivo_pdf)
                time.sleep(2)
                os.startfile(self.arquivo_pdf)

            else:
                toast("Preencha todos os campos!")

    def mostrar_dialogo_sucesso(self):
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Salvo",
                    buttons=[],
                )
            self.dialog.text = (
                f"Arquivo salvo com sucesso!\nO enrolador {self.campo1.capitalize()} "
                f"produziu {self.campo3} {self.campo2}s\nno valor unitário de R$ {float(self.campo4):.2f}, "
                f"lucrando R$ {float(self.somatorio):.2f}"
            )
            self.dialog.open()

    def verificar_campossobre(self):
        self.mostrar_dialogo_sucessosobre()

    def mostrar_dialogo_sucessosobre(self):
        self.dialog2 = MDDialog(
            title="PROGRAMA SISTEMA PRODUÇÃO DE CADEIRA",
            text="Desenvolvido por José Evangelista da Silva Filho\nContato: (75) 99245.6130\nSuporte: juniornyanata@gmail.com",
            buttons=[],
        )
        self.dialog2.open()

    def verificar_campos2(self):
            # Obtendo os valores dos campos
            self.campo5 = self.root.get_screen('terceira').ids.soldador_input.text
            self.campo6 = self.root.get_screen('terceira').ids.objeto_soldador.text
            try:
                self.campo7 = int(self.root.get_screen('terceira').ids.qtde_soldador.text)
            except ValueError:
                self.campo7 = 0
            try:
                self.campo8 = float(self.root.get_screen('terceira').ids.vunitario_soldador.text)
            except ValueError:
                self.campo8 = 0
            
            self.somatorio2 = self.campo8 * self.campo7

            if self.campo5 and self.campo6 and self.campo7 and self.campo8:
                # Se todos os campos estiverem preenchidos
                self.mostrar_dialogo_sucesso2()
                self.soldador_individual()
                self.campo5 = self.root.get_screen('terceira').ids.soldador_input.text=""
                self.campo6 = self.root.get_screen('terceira').ids.objeto_soldador.text=""
                self.campo7 = self.root.get_screen('terceira').ids.qtde_soldador.text=""
                self.campo8 = self.root.get_screen('terceira').ids.vunitario_soldador.text=""
                
                convertertxt_em_pdf.conversao_txtpdf(self.arquivo_txt3, self.arquivo_pdf3)
                time.sleep(2)
                os.startfile(self.arquivo_pdf3)


            else:
                toast("Preencha todos os campos!")

    def mostrar_dialogo_sucesso2(self):
        if not self.dialogsol5:
            # Cria o diálogo se ele ainda não foi criado
            self.dialogsol5 = MDDialog(
                title="Salvo",
                buttons=[],
            )
        # Atualiza o texto do diálogo com os novos dados
        self.dialogsol5.text = (
            f"Arquivo salvo com sucesso! O soldador {self.campo5.capitalize()} "
            f"produziu {self.campo7} {self.campo6}s\nno valor unitário de R$ {float(self.campo8):.2f}, "
            f"lucrando R$ {float(self.somatorio2):.2f}"
        )
        self.dialogsol5.open()

    def verificar_campos3(self):
            # Obtendo os valores dos campos
            campo1 = self.root.get_screen('vale').ids.fun_input.text
            campo2 = self.root.get_screen('vale').ids.vtotal_fun.text
            
            if campo1 and campo2:
                # Se todos os campos estiverem preenchidos
                self.mostrar_dialogo_sucesso3()
                self.vale_individual()
                campo1 = self.root.get_screen('vale').ids.fun_input.text=""
                campo2 = self.root.get_screen('vale').ids.vtotal_fun.text=""
                
                convertertxt_em_pdf.conversao_txtpdf(self.arquivo_txt4, self.arquivo_pdf4)
                time.sleep(2)
                os.startfile(self.arquivo_pdf4)


            else:
                toast("Preencha todos os campos!")

    def mostrar_dialogo_sucesso3(self):
            if not self.dialog3:
                self.dialog3 = MDDialog(
                    title="Salvo",
                    text="Arquivo salvo com sucesso!",
                    buttons=[],
                )
            self.dialog3.open()

    def verificar_campos4(self):
            # Obtendo os valores dos campos
            campo1 = self.root.get_screen('entregaenrolador').ids.entrega_enrol.text
            campo2 = self.root.get_screen('entregaenrolador').ids.list_entrega.text
            campo3 = self.root.get_screen('entregaenrolador').ids.qtde_entrega.text
            
            if campo1 and campo2 and campo3:
                # Se todos os campos estiverem preenchidos
                self.mostrar_dialogo_sucesso4()
                self.entrega_individual()
                campo1 = self.root.get_screen('entregaenrolador').ids.entrega_enrol.text=""
                campo2 = self.root.get_screen('entregaenrolador').ids.list_entrega.text=""
                campo3 = self.root.get_screen('entregaenrolador').ids.qtde_entrega.text=""

                convertertxt_em_pdf.conversao_txtpdf(self.arquivo_txt2, self.arquivo_pdf2)
                time.sleep(2)
                os.startfile(self.arquivo_pdf2)


            else:
                toast("Preencha todos os campos!")

    def mostrar_dialogo_sucesso4(self):
            if not self.dialog4:
                self.dialog4 = MDDialog(
                    title="Salvo",
                    text="Arquivo salvo com sucesso!",
                    buttons=[],
                )
            self.dialog4.open()

    def enrolador_individual(self):
        import datetime
        import locale
        # Definir o locale para português brasileiro
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        
        # Obter a data atual
        hoje = datetime.datetime.now()
        
        # Formatar a data no formato desejado
        dia_em_portugues = hoje.strftime('%A, %d de %B de %Y %H:%M')

        screen = self.root.get_screen('segunda')
        enrolador = screen.ids.enrolador_input.text.capitalize().replace(' ', '')
        with open(f'ENROLADOR {enrolador} impressao.txt', 'a', encoding="utf-8") as f:
            from datetime import datetime
            agora = datetime.now()
            data_hora_formatada = agora.strftime('%d/%m/%Y')
            f.write('\n')
            f.write('---------------------------------------------------------\n')
            f.write(str(f'Data: {dia_em_portugues}'))
            f.write('\n')

            list_objeto = self.root.get_screen('segunda').ids.list_objeto.text.capitalize()
            qtde = int(self.root.get_screen('segunda').ids.qtde_input.text)
            valor_unitario = float(self.root.get_screen('segunda').ids.valor_unitario.text)
            total = qtde * valor_unitario
            
            
            f.write('---------------------------------------------------------\n')
            f.write(f'Enrolador: {enrolador}\n')
            f.write(f'Objeto: {list_objeto}\n')
            f.write(f'Quantidade: {qtde}\n')
            f.write(f'Valor unitário: R$ {valor_unitario:.2f}\n')
            f.write(f'Valor Total: R$ {total:.2f}\n')
            f.write('Assinatura do conferencista:_____________________________\n')
            f.write('Assinatura do enrolador:_________________________________\n')
            f.write('---------------------------------------------------------\n')
            f.write('\n')

            with open(f'ENROLADOR {enrolador} planilha.txt', 'a', encoding='utf-8') as g:
                from datetime import datetime
                agora = datetime.now()
                data_formatada = agora.strftime('%d/%m/%Y')
                g.write(f'\n[{data_formatada}] [{enrolador}] [{list_objeto}] [{qtde}] [{valor_unitario:.2f}] [{total:.2f}]')
            with open('LISTA ENROLADORES.txt', 'a', encoding="ISO-8859-1") as tabela_geral:
                tabela_geral.write(f'\n[{data_formatada}] [{enrolador}] [{list_objeto}] [{qtde}] [{valor_unitario:.2f}] [{total:.2f}]')
            
            self.arquivo_txt = f"ENROLADOR {enrolador} impressao.txt"
            self.arquivo_pdf = f"ENROLADOR {enrolador} impressao.pdf"
    
    def entrega_individual(self):
        import datetime
        import locale
        # Definir o locale para português brasileiro
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        
        # Obter a data atual
        hoje = datetime.datetime.now()
        
        # Formatar a data no formato desejado
        dia_em_portugues = hoje.strftime('%A, %d de %B de %Y %H:%M')

        screen = self.root.get_screen('entregaenrolador')
        enrolador = screen.ids.entrega_enrol.text.capitalize().replace(' ', '')
        with open(f'ENTREGA {enrolador} impressao.txt', 'a', encoding="utf-8") as f:
            from datetime import datetime
            agora = datetime.now()
            data_hora_formatada = agora.strftime('%d/%m/%Y')
            f.write('\n')
            f.write('---------------------------------------------------------\n')
            f.write(str(f'Data: {dia_em_portugues}'))
            f.write('\n')

            list_objeto = self.root.get_screen('entregaenrolador').ids.list_entrega.text.capitalize()
            qtde = int(self.root.get_screen('entregaenrolador').ids.qtde_entrega.text)
            
            f.write('---------------------------------------------------------\n')
            f.write(f'Enrolador: {enrolador}\n')
            f.write(f'Objeto Entregue: {list_objeto}\n')
            f.write(f'Quantidade: {qtde}\n')
            f.write('Assinatura do conferencista:_____________________________\n')
            f.write('Assinatura do enrolador:_________________________________\n')
            f.write('---------------------------------------------------------\n')
            f.write('\n')

            with open(f'ENTREGA {enrolador} planilha.txt', 'a', encoding='utf-8') as g:
                from datetime import datetime
                agora = datetime.now()
                data_formatada = agora.strftime('%d/%m/%Y')
                g.write(f'\n[{data_formatada}] [{enrolador}] [{list_objeto}] [{qtde}]')
            with open('LISTA ENTREGA OBJETOS.txt', 'a', encoding="ISO-8859-1") as tabela_geral:
                tabela_geral.write(f'\n[{data_formatada}] [{enrolador}] [{list_objeto}] [{qtde}]')
            
            self.arquivo_txt2 = f"ENTREGA {enrolador} impressao.txt"
            self.arquivo_pdf2 = f"ENTREGA {enrolador} impressao.pdf"


    # Salva a data escolhida pelo usuario
    def on_save(self, instance, value, date_range):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        # Formatando a data em português
        formatted_date = value.strftime("%A, %d de %B de %Y")
        self.root.ids.data.text = formatted_date

    # Mostra a mensagem quando o usuario cancela a data
    def on_cancel(self, instance, value):
        self.ids.data.text = "Você cliclou em cancelar"

    # Cria o calendario
    def show_data_picker(self):
        date_dialog = MDDatePicker(year=2024, month=9, day=10)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def abrir_calculadora(self):
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(["calc"])
            elif system == "Linux":
                subprocess.run(["gnome-calculator"])
            elif system == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Calculator"])
            else:
                print(f"Sistema operacional {system} não suportado.")
        except Exception as e:
            print(f"Erro ao abrir a calculadora: {e}")

    def soldador_individual(self):
        import datetime
        import locale

        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    
        # Obter a data atual
        hoje = datetime.datetime.now()
        
        # Formatar a data no formato desejado
        dia_em_portugues = hoje.strftime('%A, %d de %B de %Y %H:%M')

        screen = self.root.get_screen('terceira')
        soldador = screen.ids.soldador_input.text.capitalize().replace(' ', '')
        with open(f'SOLDADOR {soldador} impressao.txt', 'a', encoding='utf-8') as f:
            from datetime import datetime
            agora = datetime.now()
            data_hora_formatada = agora.strftime('%d/%m/%Y %H:%M')
            print('Data:', data_hora_formatada)
            f.write('\n')
            f.write('---------------------------------------------------------\n')
            f.write(str(f'Data: {dia_em_portugues}'))
            f.write('\n')

            objeto_soldador = self.root.get_screen('terceira').ids.objeto_soldador.text.capitalize()
            qtde = int(self.root.get_screen('terceira').ids.qtde_soldador.text)
            valor_unitario = float(self.root.get_screen('terceira').ids.vunitario_soldador.text)
            total = qtde * valor_unitario

            f.write('---------------------------------------------------------\n')
            f.write(f'Soldador: {soldador}\n')
            f.write(f'Objeto: {objeto_soldador}\n')
            f.write(f'Quantidade: {qtde}\n')
            f.write(f'Valor unitário: R$ {valor_unitario:.2f}\n')
            f.write(f'Valor Total: R$ {total:.2f}\n')
            f.write('Assinatura do conferencista:_____________________________\n')
            f.write('Assinatura do soldador:_________________________________\n')
            f.write('---------------------------------------------------------\n')
            f.write('\n')
            with open(f'SOLDADOR {soldador} planilha.txt', 'a', encoding='utf-8') as g:
                from datetime import datetime
                agora = datetime.now()
                data_formatada = agora.strftime('%d/%m/%Y')
                # print(f'\nData: {data_formatada}')
                g.write(f'\n[{data_formatada}] [{soldador}] [{objeto_soldador}] [{qtde}] [{valor_unitario:.2f}] [{total:.2f}]')
            with open('LISTA SOLDADORES.txt', 'a', encoding="ISO-8859-1") as tabela_geral2:
                tabela_geral2.write(f'\n[{data_formatada}] [{soldador}] [{objeto_soldador}] [{qtde}] [{valor_unitario:.2f}] [{total:.2f}]')
            
            self.arquivo_txt3 = f"SOLDADOR {soldador} impressao.txt"
            self.arquivo_pdf3 = f"SOLDADOR {soldador} impressao.pdf"

    def vale_individual(self):
        import datetime
        import locale

        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    
        # Obter a data atual
        hoje = datetime.datetime.now()
        
        # Formatar a data no formato desejado
        dia_em_portugues = hoje.strftime('%A, %d de %B de %Y %H:%M')

        screen = self.root.get_screen('vale')
        self.fun = screen.ids.fun_input.text.capitalize().replace(' ', '')
        with open(f'VALE {self.fun} impressao.txt', 'a', encoding='utf-8') as f:
            from datetime import datetime
            agora = datetime.now()
            data_hora_formatada = agora.strftime('%d/%m/%Y %H:%M')
            print('Data:', data_hora_formatada)
            f.write('\n')
            f.write('---------------------------------------------------------\n')
            f.write(str(f'Data: {dia_em_portugues}'))
            f.write('\n')

            self.total = float(self.root.get_screen('vale').ids.vtotal_fun.text)

            f.write('---------------------------------------------------------\n')
            f.write(f'Nome: {self.fun}\n')
            f.write(f'Descrição: Vale\n')
            f.write(f'Valor Total: R$ {self.total:.2f}\n')
            f.write('Empresa: ART FIBRAS CADEIRAS - CNPJ: 52.539.378/0001-61\n')
            f.write('Assinatura do receptor:_________________________________\n')
            f.write('---------------------------------------------------------\n')
            f.write('\n')

            with open(f'VALOR VALE {self.fun}.txt', 'a') as valor_vale:
                valor_vale.write(f'\n[{self.total:.2f}]')

            with open(f'VALE TOTAL {self.fun}.txt', 'a', encoding='utf-8') as g:
                from datetime import datetime
                agora = datetime.now()
                data_formatada = agora.strftime('%d/%m/%Y')
                # print(f'\nData: {data_formatada}')
                g.write(f'\n[{data_formatada}] [{self.fun}] [Vale] [{self.total:.2f}]')
            with open('LISTA VALE TOTAL.txt', 'a', encoding="ISO-8859-1") as tabela_geral2:
                tabela_geral2.write(f'\n[{data_formatada}] [{self.fun}] [Vale] [{self.total:.2f}]')
            
            self.arquivo_txt4 = f"VALE {self.fun} impressao.txt"
            self.arquivo_pdf4 = f"VALE {self.fun} impressao.pdf"


    def pesquisar_nome(self):
        nome_pesquisado = self.root.get_screen('pesquisar').ids.search_field.text.lower()  # Deixar minúsculo para comparação
        if not nome_pesquisado:
            toast("Digite um nome para pesquisar")

        resultado = self.buscar_dados_txt(nome_pesquisado)
        self.root.get_screen('pesquisar').ids.resultado.text = resultado

        # Ler o arquivo
        df = pd.read_csv('LISTA ENROLADORES.txt', delimiter=' ', names=['Data', 'Nome', 'Objeto', 'Qt', 'V.un', 'Total'], encoding="ISO-8859-1")

        # Remover colchetes e espaços de todas as colunas que têm colchetes
        df['Nome'] = df['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Objeto'] = df['Objeto'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Total'] = df['Total'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Qt'] = df['Qt'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        # Converter 'Total' e 'Qt' para float
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
        df['Qt'] = pd.to_numeric(df['Qt'], errors='coerce')

        # Padronizar coluna 'Nome' e 'Objeto' para evitar problemas de capitalização
        df['Nome'] = df['Nome'].str.lower()
        df['Objeto'] = df['Objeto'].str.lower()


        dfv = pd.read_csv('LISTA ENTREGA OBJETOS.txt', delimiter=' ', names=['Data', 'Nome', 'Objeto','Qtde'], encoding="ISO-8859-1")

        dfv['Nome'] = dfv['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfv['Objeto'] = dfv['Objeto'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfv['Qtde'] = dfv['Qtde'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        # Converter 'Total' para float
        dfv['Qtde'] = pd.to_numeric(dfv['Qtde'], errors='coerce')

        # Padronizar coluna 'Nome' e 'Objeto' para evitar problemas de capitalização
        dfv['Nome'] = dfv['Nome'].str.lower()
        dfv['Objeto'] = dfv['Objeto'].str.lower()
        
        dfvale = pd.read_csv('LISTA VALE TOTAL.txt', delimiter=' ', names=['Data', 'Nome', 'Vale','Total'], encoding="ISO-8859-1")

        # Remover colchetes e espaços de todas as colunas que têm colchetes
        dfvale['Nome'] = dfvale['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfvale['Vale'] = dfvale['Vale'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfvale['Total'] = dfvale['Total'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfvale['Data'] = dfvale['Data'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        dfvale['Total'] = pd.to_numeric(dfvale['Total'], errors='coerce')

        dfvale['Nome'] = dfvale['Nome'].str.lower()
        dfvale['Vale'] = dfvale['Vale'].str.lower()
        dfvale['Data'] = dfvale['Data'].str.lower()

        # Verificar se o nome está na coluna 'Nome'
        if not df[df['Nome'] == nome_pesquisado].empty:
            nome_todos = df[df['Nome'] == nome_pesquisado]
            valor = nome_todos['Total'].sum()
            valorstring = f"\n  Total de {nome_pesquisado.capitalize()}: R$ {valor:.2f}"
            self.root.get_screen('pesquisar').ids.valortotal.text = valorstring

            nome_todosvale = dfvale[dfvale['Nome'] == nome_pesquisado]
            valorvale = nome_todosvale['Total'].sum()
            valorstringvale = f"Vale de {nome_pesquisado.capitalize()}:    R$ {valorvale:.2f}"
            self.root.get_screen('pesquisar').ids.valorvale.text = valorstringvale

            receber = (float(valor) - float(valorvale))
            valorstringresultado = f"{nome_pesquisado.capitalize()} receberá: R$ {receber:.2f}"
            self.root.get_screen('pesquisar').ids.valorresultado.text = valorstringresultado
                        
            # Agora corrigimos os objetos para serem comparados com strings minúsculas
            qtde_veneza = nome_todos[nome_todos['Objeto'] == 'veneza']['Qt'].sum()
            qtde_banqueta = nome_todos[nome_todos['Objeto'] == 'banqueta']['Qt'].sum()
            qtde_leticia = nome_todos[nome_todos['Objeto'] == 'letícia']['Qt'].sum()
            qtde_balanco = nome_todos[nome_todos['Objeto'] == 'balanço']['Qt'].sum()
            qtde_centrocomum = nome_todos[nome_todos['Objeto'] == 'ccomum']['Qt'].sum()
            qtde_centroleticia = nome_todos[nome_todos['Objeto'] == 'cletícia']['Qt'].sum()
            qtde_centroluxo = nome_todos[nome_todos['Objeto'] == 'cluxo']['Qt'].sum()
            karina = nome_todos[nome_todos['Objeto'] == 'karina']['Qt'].sum()

            nome_todose = dfv[dfv['Nome'] == nome_pesquisado]
            valore = nome_todose['Qtde'].sum()

            qtde_venezae = nome_todose[nome_todose['Objeto'] == 'veneza']['Qtde'].sum()
            qtde_banquetae = nome_todose[nome_todose['Objeto'] == 'banqueta']['Qtde'].sum()
            qtde_leticiae = nome_todose[nome_todose['Objeto'] == 'letícia']['Qtde'].sum()
            qtde_balancoe = nome_todose[nome_todose['Objeto'] == 'balanço']['Qtde'].sum()
            qtde_centrocomume = nome_todose[nome_todose['Objeto'] == 'ccomum']['Qtde'].sum()
            qtde_centroleticiae = nome_todose[nome_todose['Objeto'] == 'cletícia']['Qtde'].sum()
            qtde_centroluxoe = nome_todose[nome_todose['Objeto'] == 'cluxo']['Qtde'].sum()
            karinae = nome_todose[nome_todose['Objeto'] == 'karina']['Qtde'].sum()

            total_entregarveneza = qtde_veneza - qtde_venezae
            total_entregarbanqueta = qtde_banqueta - qtde_banquetae
            total_entregarleticia = qtde_leticia - qtde_leticiae
            total_entregarbalanco = qtde_balanco - qtde_balancoe
            total_entregarccomum = qtde_centrocomum - qtde_centrocomume
            total_entregarcleticia = qtde_centroleticia - qtde_centroleticiae
            total_entregarcluxo = qtde_centroluxo - qtde_centroluxoe
            total_entregarkarina = karina- karinae

            cadeiratotal = f"_________________________________________________________\n PRODUÇÃO TOTAL:\n\n Veneza: {qtde_veneza} unidades\n    Banqueta: {qtde_banqueta} unidades\nLetícia: {qtde_leticia} unidades\nBalanço: {qtde_balanco} unidades\n   Centro Comum: {qtde_centrocomum} unidades\n   Centro Letícia: {qtde_centroleticia} unidades\n   Centro Luxo: {qtde_centroluxo} unidades\n Karina: {karina} unidades"
            cadeiratotalentrega = f"_________________________________________________________\n TOTAL DE ENTREGA:\n\n Veneza: {qtde_venezae} unidades\n    Banqueta: {qtde_banquetae} unidades\nLetícia: {qtde_leticiae} unidades\nBalanço: {qtde_balancoe} unidades\n   Centro Comum: {qtde_centrocomume} unidades\n   Centro Letícia: {qtde_centroleticiae} unidades\n   Centro Luxo: {qtde_centroluxoe} unidades\n Karina: {karinae} unidades"
            cadeiratotalentregar = f"_________________________________________________________\n ENTREGAR:\n\n Veneza: {total_entregarveneza} unidades\n    Banqueta: {total_entregarbanqueta} unidades\nLetícia: {total_entregarleticia} unidades\nBalanço: {total_entregarbalanco} unidades\n   Centro Comum: {total_entregarccomum} unidades\n   Centro Letícia: {total_entregarcleticia} unidades\n   Centro Luxo: {total_entregarcluxo} unidades\n Karina: {total_entregarkarina} unidades"
            self.root.get_screen('pesquisar').ids.cadeira.text = cadeiratotal
            self.root.get_screen('pesquisar').ids.cadeiraentrega.text = cadeiratotalentrega
            self.root.get_screen('pesquisar').ids.cadeiraentregar.text = cadeiratotalentregar

        # Verificar se o nome está na coluna 'Objeto'
        elif not df[df['Objeto'] == nome_pesquisado].empty:
            objeto_todos = df[df['Objeto'] == nome_pesquisado]
            valor2 = objeto_todos['Total'].sum()
            valorstring2 = f"Total de valor em {nome_pesquisado.capitalize()}: R$ {valor2:.2f}"
            self.root.get_screen('pesquisar').ids.valortotal.text = valorstring2

            #nome_todosvale2 = dfvale[dfvale['Data'] == nome_pesquisado]
            #valorvale2 = nome_todosvale2['Total'].sum()
            # valorstringvale2 = f" "
            # self.root.get_screen('pesquisar').ids.valorvale.text = valorstringvale2

            # valorstringresultado2 = f" "
            # self.root.get_screen('pesquisar').ids.valorresultado.text = valorstringresultado2

            # Agora corrigimos os objetos para serem comparados com strings minúsculas
            qtde_veneza2 = objeto_todos[objeto_todos['Objeto'] == 'veneza']['Qt'].sum()
            qtde_banqueta2 = objeto_todos[objeto_todos['Objeto'] == 'banqueta']['Qt'].sum()
            qtde_leticia2 = objeto_todos[objeto_todos['Objeto'] == 'letícia']['Qt'].sum()
            qtde_balanco2 = objeto_todos[objeto_todos['Objeto'] == 'balanço']['Qt'].sum()
            qtde_centrocomum2 = objeto_todos[objeto_todos['Objeto'] == 'ccomum']['Qt'].sum()
            qtde_centroleticia2 = objeto_todos[objeto_todos['Objeto'] == 'cletícia']['Qt'].sum()
            qtde_centroluxo2 = objeto_todos[objeto_todos['Objeto'] == 'cluxo']['Qt'].sum()

            cadeiratotal2 = f"_________________________________________________________\n TOTAL DE CADEIRAS:\n Veneza: {qtde_veneza2} unidades\n    Banqueta: {qtde_banqueta2} unidades\nLetícia: {qtde_leticia2} unidades\nBalanço: {qtde_balanco2} unidades\n   Centro Comum: {qtde_centrocomum2} unidades\n   Centro Letícia: {qtde_centroleticia2} unidades\n   Centro Luxo: {qtde_centroluxo2} unidades"
            self.root.get_screen('pesquisar').ids.cadeira.text = cadeiratotal2


        # Verificar se o nome está na coluna 'Data'
        elif not df[df['Data'] == nome_pesquisado].empty:
            data_todos = df[df['Data'] == nome_pesquisado]
            valor3 = data_todos['Total'].sum()
            valorstring3 = f"Total da data {nome_pesquisado.capitalize()}: R$ {valor3:.2f}"
            self.root.get_screen('pesquisar').ids.valortotal.text = valorstring3

            nome_todosvale3 = dfvale[dfvale['Data'] == nome_pesquisado]
            valorvale3 = nome_todosvale3['Total'].sum()
            valorstringvale3 = f"Vale de {nome_pesquisado.capitalize()}:  R$ {valorvale3:.2f}"
            self.root.get_screen('pesquisar').ids.valorvale.text = valorstringvale3

            receber3 = (float(valor3) - float(valorvale3))
            valorstringresultado3 = f"{nome_pesquisado.capitalize()} receberá: R$ {receber3:.2f}"
            self.root.get_screen('pesquisar').ids.valorresultado.text = valorstringresultado3

            # Agora corrigimos os objetos para serem comparados com strings minúsculas
            qtde_veneza3 = data_todos[data_todos['Objeto'] == 'veneza']['Qt'].sum()
            qtde_banqueta3 = data_todos[data_todos['Objeto'] == 'banqueta']['Qt'].sum()
            qtde_leticia3 = data_todos[data_todos['Objeto'] == 'letícia']['Qt'].sum()
            qtde_balanco3 = data_todos[data_todos['Objeto'] == 'balanço']['Qt'].sum()
            qtde_centrocomum3 = data_todos[data_todos['Objeto'] == 'ccomum']['Qt'].sum()
            qtde_centroleticia3 = data_todos[data_todos['Objeto'] == 'cletícia']['Qt'].sum()
            qtde_centroluxo3 = data_todos[data_todos['Objeto'] == 'cluxo']['Qt'].sum()

            cadeiratotal3 = f"_________________________________________________________\n TOTAL DE CADEIRAS:\n Veneza: {qtde_veneza3} unidades\n    Banqueta: {qtde_banqueta3} unidades\nLetícia: {qtde_leticia3} unidades\nBalanço: {qtde_balanco3} unidades\n   Centro Comum: {qtde_centrocomum3} unidades\n   Centro Letícia: {qtde_centroleticia3} unidades\n   Centro Luxo: {qtde_centroluxo3} unidades"
            self.root.get_screen('pesquisar').ids.cadeira.text = cadeiratotal3

        elif df[df['Nome'] == nome_pesquisado].empty:
            nome_todoses = df[df['Nome'] == nome_pesquisado]
            valores = nome_todoses['Total'].sum()
            valorstringes = f""
            self.root.get_screen('pesquisar').ids.valortotal.text = valorstringes

            nome_todosvalees = dfvale[dfvale['Nome'] == nome_pesquisado]
            valorvalees = nome_todosvalees['Total'].sum()
            valorstringvalees = f"                      "
            self.root.get_screen('pesquisar').ids.valorvale.text = valorstringvalees

            receberes = (float(valores) - float(valorvalees))
            valorstringresultadoes = f"          "
            self.root.get_screen('pesquisar').ids.valorresultado.text = valorstringresultadoes
                        
            # Agora corrigimos os objetos para serem comparados com strings minúsculas
            qtde_venezaes = nome_todoses[nome_todoses['Objeto'] == 'veneza']['Qt'].sum()
            qtde_banquetaes = nome_todoses[nome_todoses['Objeto'] == 'banqueta']['Qt'].sum()
            qtde_leticiaes = nome_todoses[nome_todoses['Objeto'] == 'letícia']['Qt'].sum()
            qtde_balancoes = nome_todoses[nome_todoses['Objeto'] == 'balanço']['Qt'].sum()
            qtde_centrocomumes = nome_todoses[nome_todoses['Objeto'] == 'ccomum']['Qt'].sum()
            qtde_centroleticiaes = nome_todoses[nome_todoses['Objeto'] == 'cletícia']['Qt'].sum()
            qtde_centroluxoes = nome_todoses[nome_todoses['Objeto'] == 'cluxo']['Qt'].sum()
            karinaes = nome_todoses[nome_todoses['Objeto'] == 'karina']['Qt'].sum()

            cadeiratotales = f""
            cadeiratotalentregaes = f""
            cadeiratotalentregares = f""
            self.root.get_screen('pesquisar').ids.cadeira.text = cadeiratotales
            self.root.get_screen('pesquisar').ids.cadeiraentrega.text = cadeiratotalentregaes
            self.root.get_screen('pesquisar').ids.cadeiraentregar.text = cadeiratotalentregares

        # Caso nenhum valor seja encontrado
        else:
            self.root.get_screen('pesquisar').ids.valortotal.text = f"Nenhum valor encontrado"

    def buscar_dados_txt(self, nome):
        resultados = []
        try:
            with open("LISTA ENROLADORES.txt", "r", encoding="ISO-8859-1") as arquivo:
                for linha in arquivo:
                    if nome.lower() in linha.lower():
                        resultados.append(linha.strip().replace("[", "  ").replace("]", "  "))
            if resultados:
                return (
                    " Data          Nome      Objeto        Qt     V.un       Total\n" + 
                    "_________________________________________________________" + "\n" + 
                    "\n".join(resultados) + "\n_________________________________________________________"
                )
            else:
                return "Nome não encontrado"
        except FileNotFoundError:
            return "Arquivo não encontrado"
        
    def pesquisar_soldador(self):
        nome_pesquisadosol = self.root.get_screen('pesquisasol').ids.sol_field.text
        if not nome_pesquisadosol:
            toast("Digite um nome para pesquisar")

        resultadosol = self.buscar_dados_txt2(nome_pesquisadosol)
        self.root.get_screen('pesquisasol').ids.resultadosol.text = resultadosol

        df = pd.read_csv('LISTA SOLDADORES.txt', delimiter=' ', names=['Data', 'Nome', 'Objeto', 'Qt', 'V.un', 'Total'], encoding="ISO-8859-1")

        # Remover colchetes e espaços de todas as colunas que têm colchetes
        df['Nome'] = df['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Objeto'] = df['Objeto'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Total'] = df['Total'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Data'] = df['Data'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        # Converter 'Total' para float
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

        # Padronizar coluna 'Nome' e 'Objeto' para evitar problemas de capitalização
        df['Nome'] = df['Nome'].str.lower()
        df['Objeto'] = df['Objeto'].str.lower()
        df['Data'] = df['Data'].str.lower()

        dfvale = pd.read_csv('LISTA VALE TOTAL.txt', delimiter=' ', names=['Data', 'Nome', 'Vale','Total'], encoding="ISO-8859-1")

        # Remover colchetes e espaços de todas as colunas que têm colchetes
        dfvale['Nome'] = dfvale['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfvale['Vale'] = dfvale['Vale'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfvale['Total'] = dfvale['Total'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        dfvale['Data'] = dfvale['Data'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        dfvale['Total'] = pd.to_numeric(dfvale['Total'], errors='coerce')

        dfvale['Nome'] = dfvale['Nome'].str.lower()
        dfvale['Vale'] = dfvale['Vale'].str.lower()
        dfvale['Data'] = dfvale['Data'].str.lower()

        # Verificar se o nome está na coluna 'Nome'
        if not df[df['Nome'] == nome_pesquisadosol].empty:
            nome_todos = df[df['Nome'] == nome_pesquisadosol]
            valor = nome_todos['Total'].sum()
            valorstring = f"Total de {nome_pesquisadosol.capitalize()}: R$ {valor:.2f}"
            self.root.get_screen('pesquisasol').ids.valortotal2.text = valorstring


            nome_todosvale2 = dfvale[dfvale['Nome'] == nome_pesquisadosol]
            valorvale2 = nome_todosvale2['Total'].sum()
            valorstringvale2 = f"Vale de {nome_pesquisadosol.capitalize()}:    R$ {valorvale2:.2f}"
            self.root.get_screen('pesquisasol').ids.valorvalesol.text = valorstringvale2

            receber2 = (float(valor) - float(valorvale2))
            valorstringresultado2 = f"{nome_pesquisadosol.capitalize()} receberá: R$ {receber2:.2f}"
            self.root.get_screen('pesquisasol').ids.valorresultadosol.text = valorstringresultado2

        # Verificar se o nome está na coluna 'Objeto'
        elif not df[df['Objeto'] == nome_pesquisadosol].empty:
            objeto_todos = df[df['Objeto'] == nome_pesquisadosol]
            valor2 = objeto_todos['Total'].sum()
            valorstring2 = f"Total de {nome_pesquisadosol.capitalize()}: R$ {valor2:.2f}"
            self.root.get_screen('pesquisasol').ids.valortotal2.text = valorstring2
        
        elif not df[df['Data'] == nome_pesquisadosol].empty:
            objeto_todos = df[df['Data'] == nome_pesquisadosol]
            valor3 = objeto_todos['Total'].sum()
            valorstring3 = f"Total da data {nome_pesquisadosol.capitalize()}: R$ {valor3:.2f}"
            self.root.get_screen('pesquisasol').ids.valortotal2.text = valorstring3

        # Caso nenhum valor seja encontrado
        else:
            self.root.get_screen('pesquisasol').ids.valortotal2.text = f"Nenhum valor encontrado"


    def buscar_dados_txt2(self, nomesol):
        resultadossol = []
        try:
            with open("LISTA SOLDADORES.txt", "r") as arquivo:
                for linha in arquivo:
                    if nomesol.lower() in linha.lower():
                        resultadossol.append(linha.strip().replace("[", "  ").replace("]", "  "))
            if resultadossol:
                return " Data          Nome      Objeto        Qt     V.un       Total\n" + "_________________________________________________________" + "\n" + "\n".join(resultadossol) + "\n_________________________________________________________"
            else:
                return "Nome não encontrado"
        except FileNotFoundError:
            return "Arquivo não encontrado"

    def pesquisar_vale(self):
        nome_pesquisadovale = self.root.get_screen('pesquisavale').ids.vale_field.text
        if not nome_pesquisadovale:
            toast("Digite um nome para pesquisar")

        resultadovale = self.buscar_dados_txt3(nome_pesquisadovale)
        self.root.get_screen('pesquisavale').ids.resultadovale.text = resultadovale

        df = pd.read_csv('LISTA VALE TOTAL.txt', delimiter=' ', names=['Data', 'Nome', 'Vale','Total'], encoding="ISO-8859-1")

        # Remover colchetes e espaços de todas as colunas que têm colchetes
        df['Nome'] = df['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Vale'] = df['Vale'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Total'] = df['Total'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Data'] = df['Data'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        # Converter 'Total' para float
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

        # Padronizar coluna 'Nome' e 'Objeto' para evitar problemas de capitalização
        df['Nome'] = df['Nome'].str.lower()
        df['Vale'] = df['Vale'].str.lower()
        df['Data'] = df['Data'].str.lower()

        # Verificar se o nome está na coluna 'Nome'
        if not df[df['Nome'] == nome_pesquisadovale].empty:
            nome_todos = df[df['Nome'] == nome_pesquisadovale]
            valor = nome_todos['Total'].sum()
            valorstring = f"Total de {nome_pesquisadovale.capitalize()}: R$ {valor:.2f}"
            self.root.get_screen('pesquisavale').ids.valortotal3.text = valorstring

        # Verificar se o nome está na coluna 'Objeto'
        elif not df[df['Vale'] == nome_pesquisadovale].empty:
            objeto_todos = df[df['Vale'] == nome_pesquisadovale]
            valor2 = objeto_todos['Total'].sum()
            valorstring2 = f"Total de {nome_pesquisadovale.capitalize()}: R$ {valor2:.2f}"
            self.root.get_screen('pesquisavale').ids.valortotal3.text = valorstring2
        
        elif not df[df['Data'] == nome_pesquisadovale].empty:
            objeto_todos = df[df['Data'] == nome_pesquisadovale]
            valor3 = objeto_todos['Total'].sum()
            valorstring3 = f"Total da data {nome_pesquisadovale.capitalize()}: R$ {valor3:.2f}"
            self.root.get_screen('pesquisavale').ids.valortotal3.text = valorstring3
                # Caso nenhum valor seja encontrado
        else:
            self.root.get_screen('pesquisavale').ids.valortotal3.text = f"Nenhum valor encontrado"


    def buscar_dados_txt3(self, nomevale):
        resultadosvale = []
        try:
            with open("LISTA VALE TOTAL.txt", "r") as arquivo:
                for linha in arquivo:
                    if nomevale.lower() in linha.lower():
                        resultadosvale.append(linha.strip().replace("[", "  ").replace("]", "  "))
            if resultadosvale:
                return "        Data          Nome        Desc.        Valor\n" + "_________________________________________________________" + "\n" + "\n".join(resultadosvale) + "\n_________________________________________________________"
            else:
                return "Nome não encontrado"
        except FileNotFoundError:
            return "Arquivo não encontrado"

    def pesquisar_entrega(self):
        nome_pesquisadaentrega = self.root.get_screen('pesquisaentrega').ids.entrega_field.text
        if not nome_pesquisadaentrega:
            toast("Digite um nome para pesquisar")

        resultadoentrega = self.buscar_dados_txt4(nome_pesquisadaentrega)
        self.root.get_screen('pesquisaentrega').ids.resultadoentrega.text = resultadoentrega

        df = pd.read_csv('LISTA ENTREGA OBJETOS.txt', delimiter=' ', names=['Data', 'Nome', 'Objeto','Qtde'], encoding="ISO-8859-1")

        # Remover colchetes e espaços de todas as colunas que têm colchetes
        df['Nome'] = df['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Objeto'] = df['Objeto'].str.replace(r'[\[\]]', '', regex=True).str.strip()
        df['Qtde'] = df['Qtde'].str.replace(r'[\[\]]', '', regex=True).str.strip()

        # Converter 'Total' para float
        df['Qtde'] = pd.to_numeric(df['Qtde'], errors='coerce')

        # Padronizar coluna 'Nome' e 'Objeto' para evitar problemas de capitalização
        df['Nome'] = df['Nome'].str.lower()
        df['Objeto'] = df['Objeto'].str.lower()
        

        # Verificar se o nome está na coluna 'Nome'
        if not df[df['Nome'] == nome_pesquisadaentrega].empty:
            nome_todos = df[df['Nome'] == nome_pesquisadaentrega]
            # Agora corrigimos os objetos para serem comparados com strings minúsculas
            qtde_veneza7 = nome_todos[nome_todos['Objeto'] == 'veneza']['Qtde'].sum()
            qtde_banqueta7 = nome_todos[nome_todos['Objeto'] == 'banqueta']['Qtde'].sum()
            qtde_leticia7 = nome_todos[nome_todos['Objeto'] == 'letícia']['Qtde'].sum()
            qtde_balanco7 = nome_todos[nome_todos['Objeto'] == 'balanço']['Qtde'].sum()
            qtde_centrocomum7 = nome_todos[nome_todos['Objeto'] == 'ccomum']['Qtde'].sum()
            qtde_centroleticia7 = nome_todos[nome_todos['Objeto'] == 'cletícia']['Qtde'].sum()
            qtde_centroluxo7 = nome_todos[nome_todos['Objeto'] == 'cluxo']['Qtde'].sum()

            valorstring = f"Veneza: {qtde_veneza7} unidades\n    Banqueta: {qtde_banqueta7} unidades\nLetícia: {qtde_leticia7} unidades\nBalanço: {qtde_balanco7} unidades\n   Centro Comum: {qtde_centrocomum7} unidades\n   Centro Letícia: {qtde_centroleticia7} unidades\n   Centro Luxo: {qtde_centroluxo7} unidades"
            self.root.get_screen('pesquisaentrega').ids.valortotal4.text = valorstring

        # Verificar se o nome está na coluna 'Objeto'
        elif not df[df['Objeto'] == nome_pesquisadaentrega].empty:
            objeto_todos = df[df['Objeto'] == nome_pesquisadaentrega]

            qtde_veneza8 = objeto_todos[objeto_todos['Objeto'] == 'veneza']['Qtde'].sum()
            qtde_banqueta8 = objeto_todos[objeto_todos['Objeto'] == 'banqueta']['Qtde'].sum()
            qtde_leticia8 = objeto_todos[objeto_todos['Objeto'] == 'letícia']['Qtde'].sum()
            qtde_balanco8 = objeto_todos[objeto_todos['Objeto'] == 'balanço']['Qtde'].sum()
            qtde_centrocomum8 = objeto_todos[objeto_todos['Objeto'] == 'ccomum']['Qtde'].sum()
            qtde_centroleticia8 = objeto_todos[objeto_todos['Objeto'] == 'cletícia']['Qtde'].sum()
            qtde_centroluxo8 = objeto_todos[objeto_todos['Objeto'] == 'cluxo']['Qtde'].sum()

            valorstring2 = f"Veneza: {qtde_veneza8} unidades\n    Banqueta: {qtde_banqueta8} unidades\nLetícia: {qtde_leticia8} unidades\nBalanço: {qtde_balanco8} unidades\n   Centro Comum: {qtde_centrocomum8} unidades\n   Centro Letícia: {qtde_centroleticia8} unidades\n   Centro Luxo: {qtde_centroluxo8} unidades"
            self.root.get_screen('pesquisaentrega').ids.valortotal4.text = valorstring2
        
        elif not df[df['Data'] == nome_pesquisadaentrega].empty:
            data_todos = df[df['Data'] == nome_pesquisadaentrega]

            qtde_veneza9 = data_todos[data_todos['Objeto'] == 'veneza']['Qtde'].sum()
            qtde_banqueta9 = data_todos[data_todos['Objeto'] == 'banqueta']['Qtde'].sum()
            qtde_leticia9 = data_todos[data_todos['Objeto'] == 'letícia']['Qtde'].sum()
            qtde_balanco9 = data_todos[data_todos['Objeto'] == 'balanço']['Qtde'].sum()
            qtde_centrocomum9 = data_todos[data_todos['Objeto'] == 'ccomum']['Qtde'].sum()
            qtde_centroleticia9 = data_todos[data_todos['Objeto'] == 'cletícia']['Qtde'].sum()
            qtde_centroluxo9 = data_todos[data_todos['Objeto'] == 'cluxo']['Qtde'].sum()

            valorstring3 = f"Veneza: {qtde_veneza9} unidades\n    Banqueta: {qtde_banqueta9} unidades\nLetícia: {qtde_leticia9} unidades\nBalanço: {qtde_balanco9} unidades\n   Centro Comum: {qtde_centrocomum9} unidades\n   Centro Letícia: {qtde_centroleticia9} unidades\n   Centro Luxo: {qtde_centroluxo9} unidades"
            self.root.get_screen('pesquisaentrega').ids.valortotal4.text = valorstring3
                # Caso nenhum valor seja encontrado
        else:
            self.root.get_screen('pesquisaentrega').ids.valortotal4.text = f"Nenhum valor encontrado"

    def buscar_dados_txt4(self, nomeentrega):
        resultadosentrega = []
        try:
            with open("LISTA ENTREGA OBJETOS.txt", "r") as arquivo:
                for linha in arquivo:
                    if nomeentrega.lower() in linha.lower():
                        resultadosentrega.append(linha.strip().replace("[", "  ").replace("]", "  "))
            if resultadosentrega:
                return "        Data          Nome        Objeto        Qtde\n" + "_________________________________________________________" + "\n" + "\n".join(resultadosentrega) + "\n_________________________________________________________"
            else:
                return "Nome não encontrado"
        except FileNotFoundError:
            return "Arquivo não encontrado"

    def hash_senha(self, senha):
        if isinstance(senha, str):
            return hashlib.sha256(senha.encode()).hexdigest()
        else:
            raise ValueError("Senha deve ser uma string")
        
    def logincadastrado(self):
        usuariocadastrado = self.root.get_screen('logincadastro').ids.usuario2.text
        senhaativa = self.root.get_screen('logincadastro').ids.senhaconfirmada.text
        senhaativa2 = self.root.get_screen('logincadastro').ids.senhateste.text
        senha_criptografada = self.hash_senha(senhaativa)
        if usuariocadastrado and senhaativa:
            if senhaativa2 == senhaativa:
                with open(f'LOGINACESSO.txt', 'w', encoding='utf-8') as acessologin:
                    acessologin.write(f'{usuariocadastrado}')
                with open(f'SENHAACESSO.txt', 'w', encoding='utf-8') as acessosenha:
                    acessosenha.write(senha_criptografada)
                usuariocadastrado = self.root.get_screen('logincadastro').ids.usuario2.text=""
                senhaativa = self.root.get_screen('logincadastro').ids.senhaconfirmada.text=""
                senhaativa2 = self.root.get_screen('logincadastro').ids.senhateste.text=""
            else:
                toast("A senha de confirmação não é igual a primeira senha")
        elif not usuariocadastrado and senhaativa:
            toast(" ")
        else:
            toast("Campo(s) vazio(s). Preencha!")

    def loginacessototal(self):
        usuarioentrar = self.root.get_screen('loginsenha').ids.usuario.text
        senhaentrar = self.root.get_screen('loginsenha').ids.senha.text

        with open(f'LOGINACESSO.txt', 'r', encoding='utf-8') as acesso1:
            conteudo1 = acesso1.read()
        with open(f'SENHAACESSO.txt', 'r', encoding='utf-8') as acesso2:
            conteudo2 = acesso2.read()

        senha_criptografada = self.hash_senha(senhaentrar) #senha descriptografada

        if usuarioentrar == conteudo1 and senha_criptografada == conteudo2:
            self.root.current = 'principal'
            usuarioentrar = self.root.get_screen('loginsenha').ids.usuario.text=""
            senhaentrar = self.root.get_screen('loginsenha').ids.senha.text=""
        else:
                toast("Usuário ou senha incorretos!")

    def loginentrada(self):
            # Obtendo os valores dos campos
            login = self.root.get_screen('loginsenha').ids.usuario.text
            senha = self.root.get_screen('loginsenha').ids.senha.text
            
            if login and senha:
                # Se todos os campos estiverem preenchidos
                self.loginacessototal()
                # login = self.root.get_screen('loginsenha').ids.usuario.text=""
                # senha = self.root.get_screen('loginsenha').ids.senha.text=""

            else:
                toast("Login e senha não coincidem!")
    
    def iniciar_backup(self):
        # Verifique se o 'progress_bar' está carregado em 'self.root.ids'
        backup_screen = self.root.get_screen('backup')  # Obtém a tela 'backup' no ScreenManager
        if 'progress' in backup_screen.ids:
            self.increment_value = 0  # Inicializa o valor de progresso
            backup_screen.ids.progress.value = 0
            Clock.schedule_interval(self.atualizar_progresso, 0.1)
            Clock.schedule_once(self.realizar_backup, 2)
        else:
            print("Erro: 'progress' não encontrado no root.ids. Verifique o arquivo KV para garantir que o ID está correto.")
            #print(self.root.get_screen('backup').ids)

    def realizar_backup(self, *args):
        # source_file = r'C:\Users\curso\OneDrive\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA'  # Certifique-se do caminho correto
        # destination_dir = r'C:\Users\curso\OneDrive\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA\backup_destino'
        
        source_dir = r'C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA'  # Diretório onde estão os arquivos .txt
        destination_dir = r'C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA\backup_destino'

        # if not os.path.exists(source_file):
        #     print(f"Erro: O arquivo '{source_file}' não existe.")
        #     return

        # Cria uma pasta de backup com a data e hora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        destination = os.path.join(destination_dir, f'backup_{timestamp}')
        os.makedirs(destination, exist_ok=True)

        # Copia o arquivo
        # shutil.copy(source_file, destination)
        # print(f'Backup do arquivo {source_file} criado em {destination}')
        for filename in os.listdir(source_dir):
            if filename.endswith('.txt'):
                source_file = os.path.join(source_dir, filename)
                shutil.copy(source_file, destination)
                print(f'Backup do arquivo {filename} criado em {destination}')
        # Exibe mensagem de sucesso
        self.mostrar_dialogo_sucesso_bk()

    def atualizar_progresso(self, dt):
            # Incrementa a barra até 100%
            backup_screen = self.root.get_screen('backup')  # Acessa a tela 'backup'
            if self.increment_value < 100:
                self.increment_value += 5
                backup_screen.ids.progress.value = self.increment_value
            else:
                backup_screen.ids.progress.value = 100
                Clock.unschedule(self.atualizar_progresso)

    def mostrar_dialogo_sucesso_bk(self):
        # Exibe mensagem de sucesso ao completar o backup
        if not self.dialogbk6:
            self.dialogbk6 = MDDialog(
                title="Backup Concluído!",
                text="O backup foi realizado com sucesso.",
                buttons=[MDRaisedButton(text="OK", on_release=self.fechar_dialogo_bk)]
            )
        self.dialogbk6.open()

    def fechar_dialogo_bk(self, *args):
        self.dialogbk6.dismiss()
        backup_screen3 = self.root.get_screen('backup')
        backup_screen3.ids.progress.value = 0  # Reseta a barra de progresso
    
    def iniciar_restauracao(self):
        # Obtém a tela 'backup' no ScreenManager para atualizar a barra de progresso, se necessário
        backup_screen = self.root.get_screen('backup')
        if 'progress' in backup_screen.ids:
            self.increment_value = 0  # Inicializa o valor de progresso
            backup_screen.ids.progress.value = 0
            Clock.schedule_interval(self.atualizar_progresso, 0.1)
            Clock.schedule_once(self.realizar_restauracao, 2)
        else:
            print("Erro: 'progress' não encontrado no root.ids. Verifique o arquivo KV para garantir que o ID está correto.")

    def realizar_restauracao(self, *args):
        # Diretório onde os backups são armazenados
        backup_dir = r'C:\Users\curso\OneDrive\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA\backup_destino'
        # Diretório de destino para restaurar os arquivos
        original_dir = r'C:\Users\curso\OneDrive\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA'

        # Encontre o último backup criado
        backups = [f for f in os.listdir(backup_dir) if f.startswith('backup_')]
        if not backups:
            print("Nenhum backup encontrado para restaurar.")
            return

        # Ordena e seleciona o último backup pelo nome (timestamp mais recente)
        latest_backup = sorted(backups)[-1]
        latest_backup_path = os.path.join(backup_dir, latest_backup)

        # Restaura cada arquivo .txt do último backup para o diretório original
        for filename in os.listdir(latest_backup_path):
            if filename.endswith('.txt'):
                source_file = os.path.join(latest_backup_path, filename)
                destination_file = os.path.join(original_dir, filename)
                shutil.copy(source_file, destination_file)
                print(f'Arquivo {filename} restaurado para {original_dir}')
        
        # Exibe mensagem de sucesso
        self.mostrar_dialogo_sucesso_re()

    def mostrar_dialogo_sucesso_re(self):
        # Exibe mensagem de sucesso ao completar a restauração
        if not self.dialogbk6:
            self.dialogbk6 = MDDialog(
                title="Restauração Concluída!",
                text="A restauração foi realizada com sucesso.",
                buttons=[MDRaisedButton(text="OK", on_release=self.fechar_dialogo_bk)]
            )
        self.dialogbk6.open()

    def deletar_arquivos_txt(self):

        # Diretório onde os arquivos .txt estão armazenados
        target_dir = r'C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA'

        # Lista todos os arquivos .txt e os remove
        for filename in os.listdir(target_dir):
            arquivo = ('.txt', '.pdf')
            if filename.endswith(arquivo) and filename not in ('LOGINACESSO.txt', 'SENHAACESSO.txt'):
                file_path = os.path.join(target_dir, filename)
                try:
                    os.remove(file_path)
                    print(f'Arquivo {filename} deletado com sucesso.')
                except Exception as e:
                    print(f'Erro ao deletar {filename}: {e}')

        # Exibe mensagem de sucesso
        self.mostrar_dialogo_sucesso_delecao()

    def mostrar_dialogo_sucesso_delecao(self):
        # Inicializa `dialog_del` apenas se ele não existir
        if not hasattr(self, 'dialog_del') or not self.dialog_del:
            self.dialog_del = MDDialog(
                title="Deleção Concluída!",
                text="Todos os arquivos '.txt' e '.pdf' foram deletados com sucesso.",
                buttons=[MDRaisedButton(text="OK", on_release=self.fechar_dialogo_delecao)]
            )
        self.dialog_del.open()

    def fechar_dialogo_delecao(self, *args):
        self.dialog_del.dismiss()
        arquivos_de_inicializacao.arquivos_iniciais()
        # self.dados_enrol('logininicial')

MainApp().run()
