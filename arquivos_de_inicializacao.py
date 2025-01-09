import os

def arquivos_iniciais():
    lista_enroladores = "LISTA ENROLADORES.txt"
    def criar_arquivo_txt():
        with open(lista_enroladores, "w", encoding="utf-8") as arquivo:
            arquivo.write("[00/00/0000] [Nenhum] [Nenhum] [0] [0.00] [0.00]")
        return arquivo
    
    def criar_arquivo_txt2():
        with open("LISTA VALE TOTAL.txt", "w", encoding="utf-8") as arquivo2:
            arquivo2.write("[00/00/0000] [Nenhum] [Nenhum] [0.00]")
        return arquivo2
    
    def criar_arquivo_txt3():
        with open("LISTA SOLDADORES.txt", "w", encoding="utf-8") as arquivo2:
            arquivo2.write("[00/00/0000] [Nenhum] [Nenhum] [0] [0.00] [0.00]")
        return arquivo2
    
    def criar_arquivo_txt4():
        with open("LISTA ENTREGA OBJETOS.txt", "w", encoding="utf-8") as arquivo2:
            arquivo2.write("[00/00/0000] [Nenhum] [Nenhum] [0]")
        return arquivo2

    def localizar(pasta, arquivo):
        for root, dirs,  files in os.walk(pasta):
            if arquivo in files:
                caminho = os.path.join(root, arquivo)
                if not os.path.exists("LISTA ENROLADORES.txt"):
                    print("O arquivo LISTA ENROLADORES.txt não existe, mas foi  criado!")
                    criar_arquivo_txt()
                else:
                    print("O arquivo LISTA ENROLADORES.txt já existe!")
                return caminho
        return
    
    def localizar2(pasta, arquivo):
        for root, dirs,  files in os.walk(pasta):
            if arquivo in files:
                caminho = os.path.join(root, arquivo)
                if not os.path.exists("LISTA VALE TOTAL.txt"):
                    print("O arquivo LISTA VALE TOTAL.txt não existe, mas foi  criado!")
                    criar_arquivo_txt2()
                else:
                    print("O arquivo LISTA VALE TOTAL.txt já existe!")
                return caminho
        return
    
    def localizar3(pasta, arquivo):
        for root, dirs,  files in os.walk(pasta):
            if arquivo in files:
                caminho = os.path.join(root, arquivo)
                if not os.path.exists("LISTA SOLDADORES.txt"):
                    print("O arquivo LISTA SOLDADORES.txt não existe, mas foi  criado!")
                    criar_arquivo_txt3()
                else:
                    print("O arquivo LISTA SOLDADORES.txt já existe!")
                return caminho
        return
    
    def localizar4(pasta, arquivo):
        for root, dirs,  files in os.walk(pasta):
            if arquivo in files:
                caminho = os.path.join(root, arquivo)
                if not os.path.exists("LISTA ENTREGA OBJETOS.txt"):
                    print("O arquivo LISTA ENTREGA OBJETOS.txt não existe, mas foi  criado!")
                    criar_arquivo_txt4()
                else:
                    print("O arquivo LISTA ENTREGA OBJETOS.txt já existe!")
                return caminho
        return

    caminho_pasta = r"C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA"
    arquivo_da_pasta = "LISTA ENROLADORES.txt"
    enroladores_arquivo =localizar(caminho_pasta, arquivo_da_pasta)
    
    caminho_pasta2 = r"C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA"
    arquivo_da_pasta2 = "LISTA VALE TOTAL.txt"
    enroladores_arquivo2 =localizar2(caminho_pasta2, arquivo_da_pasta2)
    
    caminho_pasta3 = r"C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA"
    arquivo_da_pasta3 = "LISTA SOLDADORES.txt"
    enroladores_arquivo3 =localizar3(caminho_pasta3, arquivo_da_pasta3)
    
    caminho_pasta4 = r"C:\Users\curso\Downloads\ESTUDOS SOBRE PROGRAMAÇÃO\SISTEMA"
    arquivo_da_pasta4 = "LISTA ENTREGA OBJETOS.txt"
    enroladores_arquivo4 =localizar4(caminho_pasta4, arquivo_da_pasta4)

    if enroladores_arquivo:
        print("Arquivo localizado!")
    else:
        print("Arquivo não encontrado!")
    return

arquivos_iniciais()