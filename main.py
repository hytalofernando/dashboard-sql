import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os
from database import init_db, get_db_session, DATABASE_URL, engine
from models import Equipment
from auth import authenticate_user
from sqlalchemy import text

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Estoque",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializa o banco de dados
init_db()

# Inicializa variáveis de sessão
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None


def login_page():
    """Página de login com design melhorado"""
    st.markdown("<h1 style='text-align: center;'>🔐 Login - Dashboard de Estoque</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Faça login para continuar")
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit_button = st.form_submit_button("🚀 Entrar", use_container_width=True)
            
            if submit_button:
                if username and password:
                    result = authenticate_user(username, password)
                    if result['success']:
                        st.session_state.authenticated = True
                        st.session_state.user = result['user']
                        st.success("✅ " + result['message'])
                        st.rerun()
                    else:
                        st.error("❌ " + result['message'])
                else:
                    st.warning("⚠️ Por favor, preencha todos os campos")


def dashboard_page():
    """Página principal com gráficos e estatísticas do estoque"""
    st.title("📊 Dashboard de Estoque")
    st.markdown("---")
    
    db = get_db_session()
    try:
        equipments = db.query(Equipment).all()
        
        if not equipments:
            st.info("📭 Nenhum equipamento cadastrado ainda. Adicione equipamentos para visualizar o dashboard.")
            return
        
        # Prepara dados para análise
        df = pd.DataFrame([{
            'Código': eq.codigo,
            'Nome': getattr(eq, 'nome', 'N/A'),
            'Tipo': eq.tipo,
            'Quantidade': eq.quantidade,
            'Data Adição': getattr(eq, 'data_adicao', None),
            'Última Atualização': getattr(eq, 'ultima_atualizacao', None)
        } for eq in equipments])
        
        # Estatísticas gerais no topo
        st.subheader("📈 Estatísticas Gerais")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_tipos = len(equipments)  # Total de linhas (código+tipo)
        total_quantidade = df['Quantidade'].sum()
        total_novo = df[df['Tipo'] == 'NOVO']['Quantidade'].sum()
        total_usado = df[df['Tipo'] == 'USADO']['Quantidade'].sum()
        codigos_unicos = df['Código'].nunique()
        
        with col1:
            st.metric("📦 Itens no Banco", total_tipos, help="Total de registros salvos")
        with col2:
            st.metric("🔢 Quantidade Total", int(total_quantidade), help="Soma de todas as quantidades")
        with col3:
            st.metric("✨ NOVO", int(total_novo), help="Total de equipamentos novos")
        with col4:
            st.metric("♻️ USADO", int(total_usado), help="Total de equipamentos usados")
        with col5:
            st.metric("🏷️ Códigos Únicos", codigos_unicos, help="Total de códigos diferentes")
        
        st.markdown("---")
        
        # Gráficos lado a lado
        col_grafico1, col_grafico2 = st.columns(2)
        
        with col_grafico1:
            st.subheader("📊 Estoque por Tipo")
            tipo_sum = df.groupby('Tipo')['Quantidade'].sum().reset_index()
            
            fig1 = px.pie(
                tipo_sum,
                values='Quantidade',
                names='Tipo',
                color='Tipo',
                color_discrete_map={'NOVO': '#2ecc71', 'USADO': '#e74c3c'},
                hole=0.4
            )
            fig1.update_traces(textposition='inside', textinfo='percent+label+value')
            fig1.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_grafico2:
            st.subheader("📈 Top 5 Equipamentos")
            top5 = df.nlargest(5, 'Quantidade')[['Nome', 'Quantidade', 'Tipo']]
            
            fig2 = px.bar(
                top5,
                x='Quantidade',
                y='Nome',
                color='Tipo',
                orientation='h',
                color_discrete_map={'NOVO': '#2ecc71', 'USADO': '#e74c3c'},
                text='Quantidade'
            )
            fig2.update_traces(texttemplate='%{text}', textposition='outside')
            fig2.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        # Lista completa de equipamentos
        st.subheader("📋 Lista Completa de Equipamentos")
        
        # Adiciona filtros
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        with col_filtro1:
            filtro_tipo = st.multiselect("Filtrar por Tipo", options=['NOVO', 'USADO'], default=['NOVO', 'USADO'])
        with col_filtro2:
            filtro_codigo = st.text_input("🔍 Buscar por Código", placeholder="Digite o código")
        with col_filtro3:
            filtro_nome = st.text_input("🔍 Buscar por Nome", placeholder="Digite o nome")
        
        # Aplica filtros
        df_filtrado = df.copy()
        if filtro_tipo:
            df_filtrado = df_filtrado[df_filtrado['Tipo'].isin(filtro_tipo)]
        if filtro_codigo:
            df_filtrado = df_filtrado[df_filtrado['Código'].str.contains(filtro_codigo.upper(), case=False, na=False)]
        if filtro_nome:
            df_filtrado = df_filtrado[df_filtrado['Nome'].str.contains(filtro_nome, case=False, na=False)]
        
        # Formata datas se existirem
        if 'Data Adição' in df_filtrado.columns:
            df_filtrado['Data Adição'] = pd.to_datetime(df_filtrado['Data Adição']).dt.strftime('%d/%m/%Y %H:%M')
        if 'Última Atualização' in df_filtrado.columns:
            df_filtrado['Última Atualização'] = pd.to_datetime(df_filtrado['Última Atualização']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Exibe tabela com estilo
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Código": st.column_config.TextColumn("Código", width="small"),
                "Nome": st.column_config.TextColumn("Nome", width="medium"),
                "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                "Quantidade": st.column_config.NumberColumn("Quantidade", width="small"),
                "Data Adição": st.column_config.TextColumn("Data Adição", width="medium"),
                "Última Atualização": st.column_config.TextColumn("Última Atualização", width="medium")
            }
        )
        
        st.info(f"📊 Mostrando **{len(df_filtrado)}** de **{len(df)}** equipamentos")
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
    finally:
        db.close()


def adicionar_equipamento_page():
    """Página para adicionar ou atualizar equipamentos com autocompletar"""
    st.title("➕ Adicionar / Atualizar Equipamento")
    st.markdown("---")
    
    if st.session_state.user['role'] != 'admin':
        st.warning("⚠️ Você não tem permissão para adicionar equipamentos. Apenas administradores podem realizar esta ação.")
        return
    
    # Inicializa variáveis de sessão
    if 'codigo_busca' not in st.session_state:
        st.session_state.codigo_busca = ""
    if 'equipamento_encontrado' not in st.session_state:
        st.session_state.equipamento_encontrado = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Informações do Equipamento")
        
        # Busca códigos existentes para o selectbox
        db = get_db_session()
        try:
            equipamentos_existentes = db.query(Equipment.codigo, Equipment.nome).distinct().all()
            codigos_existentes = [""] + [f"{eq.codigo} - {eq.nome}" for eq in equipamentos_existentes]
        except:
            codigos_existentes = [""]
        finally:
            db.close()
        
        # Opção de selecionar código existente
        st.markdown("**Opção 1: Selecione um código existente**")
        codigo_selecionado = st.selectbox(
            "📋 Códigos Cadastrados",
            codigos_existentes,
            help="Selecione um código já cadastrado ou digite um novo abaixo"
        )
        
        st.markdown("**Opção 2: Digite um código novo ou existente**")
        
        # Busca de código
        col_codigo, col_buscar = st.columns([3, 1])
        
        with col_codigo:
            codigo_input = st.text_input(
                "🏷️ Código do Equipamento *",
                value=st.session_state.codigo_busca,
                placeholder="Ex: EQ001",
                help="Digite o código e clique em Buscar",
                key="codigo_search"
            )
        
        with col_buscar:
            st.write("")  # Espaçamento
            st.write("")  # Espaçamento
            buscar_button = st.button("🔍 Buscar", use_container_width=True, type="secondary")
        
        # Se selecionou da lista, usa esse código
        if codigo_selecionado and not codigo_input:
            codigo_da_lista = codigo_selecionado.split(" - ")[0]
            codigo_input = codigo_da_lista
            st.session_state.codigo_busca = codigo_da_lista
            buscar_button = True  # Força busca
        
        # Busca quando botão é clicado ou código muda
        realizar_busca = False
        
        if buscar_button:
            realizar_busca = True
            st.session_state.codigo_busca = codigo_input.upper() if codigo_input else ""
        
        # Também busca se o código mudou e não está vazio
        if codigo_input and codigo_input.upper() != st.session_state.codigo_busca and not buscar_button:
            realizar_busca = True
            st.session_state.codigo_busca = codigo_input.upper()
        
        # Executa busca
        if realizar_busca and st.session_state.codigo_busca:
            db = get_db_session()
            try:
                # Busca qualquer equipamento com este código
                equipamento = db.query(Equipment).filter(
                    Equipment.codigo == st.session_state.codigo_busca
                ).first()
                
                if equipamento:
                    st.session_state.equipamento_encontrado = {
                        'codigo': equipamento.codigo,
                        'nome': equipamento.nome
                    }
                else:
                    st.session_state.equipamento_encontrado = None
            except Exception as e:
                st.error(f"Erro ao buscar: {str(e)}")
                st.session_state.equipamento_encontrado = None
            finally:
                db.close()
        
        # Limpa busca se código foi apagado
        if not codigo_input:
            st.session_state.equipamento_encontrado = None
            st.session_state.codigo_busca = ""
        
        # Mostra informações do equipamento encontrado
        if st.session_state.equipamento_encontrado:
            st.success(f"✅ **Código encontrado no banco!** Nome: **{st.session_state.equipamento_encontrado['nome']}**")
            nome_readonly = st.session_state.equipamento_encontrado['nome']
            nome_disabled = True
            placeholder_nome = st.session_state.equipamento_encontrado['nome']
        else:
            if codigo_input:
                st.info("ℹ️ Código novo - preencha o nome do equipamento abaixo")
            nome_readonly = ""
            nome_disabled = False
            placeholder_nome = "Ex: Notebook Dell Inspiron"
        
        # Formulário
        with st.form("adicionar_equipamento_form", clear_on_submit=False):
            # Campo nome (readonly se equipamento encontrado)
            if nome_disabled:
                st.text_input(
                    "📦 Nome do Equipamento",
                    value=nome_readonly,
                    disabled=True,
                    help="Nome preenchido automaticamente (equipamento já cadastrado)"
                )
                nome = nome_readonly
            else:
                nome = st.text_input(
                    "📦 Nome do Equipamento *",
                    placeholder=placeholder_nome,
                    help="Nome descritivo do equipamento"
                )
            
            # Tipo e Quantidade sempre editáveis
            tipo = st.selectbox(
                "🔖 Tipo *",
                ["NOVO", "USADO"],
                help="Selecione se o equipamento é novo ou usado"
            )
            
            quantidade = st.number_input(
                "🔢 Quantidade a Adicionar *",
                min_value=1,
                value=1,
                step=1,
                help="Quantidade que será adicionada ao estoque"
            )
            
            st.markdown("---")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit_button = st.form_submit_button(
                    "✅ Adicionar / Atualizar",
                    use_container_width=True,
                    type="primary"
                )
            with col_btn2:
                limpar_button = st.form_submit_button(
                    "🔄 Limpar Campos",
                    use_container_width=True
                )
            
            if limpar_button:
                st.session_state.codigo_busca = ""
                st.session_state.equipamento_encontrado = None
                st.rerun()
            
            if submit_button:
                codigo = st.session_state.codigo_busca
                
                if not codigo:
                    st.error("❌ Por favor, preencha o código do equipamento")
                elif not nome:
                    st.error("❌ Por favor, preencha o nome do equipamento")
                else:
                    db = get_db_session()
                    try:
                        # Verifica se já existe equipamento com o mesmo código e tipo
                        existing = db.query(Equipment).filter(
                            Equipment.codigo == codigo.upper(),
                            Equipment.tipo == tipo
                        ).first()
                        
                        if existing:
                            # Atualiza a quantidade do equipamento existente
                            quantidade_anterior = existing.quantidade
                            existing.quantidade += quantidade
                            existing.ultima_atualizacao = datetime.now()
                            db.commit()
                            
                            st.success(f"""
                            ✅ **Quantidade atualizada com sucesso!**
                            
                            📦 **Equipamento:** {existing.nome}  
                            🏷️ **Código:** {codigo.upper()}  
                            🔖 **Tipo:** {tipo}  
                            📊 **Quantidade anterior:** {quantidade_anterior}  
                            ➕ **Quantidade adicionada:** {quantidade}  
                            🔢 **Quantidade atual:** {existing.quantidade}  
                            🕐 **Atualizado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
                            """)
                            st.balloons()
                            
                            # Limpa campos após sucesso
                            st.session_state.codigo_busca = ""
                            st.session_state.equipamento_encontrado = None
                        else:
                            # Cria novo equipamento
                            novo_equipamento = Equipment(
                                codigo=codigo.upper(),
                                nome=nome,
                                tipo=tipo,
                                quantidade=quantidade,
                                data_adicao=datetime.now(),
                                ultima_atualizacao=datetime.now()
                            )
                            db.add(novo_equipamento)
                            db.commit()
                            
                            st.success(f"""
                            ✅ **Equipamento adicionado com sucesso!**
                            
                            📦 **Nome:** {nome}  
                            🏷️ **Código:** {codigo.upper()}  
                            🔖 **Tipo:** {tipo}  
                            🔢 **Quantidade:** {quantidade}  
                            🕐 **Adicionado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
                            """)
                            st.balloons()
                            
                            # Limpa campos após sucesso
                            st.session_state.codigo_busca = ""
                            st.session_state.equipamento_encontrado = None
                    except Exception as e:
                        db.rollback()
                        st.error(f"❌ Erro ao adicionar/atualizar equipamento: {str(e)}")
                    finally:
                        db.close()
    
    with col2:
        st.info("""
        ### ℹ️ Como usar?
        
        **📋 Opção 1: Selecionar da Lista**
        - Escolha um código já cadastrado
        - Nome preenche automaticamente
        - Escolha tipo e quantidade
        
        **⌨️ Opção 2: Digitar Código**
        - Digite o código
        - Clique em "🔍 Buscar"
        - Se existir, nome preenche automaticamente
        - Se não existir, preencha o nome
        
        **✨ Código Novo:**
        - Digite um código novo
        - Preencha o nome manualmente
        - Escolha tipo e quantidade
        - Clique em "Adicionar"
        
        **📦 Código Existente:**
        - Nome bloqueado (automático)
        - Escolha NOVO ou USADO
        - Defina quantidade a adicionar
        - Sistema soma ao estoque existente
        
        **💡 Dica:**
        - Use a lista para facilitar
        - Ou digite se souber o código
        """)


def remover_equipamento_page():
    """Página para remover equipamentos por quantidade"""
    st.title("➖ Remover Equipamento")
    st.markdown("---")
    
    if st.session_state.user['role'] != 'admin':
        st.warning("⚠️ Você não tem permissão para remover equipamentos. Apenas administradores podem realizar esta ação.")
        return
    
    db = get_db_session()
    try:
        equipments = db.query(Equipment).all()
        
        if not equipments:
            st.info("📭 Nenhum equipamento cadastrado para remover.")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Cria lista de opções para o selectbox
            opcoes = [f"{eq.codigo} - {getattr(eq, 'nome', 'N/A')} - {eq.tipo} (Qtd: {eq.quantidade})" for eq in equipments]
            
            with st.form("remover_equipamento_form"):
                st.subheader("🗑️ Selecione o equipamento")
                
                selected = st.selectbox("📦 Equipamento *", opcoes, help="Escolha o equipamento que deseja remover")
                
                # Extrai informações do equipamento selecionado
                codigo_selecionado = selected.split(" - ")[0]
                tipo_selecionado = selected.split(" - ")[2].split(" (")[0]
                
                equipment = db.query(Equipment).filter(
                    Equipment.codigo == codigo_selecionado,
                    Equipment.tipo == tipo_selecionado
                ).first()
                
                if equipment:
                    quantidade_disponivel = equipment.quantidade
                    
                    st.info(f"📊 **Quantidade disponível:** {quantidade_disponivel}")
                    
                    quantidade_remover = st.number_input(
                        "🔢 Quantidade a remover *",
                        min_value=1,
                        max_value=quantidade_disponivel,
                        value=min(1, quantidade_disponivel),
                        step=1,
                        help=f"Você pode remover de 1 até {quantidade_disponivel} unidades"
                    )
                    
                    remover_tudo = st.checkbox("🗑️ Remover equipamento completamente do sistema", help="Marca esta opção para deletar o equipamento independente da quantidade")
                    
                    st.markdown("---")
                    submit_button = st.form_submit_button("🗑️ Confirmar Remoção", type="primary", use_container_width=True)
                    
                    if submit_button:
                        try:
                            if remover_tudo or quantidade_remover >= quantidade_disponivel:
                                # Remove o equipamento completamente
                                db.delete(equipment)
                                db.commit()
                                st.success(f"""
                                ✅ **Equipamento removido completamente!**
                                
                                📦 **Nome:** {equipment.nome}  
                                🏷️ **Código:** {equipment.codigo}  
                                🔖 **Tipo:** {equipment.tipo}  
                                🔢 **Quantidade removida:** {equipment.quantidade}  
                                🕐 **Removido em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
                                """)
                                st.rerun()
                            else:
                                # Remove apenas a quantidade especificada
                                quantidade_anterior = equipment.quantidade
                                equipment.quantidade -= quantidade_remover
                                equipment.ultima_atualizacao = datetime.now()
                                db.commit()
                                st.success(f"""
                                ✅ **Quantidade reduzida com sucesso!**
                                
                                📦 **Equipamento:** {equipment.nome}  
                                🏷️ **Código:** {equipment.codigo}  
                                🔖 **Tipo:** {equipment.tipo}  
                                📊 **Quantidade anterior:** {quantidade_anterior}  
                                ➖ **Quantidade removida:** {quantidade_remover}  
                                🔢 **Quantidade restante:** {equipment.quantidade}  
                                🕐 **Atualizado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
                                """)
                                st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"❌ Erro ao remover equipamento: {str(e)}")
        
        with col2:
            st.info("""
            ### ℹ️ Como funciona?
            
            **Remoção parcial:**
            - Remove apenas a quantidade especificada
            - O equipamento permanece no sistema
            
            **Remoção total:**
            - Marca "Remover completamente"
            - OU remove a quantidade total disponível
            - Deleta o equipamento do sistema
            
            **Dica:**
            - Use remoção parcial para saídas graduais
            - Use remoção total quando não usar mais o item
            """)
            
    except Exception as e:
        st.error(f"❌ Erro ao processar remoção: {str(e)}")
    finally:
        db.close()


def main():
    """Função principal da aplicação"""
    
    # Se não estiver autenticado, mostra página de login
    if not st.session_state.authenticated:
        login_page()
    else:
        # Menu lateral com design melhorado
        with st.sidebar:
            st.markdown(f"""
            ### 👤 {st.session_state.user['username']}
            **Perfil:** {st.session_state.user['role'].upper()}
            """)
            
            st.markdown("---")
            
            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 🧭 Navegação")
            
            # Navegação
            pages = {
                "📊 Dashboard": dashboard_page,
                "➕ Adicionar Equipamento": adicionar_equipamento_page,
                "➖ Remover Equipamento": remover_equipamento_page
            }
            
            # Se for usuário comum, remove opções de admin
            if st.session_state.user['role'] == 'usuario':
                pages = {
                    "📊 Dashboard": dashboard_page
                }
            
            selected_page = st.radio(
                "Navegação",
                list(pages.keys()),
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #666; font-size: 12px;'>
            📦 Sistema de Estoque v2.0<br>
            Desenvolvido com Streamlit
            </div>
            """, unsafe_allow_html=True)
        
        # Renderiza a página selecionada
        pages[selected_page]()


if __name__ == "__main__":
    main()
