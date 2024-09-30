# Tratamento e Higienização de Leads

Este repositório contém um script em Python que utiliza a biblioteca Streamlit para criar uma aplicação que realiza o tratamento e a higienização de dados de leads. A aplicação permite o upload de arquivos em formato CSV, XLSX ou TXT, valida os dados contidos neles e exibe gráficos de distribuição das informações. Além disso, o script fornece uma interface para download dos dados processados.

## Dependências

- **Streamlit**: Para a criação da interface do usuário.
- **Pandas**: Para manipulação e análise de dados.
- **re**: Para expressões regulares.
- **unicodedata**: Para normalização de texto.
- **plotly.express**: Para a visualização gráfica de dados.

## Funções

### 1. `normalizar_texto(texto)`

Normaliza o texto removendo acentuação e pontuações.

**Parâmetros:**
- `texto` (str): O texto a ser normalizado.

**Retorno:**
- (str): O texto normalizado em letras minúsculas.

---

### 2. `calcular_idade(data_nascimento)`

Calcula a idade com base na data de nascimento fornecida.

**Parâmetros:**
- `data_nascimento` (str): A data de nascimento no formato aceito.

**Retorno:**
- (int ou None): A idade em anos ou `None` se a data for inválida.

---

### 3. `validar_nome(df, coluna_nome, palavras_ofensivas)`

Valida se os nomes na coluna especificada contêm palavras ofensivas.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_nome` (str): O nome da coluna que contém os nomes.
- `palavras_ofensivas` (list): Lista de palavras que são consideradas ofensivas.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 4. `validar_data_nascimento(df, coluna_data)`

Valida se as datas de nascimento são válidas e se a idade é maior ou igual a 18 anos.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_data` (str): O nome da coluna que contém as datas de nascimento.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 5. `validar_genero(df, coluna_genero)`

Valida se os gêneros na coluna especificada são válidos.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_genero` (str): O nome da coluna que contém os gêneros.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 6. `validar_telefone(df, coluna_telefone)`

Valida os números de telefone e identifica se são fixos ou celulares.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_telefone` (str): O nome da coluna que contém os números de telefone.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 7. `validar_cep(df, coluna_cep)`

Valida os CEPs brasileiros, verificando se estão no formato correto e se não são duplicados.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_cep` (str): O nome da coluna que contém os CEPs.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 8. `validar_email(df, coluna_email)`

Valida os e-mails e os converte para letras minúsculas.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_email` (str): O nome da coluna que contém os e-mails.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 9. `validar_estado(df, coluna_estado)`

Padroniza os estados (UF) convertendo para letras maiúsculas.

**Parâmetros:**
- `df` (DataFrame): O DataFrame contendo os dados a serem validados.
- `coluna_estado` (str): O nome da coluna que contém os estados.

**Retorno:**
- None (modifica o DataFrame diretamente).

---

### 10. `aplicar_initcap(df)`

Aplica o formato Initcap (primeira letra de cada palavra em maiúscula) nos dados do DataFrame.

**Parâmetros:**
- `df` (DataFrame): O DataFrame a ser modificado.

**Retorno:**
- (DataFrame): O DataFrame com as alterações aplicadas.

---

### 11. `exibir_modal_erro(mensagem)`

Exibe um modal com a mensagem de erro fornecida.

**Parâmetros:**
- `mensagem` (str): A mensagem a ser exibida no modal.

**Retorno:**
- (str): O HTML do modal a ser exibido.

---

### 12. `processar_arquivo(uploaded_file)`

Processa o arquivo enviado pelo usuário, aplicando as validações necessárias.

**Parâmetros:**
- `uploaded_file` (file): O arquivo carregado pelo usuário.

**Retorno:**
- (DataFrame, dict, str): O DataFrame processado, um dicionário de inconsistências e uma mensagem de erro, se houver.

---

### 13. `gerar_download(df, formato)`

Gera um arquivo para download no formato especificado.

**Parâmetros:**
- `df` (DataFrame): O DataFrame a ser convertido.
- `formato` (str): O formato para download (`csv`, `xlsx`, ou `txt`).

**Retorno:**
- (bytes): O conteúdo do arquivo gerado para download.

---

### 14. `exibir_modal(inconsistencias)`

Exibe um modal com a contagem de inconsistências encontradas.

**Parâmetros:**
- `inconsistencias` (dict): Um dicionário contendo tipos de inconsistências e suas contagens.

**Retorno:**
- (str): O HTML do modal a ser exibido.

---

### 15. `main()`

Função principal que inicializa a aplicação Streamlit.

**Parâmetros:**
- Nenhum.

**Retorno:**
- Nenhum (executa a aplicação Streamlit).

---

## Como Usar

1. Instale as dependências necessárias.
2. Execute o script em um ambiente que suporte Streamlit.
3. Acesse a aplicação em um navegador através do link gerado.
4. Faça o upload de um arquivo nos formatos suportados (CSV, XLSX ou TXT).
5. Acompanhe as validações realizadas e visualize os gráficos gerados.
6. Baixe os dados processados no formato desejado.

## Considerações Finais

Este script é uma ferramenta útil para a higienização de dados de leads, permitindo validar e padronizar informações essenciais antes do uso em análises ou campanhas. Adapte as listas de palavras ofensivas e outras validações conforme necessário para atender às suas necessidades específicas.