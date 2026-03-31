import streamlit as st

# Configuração básica da página
st.set_page_config(page_title="Sistema de Gestão", layout="wide")

# Menu de navegação lateral para substituir a 'opcao'
st.sidebar.title("Navegação")
opcao = st.sidebar.selectbox(
    "Escolha uma funcionalidade:",
    ["Início", "Cálculo de Média Escolar", "Sistema de Pedidos"]
)

# --- Opção 0: Início ---
if opcao == "Início":
    st.title("Bem-vindo ao Sistema")
    st.write("Selecione uma opção no menu lateral para começar.")

# --- Opção 1: Cálculo de Média Escolar ---
elif opcao == "Cálculo de Média Escolar":
    st.title("📊 Calculadora de Desempenho Escolar")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do aluno")
            nota1 = st.number_input("Nota 1", min_value=0.0, max_value=10.0, step=0.1)
            nota2 = st.number_input("Nota 2", min_value=0.0, max_value=10.0, step=0.1)
            
        with col2:
            num_falta = st.number_input("Número de faltas", min_value=0, step=1)
            num_aulas = st.number_input("Total de aulas", min_value=1, step=1, value=100)

    if st.button("Calcular Resultado"):
        media = (nota1 + nota2) / 2
        freq = (1 - (num_falta / num_aulas)) * 100
        
        st.divider()
        
        # Colunas para exibir métricas
        m1, m2, m3 = st.columns(3)
        m1.metric("Média Final", f"{media:.2f}")
        m2.metric("Frequência", f"{freq:.2f}%")
        
        if (media >= 6) and (freq >= 75):
            m3.success("Aprovado")
            st.balloons()
        else:
            m3.error("Reprovado")
            
        st.info(f"Aluno: {nome}")

# --- Opção 2: Sistema de Pedidos ---
elif opcao == "Sistema de Pedidos":
    st.title("🍔 Sistema de Lanchonete")
    
    nome_cliente = st.text_input("Nome do Cliente")
    
    c1, c2, c3 = st.columns(3)
    lanche = c1.number_input("Quantidade de Lanches (R$ 18,00)", min_value=0, step=1)
    refri = c2.number_input("Quantidade de Refris (R$ 7,00)", min_value=0, step=1)
    sobre = c3.number_input("Quantidade de Sobremesas (R$ 9,00)", min_value=0, step=1)

    if st.button("Finalizar Pedido"):
        conta = (lanche * 18) + (refri * 7) + (sobre * 9)
        valordesc = 0.0

        if conta > 50:
            valordesc = conta * 0.10

        valortotal = conta - valordesc
        ganhou_brinde = (lanche >= 2) and (sobre >= 1)

        st.divider()
        
        st.subheader(f"Resumo do Pedido: {nome_cliente}")
        
        # Exibição financeira
        res1, res2, res3 = st.columns(3)
        res1.write(f"**Subtotal:** R$ {conta:.2f}")
        res2.write(f"**Desconto (10%):** R$ {valordesc:.2f}")
        res3.subheader(f"Total: R$ {valortotal:.2f}")

        if ganhou_brinde:
            st.success("🎁 Parabéns! Você ganhou um brinde especial!")
        else:
            st.warning("Não há brindes para este pedido.")