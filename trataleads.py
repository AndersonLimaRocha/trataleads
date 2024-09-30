import streamlit as st
import pandas as pd
import re
import unicodedata
import plotly.express as px
import io
from io import BytesIO

# Função para normalizar texto, removendo acentuação e pontuações
def normalizar_texto(texto):
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r'[^\w\s]', '', texto)  # Remove pontuações
    return texto.lower()

# Função para calcular idade com base na data de nascimento
def calcular_idade(data_nascimento):
    try:
        hoje = pd.Timestamp.now().normalize()
        nascimento = pd.to_datetime(data_nascimento, errors='coerce')
        idade = (hoje - nascimento).days // 365
        return idade
    except:
        return None

# Função para validar nome
def validar_nome(df, coluna_nome, palavras_ofensivas):
    def nome_invalido(nome):
        nome_normalizado = normalizar_texto(str(nome))
        return any(palavra in nome_normalizado for palavra in palavras_ofensivas)

    df['Nome Inválido'] = df[coluna_nome].apply(nome_invalido)

# Função para validar data de nascimento (maior de 18 anos)
def validar_data_nascimento(df, coluna_data):
    df['Idade'] = df[coluna_data].apply(calcular_idade)
    df['Data Nascimento Inválida'] = df['Idade'].apply(lambda x: True if x is None or x < 18 else False)

# Função para validar gênero
def validar_genero(df, coluna_genero):
    def genero_invalido(genero):
        genero = genero.lower()
        return genero not in ['masculino', 'feminino', 'homem', 'mulher']

    df['Gênero Inválido'] = df[coluna_genero].apply(genero_invalido)

# Função para validar telefone e identificar se é fixo ou celular
def validar_telefone(df, coluna_telefone):
    def telefone_invalido(telefone):
        telefone = re.sub(r'\D', '', telefone)  # Remove caracteres não numéricos
        return len(telefone) not in [10, 11]  # Tamanho típico de telefones no Brasil

    def tipo_telefone(telefone):
        telefone = re.sub(r'\D', '', telefone)
        if len(telefone) == 10 and telefone[2] in '2345':  # Telefones fixos
            return 'Fixo'
        elif len(telefone) == 11 and telefone[2] == '9':  # Telefones celulares
            return 'Celular'
        return 'Desconhecido'

    df['Telefone Inválido'] = df[coluna_telefone].apply(telefone_invalido)
    df['Tipo Telefone'] = df[coluna_telefone].apply(tipo_telefone)

# Função para validar CEP (apenas para CEP brasileiro)
def validar_cep(df, coluna_cep):
    def cep_invalido(cep):
        cep = re.sub(r'\D', '', cep)  # Remove caracteres não numéricos
        # Verifica se o CEP tem 8 dígitos e não é repetido
        return len(cep) != 8 or not re.match(r'^[0-9]{8}$', cep) or df[coluna_cep].duplicated().any()

    df['CEP Inválido'] = df[coluna_cep].apply(cep_invalido)

    # Adicionando uma coluna para indicar duplicatas
    df['CEP Duplicado'] = df.duplicated(coluna_cep, keep=False)

# Função para validar e-mail e convertê-lo para minúsculas
def validar_email(df, coluna_email):
    def email_invalido(email):
        # Expressão regular para verificar formato de e-mail válido
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return not re.match(padrao, email)

    df[coluna_email] = df[coluna_email].str.lower()  # Converter e-mails para minúsculas
    df['E-mail Inválido'] = df[coluna_email].apply(email_invalido)

# Função para padronizar estados (UF) em letras maiúsculas
def validar_estado(df, coluna_estado):
    df[coluna_estado] = df[coluna_estado].str.upper()  # Converter estados para maiúsculas

# Função para aplicar Initcap nos dados
def aplicar_initcap(df):
    df = df.applymap(lambda s: s.title() if isinstance(s, str) else s)
    return df

# Função para exibir o modal de erros
def exibir_modal_erro(mensagem):
    modal_html = f"""
    <div class="modal" style="display:block;">
        <div class="modal-content">
            <span class="close" onclick="document.querySelector('.modal').style.display='none';">&times;</span>
            <h4>Erro no formato do arquivo.</h4>
            <p>{mensagem}</p>
        </div>
    </div>
    """
    return modal_html

# Função para processar o arquivo e aplicar validações
def processar_arquivo(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, sep='\t', encoding='utf-8')
        else:
            return None, None, "Formato de arquivo não suportado. Envie um arquivo CSV, XLSX ou TXT."
    except pd.errors.EmptyDataError:
        return None, None, "Erro: O arquivo está vazio ou não contém colunas para serem processadas."
    except UnicodeDecodeError:
        return None, None, "<b>Erro</b>: O arquivo precisa dos campos obrigatórios de Nome, Data de Nascimento, Gênero, Telefone, E-mail, Logradouro, Número, Bairro, Cidade, Estado e CEP"
    except Exception as e:
        return None, None, f"Ocorreu um erro inesperado: {e}"

    # Higienização das colunas
    df.columns = df.columns.str.strip()  # Remove espaços em branco dos nomes das colunas

    # Lista de palavras ofensivas
    palavras_ofensivas = ['puta', 'putão', 'cuzão', 'cusão', 'veado', 'aaa', 'xxxx', 'bunda', 'viado', 'cusao',
                          'minhas bolas', 'cachorro', 'vaca']  # Adicione mais palavras conforme necessário

    # Mapeamento de colunas esperadas
    colunas = {
        'nome': ['Nome', 'nome', 'Nome Completo'],
        'data_nascimento': ['Data Nascimento', 'Nascimento', 'data_nascimento'],
        'genero': ['Genero', 'Gênero', 'genero', 'sexo'],
        'telefone': ['Telefone', 'Celular', 'telefone'],
        'cep': ['CEP', 'cep', 'Código Postal'],
        'email': ['E-mail', 'email', 'Email', 'E-Mail'],
        'estado': ['Estado', 'estado', 'UF'],  # Adicionando estados/UF
        'cidade': ['Cidade', 'cidade', 'Município'],
        'logradouro': ['Logradouro', 'logradouro'],
        'numero': ['Número', 'numero'],
        'bairro': ['Bairro', 'bairro']
    }

    colunas_encontradas = {}

    for chave, nomes_possiveis in colunas.items():
        colunas_encontradas[chave] = next((nome for nome in nomes_possiveis if nome in df.columns), None)

    # Aplicar validações apenas nas colunas que foram encontradas
    if colunas_encontradas['nome']:
        validar_nome(df, colunas_encontradas['nome'], palavras_ofensivas)
    if colunas_encontradas['data_nascimento']:
        validar_data_nascimento(df, colunas_encontradas['data_nascimento'])
    if colunas_encontradas['genero']:
        validar_genero(df, colunas_encontradas['genero'])
    if colunas_encontradas['telefone']:
        validar_telefone(df, colunas_encontradas['telefone'])
    if colunas_encontradas['cep']:
        validar_cep(df, colunas_encontradas['cep'])
    if colunas_encontradas['email']:
        validar_email(df, colunas_encontradas['email'])
    if colunas_encontradas['estado']:
        validar_estado(df, colunas_encontradas['estado'])

    # Aplicar Initcap nos dados
    df = aplicar_initcap(df)

    # Coletar inconsistências
    inconsistencias = {col: df[col].sum() for col in df.columns if col.endswith('Inválido')}

    return df, inconsistencias, None

# Função para download do arquivo
def gerar_download(df, formato):
    if formato == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    elif formato == 'xlsx':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()
    elif formato == 'txt':
        return df.to_csv(index=False, sep='\t').encode('utf-8')

# Função para exibir o modal de inconsistências
def exibir_modal(inconsistencias):
    modal_html = """
    <div class="modal" style="display:block;">
        <div class="modal-content">
            <span class="close" onclick="document.querySelector('.modal').style.display='none';">&times;</span>
            <h4>Inconsistências Encontradas</h4>
            <ul>
    """
    
    for col, count in inconsistencias.items():
        modal_html += f"<li>{col}: {count}</li>"

    modal_html += """
            </ul>
        </div>
    </div>
    """
    return modal_html

# Função principal do Streamlit
def main():
    st.title("Tratamento e higienização de Leads")

    # Uplaod do arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo CSV, XLSX ou TXT", type=['csv', 'xlsx', 'txt'])
    if uploaded_file is not None:
        df, inconsistencias, erro_mensagem = processar_arquivo(uploaded_file)

        if erro_mensagem:
            st.error("Erro no processamento. Favor verificar o que aconteceu")
            st.markdown(exibir_modal_erro(erro_mensagem), unsafe_allow_html=True)
        
        elif df is not None:
            st.success("Arquivo processado com sucesso!")
            # st.dataframe(df)
            st.write(df)

            st.divider()

            # Botão para abrir modal de inconsistências
            if st.button("Visualizar quantidades de Inconsistências"):
                st.session_state.modal_visible = True

            if st.session_state.get('modal_visible', False):
                st.markdown(exibir_modal(inconsistencias), unsafe_allow_html=True)

            st.divider()

            # Adicionando gráficos de distribuição            
            if 'Idade' in df.columns:
                fig_idade = px.histogram(df, x='Idade', title='Distribuição de Idade')
                st.plotly_chart(fig_idade)

            if 'Tipo Telefone' in df.columns:
                fig_telefone = px.pie(df, names='Tipo Telefone', title='Distribuição de Tipo de Telefone')
                st.plotly_chart(fig_telefone)

            if 'Gênero' in df.columns:
                fig_genero = px.histogram(df, x='Gênero', title='Distribuição de Gênero')
                st.plotly_chart(fig_genero)

            if 'Estado' in df.columns:
                fig_estado = px.histogram(df, x='Estado', title='Distribuição de Estados')
                st.plotly_chart(fig_estado)

            # Gráfico de inconsistências
            if inconsistencias:
                df_inconsistencias = pd.DataFrame(list(inconsistencias.items()), columns=['Tipo de Inconsistência', 'Contagem'])
                fig_inconsistencias = px.bar(df_inconsistencias, x='Tipo de Inconsistência', y='Contagem', title='Inconsistências Encontradas')
                st.plotly_chart(fig_inconsistencias)

            st.divider()

            # Opção para download dos dados processados

            formato = st.selectbox("Selecione o formato para download", ["csv", "xlsx", "txt"])
            if st.button("Download"):
                download = gerar_download(df, formato)
                st.download_button("Baixar Arquivo", download, file_name=f'dados_processados.{formato}', mime='text/csv')

if __name__ == "__main__":
    main()