import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração básica da página
st.set_page_config(
    page_title="Sistema de Gestão Integrado",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do session_state
if 'carrinho' not in st.session_state:
    st.session_state['carrinho'] = []
if 'historico_notas' not in st.session_state:
    st.session_state['historico_notas'] = []

def calcular_desconto(total):
    """Calcula 10% de desconto se a compra for maior que R$ 50"""
    return total * 0.10 if total > 50 else 0.0

def exibir_inicio():
    st.title("🏢 Bem-vindo ao Sistema de Gestão Integrado")
    st.markdown("""
        Este sistema possui dois módulos principais:
        
        *   **🎓 Gestão Escolar:** Ferramenta para calcular médias, frequência e manter um histórico de desempenho dos alunos.
        *   **🍔 Gestão de Lanchonete:** Sistema completo de PDV (Ponto de Venda) com controle de carrinho, cardápio variado e cálculo automático de descontos.
        
        👈 **Utilize o menu lateral para navegar entre os módulos.**
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Dica:** No sistema de Lanchonete, compras acima de R$ 50,00 ganham 10% de desconto!")
    with col2:
        st.success("🎁 **Promoção:** Na compra de 2 ou mais lanches e 1 sobremesa, o cliente ganha um brinde surpresa!")

def exibir_calculadora_escolar():
    st.title("🎓 Calculadora de Desempenho Escolar")
    st.markdown("Calcule a média, verifique a aprovação e guarde o histórico do aluno.")
    
    with st.form("form_notas"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dados do Aluno")
            nome = st.text_input("Nome completo")
            disciplina = st.text_input("Disciplina")
            
        with col2:
            st.subheader("Notas e Frequência")
            c_nota1, c_nota2, c_nota3, c_nota4 = st.columns(4)
            n1 = c_nota1.number_input("1º Bim", min_value=0.0, max_value=10.0, step=0.1)
            n2 = c_nota2.number_input("2º Bim", min_value=0.0, max_value=10.0, step=0.1)
            n3 = c_nota3.number_input("3º Bim", min_value=0.0, max_value=10.0, step=0.1)
            n4 = c_nota4.number_input("4º Bim", min_value=0.0, max_value=10.0, step=0.1)
            
            c_faltas, c_aulas = st.columns(2)
            faltas = c_faltas.number_input("Total de Faltas", min_value=0, step=1)
            aulas = c_aulas.number_input("Total de Aulas no Ano", min_value=1, step=1, value=200)
            
        submit = st.form_submit_button("Calcular e Salvar", use_container_width=True)
        
    if submit:
        if not nome or not disciplina:
            st.warning("Por favor, preencha o nome do aluno e a disciplina.")
        else:
            media = (n1 + n2 + n3 + n4) / 4
            frequencia = ((aulas - faltas) / aulas) * 100
            
            situacao = "Aprovado" if media >= 6.0 and frequencia >= 75.0 else ("Recuperação" if frequencia >= 75.0 and media >= 4.0 else "Reprovado")
            
            st.session_state['historico_notas'].append({
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Aluno": nome,
                "Disciplina": disciplina,
                "Média": round(media, 2),
                "Frequência (%)": round(frequencia, 2),
                "Situação": situacao
            })
            
            st.success("Cálculo realizado e salvo com sucesso!")
            
            st.divider()
            st.subheader(f"📊 Resultado: {nome} - {disciplina}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Média Final", f"{media:.2f}", f"{media - 6.0:.2f} da média (6.0)")
            m2.metric("Frequência", f"{frequencia:.1f}%", f"{frequencia - 75.0:.1f}% do mínimo (75%)")
            
            if situacao == "Aprovado":
                m3.success("✨ APROVADO ✨")
            elif situacao == "Recuperação":
                m3.warning("⚠️ RECUPERAÇÃO ⚠️")
            else:
                m3.error("❌ REPROVADO ❌")

    if st.session_state['historico_notas']:
        st.divider()
        st.subheader("📋 Histórico de Consultas")
        df = pd.DataFrame(st.session_state['historico_notas'])
        
        # Estilizando o dataframe
        def color_situacao(val):
            color = 'green' if val == 'Aprovado' else ('orange' if val == 'Recuperação' else 'red')
            return f'color: {color}; font-weight: bold'
            
        st.dataframe(
            df.style.map(color_situacao, subset=['Situação']),
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("Limpar Histórico"):
            st.session_state['historico_notas'] = []
            st.rerun()

def exibir_sistema_lanchonete():
    st.title("🍔 Sistema PDV - Lanchonete")
    st.markdown("Gerencie pedidos, adicione itens ao carrinho e processe o pagamento.")
    
    # Dicionário de produtos
    cardapio = {
        "Lanches": {
            "X-Burger": 18.00,
            "X-Salada": 20.00,
            "X-Bacon": 22.00,
            "X-Tudo Mega": 28.00
        },
        "Bebidas": {
            "Refrigerante Lata": 7.00,
            "Suco Natural 500ml": 9.00,
            "Água Mineral": 4.00,
            "Cerveja Long Neck": 12.00
        },
        "Sobremesas": {
            "Pudim": 9.00,
            "Sorvete (2 bolas)": 12.00,
            "Brownie com Sorvete": 16.00,
            "Mousse de Maracujá": 8.00
        }
    }

    col_menu, col_cart = st.columns([3, 2])
    
    with col_menu:
        st.subheader("📖 Cardápio")
        
        tabs = st.tabs(list(cardapio.keys()))
        
        for i, (categoria, itens) in enumerate(cardapio.items()):
            with tabs[i]:
                for item, preco in itens.items():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.write(f"**{item}**")
                    c2.write(f"R$ {preco:.2f}")
                    if c3.button("Adicionar", key=f"add_{item}"):
                        st.session_state['carrinho'].append({"item": item, "preco": preco, "categoria": categoria})
                        st.toast(f"{item} adicionado ao carrinho!", icon="🛒")

    with col_cart:
        st.subheader("🛒 Carrinho atual")
        
        if not st.session_state['carrinho']:
            st.info("O carrinho está vazio. Adicione itens do cardápio.")
        else:
            # Agrupar itens no carrinho
            df_carrinho = pd.DataFrame(st.session_state['carrinho'])
            resumo = df_carrinho.groupby(['item', 'categoria']).agg(
                quantidade=('item', 'count'),
                preco_unitario=('preco', 'first')
            ).reset_index()
            
            resumo['subtotal'] = resumo['quantidade'] * resumo['preco_unitario']
            
            # Formatar para exibição
            resumo_view = resumo[['item', 'quantidade', 'preco_unitario', 'subtotal']].copy()
            resumo_view.columns = ['Item', 'Qtd', 'Unid (R$)', 'Total (R$)']
            st.dataframe(resumo_view, hide_index=True, use_container_width=True)
            
            total_bruto = resumo['subtotal'].sum()
            desconto = calcular_desconto(total_bruto)
            total_liquido = total_bruto - desconto
            
            # Lógica de brindes: 2 lanches e 1 sobremesa
            qtd_lanches = resumo[resumo['categoria'] == 'Lanches']['quantidade'].sum()
            qtd_sobremesas = resumo[resumo['categoria'] == 'Sobremesas']['quantidade'].sum()
            ganhou_brinde = (qtd_lanches >= 2 and qtd_sobremesas >= 1)
            
            st.divider()
            st.markdown(f"**Subtotal:** R$ {total_bruto:.2f}")
            if desconto > 0:
                st.markdown(f"**Desconto (10%):** <span style='color:green'>- R$ {desconto:.2f}</span>", unsafe_allow_html=True)
            
            st.markdown(f"### Total a Pagar: R$ {total_liquido:.2f}")
            
            if ganhou_brinde:
                st.success("🎁 Brinde Desbloqueado! O cliente ganhou uma batata frita pequena!")
                
            col_clear, col_checkout = st.columns(2)
            if col_clear.button("🗑️ Limpar Carrinho", use_container_width=True):
                st.session_state['carrinho'] = []
                st.rerun()
                
            if col_checkout.button("✅ Finalizar Pedido", type="primary", use_container_width=True):
                st.balloons()
                st.success(f"Pedido finalizado com sucesso! Valor pago: R$ {total_liquido:.2f}")
                st.session_state['carrinho'] = [] # Limpando após finalização
                # st.rerun() não é estritamente necessário se não quiser apagar o success instantaneamente

# Menu de navegação lateral
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942821.png", width=100)
    st.title("Navegação")
    
    opcao = st.radio(
        "Selecione o Módulo:",
        ["🏠 Início", "🎓 Cálculo de Média Escolar", "🍔 Sistema de Pedidos"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("Desenvolvido para demonstração de conceitos do Streamlit.")
    st.caption("Versão 2.0")

# Roteamento de páginas
if "Início" in opcao:
    exibir_inicio()
elif "Cálculo" in opcao:
    exibir_calculadora_escolar()
elif "Sistema" in opcao:
    exibir_sistema_lanchonete()