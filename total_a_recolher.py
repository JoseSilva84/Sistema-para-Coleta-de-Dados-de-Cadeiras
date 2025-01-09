from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
import pandas as pd
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.properties import BooleanProperty
import convertertxt_em_pdf


class DadosFaltaEntregar(Screen):
    
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
        self.dados_enrol_scroll_texten2 = f"1. Quantidade total de Veneza a entregar: {qtde_ven7} unidades/{qtde_jogoven7} jogos\n2. Quantidade total de Banqueta a entregar: {qtde_ban7} unidades\n3. Quantidade total de Letícia a entregar: {qtde_let7} unidades/{jogolet7} jogos\n4. Quantidade total de Balanço a entregar: {qtde_bal7} unidades\n5. Quantidade total de Centro Comum a entregar: {qtde_ccomum7} unidades\n6. Quantidade total de Centro Letícia a entregar: {qtde_clet7} unidades\n7. Quantidade total de Centro Luxo a entregar: {qtde_cluxo7} unidades"
