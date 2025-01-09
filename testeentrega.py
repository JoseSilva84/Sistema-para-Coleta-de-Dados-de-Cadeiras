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
