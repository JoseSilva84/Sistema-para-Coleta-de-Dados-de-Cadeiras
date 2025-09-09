# 🪑 Sistema para Coleta de Dados de Cadeiras  

📊 Um software desenvolvido em **Python** para auxiliar a empresa **Art & Fibras Cadeiras** na coleta, organização e análise de dados relacionados à produção de cadeiras.  
Combinando a praticidade do **KivyMD** para a interface gráfica e a robustez do **pandas** para manipulação de dados, o sistema torna o processo mais rápido, confiável e intuitivo.  

---

## ✨ Funcionalidades

- ✅ Interface gráfica moderna baseada em **Material Design**  
- 📂 Importação e leitura de arquivos `.txt` com dados da produção  
- 📊 Processamento e análise de dados com **pandas**  
- 📑 Geração de relatórios organizados  
- 💾 Sistema de **backup automático** dos arquivos  
- 🔍 Pesquisa e consulta rápida por **enrolador**, **tipo de cadeira** e **valores**  
- 📈 Contagem e somatória de produção  

---

## 🖼️ Prévia da Interface  

![Tela 01](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/01.png)  
![Tela 02](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/02.png)  
![Tela 03](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/03.png)  
![Tela 04](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/04.png)  
![Tela 05](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/05.png)  
![Tela 06](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/06.png)  
![Tela 07](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/07.png)  
![Tela 08](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/08.png)  
![Tela 09](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/09.png)  
![Tela 10](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/10.png)  
![Tela 11](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/11.png)  
![Tela 12](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/12.png)  
![Tela 13](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/13.png)  
![Tela 14](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/14.png)  
![Tela 15](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/15.png)  
![Tela 16](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/16.png)  
![Tela 17](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/17.png)  
![Tela 18](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/18.png)  
![Tela 19](https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/19.png)  

---

## 🛠️ Tecnologias Utilizadas  

- **Python 3.10+**  
- [pandas](https://pandas.pydata.org/) → análise e manipulação de dados  
- [KivyMD](https://kivymd.readthedocs.io/) → interface gráfica moderna  
- [Matplotlib](https://matplotlib.org/) *(opcional, caso use para gráficos)*  

---

## 📂 Estrutura do Projeto  

```text
📦 Sistema-para-Coleta-de-Dados-de-Cadeiras
├── assets/              # Recursos visuais (imagens, ícones, etc.)
├── backup_destino/      # Backups automáticos gerados pelo sistema
├── dados/               # Arquivos de entrada (txt, csv, etc.)
│   ├── ENROLADOR_JOAO.txt
│   ├── ENROLADOR_MARIA.txt
│   └── ...
├── main.py              # Ponto de entrada da aplicação
├── requirements.txt     # Lista de dependências
└── README.md            # Este arquivo
