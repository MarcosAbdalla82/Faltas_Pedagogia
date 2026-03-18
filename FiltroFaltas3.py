import pandas as pd
import streamlit as st

# Le o arquivo csv
st.title('Sistema de verificação de faltas')
arq = st.file_uploader("Selecione o arquivo")
if arq is not None:
    df = pd.read_csv(arq,sep=';',encoding="latin1")
    #st.write(df.head())
else:
    arq = None
    df = pd.DataFrame()

cols = df.columns
colunas = []
for col in cols:
    colunas.append(col)

if arq is not None:
    turmas = df['COD_TURMA'].unique()
    turmasSAT = df[df["COD_TURMA"].str.contains("13390", na=False)]
    Alunos = turmasSAT[["ALUNO","DATA","COD_TURMA"]]

    Alunos["DATA"] = pd.to_datetime(Alunos["DATA"], dayfirst=True)
    Alunos["DATA"] = Alunos["DATA"].dt.date

    Dias = Alunos["DATA"].unique()

    Inicio = Dias[0]
    Fim = Dias[-1]
    Dt = Fim - Inicio
    dT = Dt.days # Numero de dias
    
    if dT<=5: 

        Filt = Alunos[Alunos["DATA"].between(Inicio,Fim)]
        Turmas = Alunos["COD_TURMA"].unique()

        T = st.selectbox('Turma', options=Turmas)

        filtroT = Filt[Filt['COD_TURMA']==T]

        Agrupado = (
            filtroT.groupby(["ALUNO", "COD_TURMA", "DATA"])
            .size()
            .reset_index(name="FALTAS/AULA")
        )
        st.subheader('Alunos faltoso na semana')
        st.write(Agrupado)

        resumo = (
        Agrupado.groupby(["ALUNO", "COD_TURMA"])["FALTAS/AULA"]
        .sum()
        .reset_index()
        )

        st.subheader('Alunos com mais de 8 faltas')
        resumo = resumo[resumo["FALTAS/AULA"] >= 8]   
        st.write(resumo) 
    else:
        st.warning("O período do arquivo é maior do que 1 semana",icon="⚠️")

