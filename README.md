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

(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/01.png)  
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/02.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/03.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/04.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/05.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/06.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/07.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/08.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/09.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/10.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/11.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/12.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/13.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/14.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/15.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/16.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/17.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/18.png)
(https://github.com/JoseSilva84/Sistema-para-Coleta-de-Dados-de-Cadeiras/blob/main/img/19.png)
---

## 🛠️ Tecnologias Utilizadas  

- **Python 3.10+**  
- [pandas](https://pandas.pydata.org/) → análise e manipulação de dados  
- [KivyMD](https://kivymd.readthedocs.io/) → interface gráfica moderna  
- [Matplotlib](https://matplotlib.org/) *(opcional, caso use para gráficos)*  

---

## 📂 Estrutura do Projeto  

📦 Sistema-para-Coleta-de-Dados-de-Cadeiras
├── assets/ # Recursos visuais (imagens, ícones, etc.)
├── backup_destino/ # Backups automáticos gerados pelo sistema
├── dados/ # Arquivos de entrada (txt, csv, etc.)
│ ├── ENROLADOR_JOAO.txt
│ ├── ENROLADOR_MARIA.txt
│ └── ...
├── main.py # Ponto de entrada da aplicação
├── requirements.txt # Lista de dependências
└── README.md # Este arquivo

📦 Backup Automático

Todos os arquivos .txt manipulados pelo sistema são automaticamente copiados para a pasta:
backup_destino/
   ├── backup_20240930_101200/
   │   ├── ENROLADOR_JOAO.txt
   │   └── ENROLADOR_MARIA.txt

👨‍💻 Autor
Desenvolvido por José Silva Filho
