
import streamlit as st
import sqlite3

# Função para conectar ao banco de dados
def conectar_db():
    conn = sqlite3.connect('consultor.db')
    return conn

# Função para criar a tabela
def criar_tabela():
    conn = conectar_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS respostas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    problema TEXT,
                    solucao TEXT,
                    falta TEXT
                )''')
    conn.commit()
    conn.close()

# Função para inserir respostas
def inserir_respostas(respostas):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('''INSERT INTO respostas (nome, problema, solucao, falta) VALUES (?, ?, ?, ?)''', 
              (respostas['nome'], respostas['problema'], respostas['solucao'], respostas.get('falta')))
    conn.commit()
    conn.close()

# Função para excluir respostas
def excluir_respostas(nome):
    conn = conectar_db()
    c = conn.cursor()
    c.execute('DELETE FROM respostas WHERE nome = ?', (nome,))
    conn.commit()
    conn.close()

# Cria a tabela ao iniciar o aplicativo
criar_tabela()

# Interface do Streamlit
st.title("Bem-vindo ao Consultor!")

# Solicitar o nome do usuário
nome = st.text_input("Digite o seu nome:")
if nome:
    st.session_state['nome'] = nome

# Solicitar o problema do usuário
problema = st.text_input(f"{nome}, qual é o seu maior problema hoje:")
if problema:
    st.session_state['problema'] = problema

# Solicitar solução proposta pelo usuário
solucao = st.text_input("O que pretende fazer para resolver?")
if solucao:
    st.session_state['solucao'] = solucao

# Perguntar se o usuário já deu início à solução
inicio = st.radio("Você já deu início a esta solução?", ("sim", "não"))
if inicio == 'não':
    falta = st.text_input("O que falta para você começar?")
    if falta:
        st.session_state['falta'] = falta
else:  # Se o usuário respondeu 'sim'
    solucao_encontrada = st.text_input("Qual solução você encontrou?")
    if solucao_encontrada:
        st.session_state['solucao_encontrada'] = solucao_encontrada
        st.success("Parabéns! Você encontrou uma solução.")

if st.button("Enviar Respostas"):
    if 'nome' in st.session_state and 'problema' in st.session_state and 'solucao' in st.session_state:
        respostas = {
            'nome': st.session_state['nome'],
            'problema': st.session_state['problema'],
            'solucao': st.session_state['solucao'],
            'falta': st.session_state.get('falta', None)
        }
        inserir_respostas(respostas)
        st.success("Obrigado por participar da nossa pesquisa.")

        # Exibir resumo das respostas
        st.subheader("Resumo das suas respostas:")
        for chave, valor in respostas.items():
            st.write(f"{chave.capitalize()}: {valor}")

if 'nome' not in st.session_state:
    st.write("Preencha suas informações para continuar.")

# Se o usuário quiser excluir as respostas
if st.button("Excluir Respostas"):
    senha = st.text_input("Digite a senha para confirmar a exclusão (senha: ***...)", type='password')
    if senha == '055...':
        if 'nome' in st.session_state:
            excluir_respostas(st.session_state['nome'])
            st.success("Suas respostas foram excluídas com sucesso.")
            # Limpar o estado da sessão
            st.session_state.clear()
        else:
            st.warning("Nome não encontrado. Preencha suas informações primeiro.")
    else:
        st.error("Senha incorreta.")