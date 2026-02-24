import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime, timedelta

st.markdown("""
<style>
/* Esconde header superior */
header {visibility: hidden;}

/* Esconde menu dos três pontinhos */
#MainMenu {visibility: hidden;}

/* Remove espaço vazio que sobra */
div.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Configuração da Página ---
st.set_page_config(
    page_title="Carielo NBA Scouts",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEFINIÇÃO DE VARIÁVEIS DE CORES (3 TONS CADA) ---
# Azul (NBA)
AZUL_NBA_CLARO = "#4169E1"
AZUL_NBA_MEDIO = "#17408B" # Cor Principal
AZUL_NBA_ESCURO = "#0C2340"

# Vermelho (NBA)
VERMELHO_NBA_CLARO = "#FF4C4C"
VERMELHO_NBA_MEDIO = "#C9082A" # Cor Principal
VERMELHO_NBA_ESCURO = "#8B0000"

# Branco
BRANCO_CLARO = "#FFFFFF"
BRANCO_MEDIO = "#F0F2F6" # Padrão Streamlit (Cinza muito claro)
BRANCO_ESCURO = "#E0E0E0"

# Preto
PRETO_CLARO = "#333333"
PRETO_MEDIO = "#1E1E1E"
PRETO_ESCURO = "#121212"

# Laranja (Basquete)
LARANJA_BASQUETE_CLARO = "#FC9C50"
LARANJA_BASQUETE_MEDIO = "#FA8320"
LARANJA_BASQUETE_ESCURO = "#C05805"

# --- MAPEAMENTO DE CORES NOS ELEMENTOS (Edite aqui para mudar o tema) ---
# Fundo e Texto Principal
VAR_COR_FUNDO_APP = BRANCO_CLARO           # Onde usar: Background geral do app
VAR_COR_TEXTO_PRINCIPAL = PRETO_CLARO      # Onde usar: Texto padrão do corpo (Legibilidade)
VAR_COR_TEXTO_SECUNDARIO = AZUL_NBA_MEDIO # Onde usar: Texto secundário

# Cabeçalhos (H1, H2, H3...)
VAR_COR_TITULOS = AZUL_NBA_MEDIO        # Onde usar: Títulos principais

# Botões
VAR_COR_BOTAO_FUNDO = AZUL_NBA_MEDIO # Onde usar: Cor de fundo dos botões
VAR_COR_BOTAO_TEXTO = BRANCO_CLARO    # Onde usar: Cor do texto dentro do botão
VAR_COR_BOTAO_HOVER = AZUL_NBA_ESCURO # Onde usar: Cor do botão ao passar o mouse

# Barra Lateral (Sidebar)
VAR_COR_SIDEBAR_FUNDO = AZUL_NBA_MEDIO  # Onde usar: Fundo da barra lateral
VAR_COR_SIDEBAR_TEXTO = BRANCO_CLARO       # Onde usar: Textos gerais na sidebar
VAR_COR_SIDEBAR_TITULOS = BRANCO_CLARO # Onde usar: Títulos dentro da sidebar (Contraste no Azul)
VAR_COR_SIDEBAR_INPUT_BG = BRANCO_CLARO # Onde usar: Fundo dos campos de seleção/texto
VAR_COR_SIDEBAR_INPUT_TXT = PRETO_CLARO   # Onde usar: Texto dentro dos campos
VAR_COR_SIDEBAR_RADIO_TEXTO = BRANCO_CLARO # Onde usar: Texto das opções de radio na sidebar
VAR_COR_BOTAO_RESET_FUNDO = VERMELHO_NBA_MEDIO # Onde usar: Fundo do botão de reset (Visão Geral)
VAR_COR_BOTAO_RESET_TEXTO = BRANCO_CLARO # Onde usar: Texto do botão de reset

# Elementos de Interface (Cards, Métricas, Tabelas)
VAR_COR_CARD_FUNDO = BRANCO_MEDIO          # Onde usar: Fundo de containers e tabelas
VAR_COR_EXPANDER_BORDA = AZUL_NBA_MEDIO # Onde usar: Borda dos elementos expansíveis
VAR_COR_EXPANDER_TEXTO = AZUL_NBA_MEDIO # Onde usar: Texto dos elementos expansíveis
VAR_COR_METRICA_FUNDO = BRANCO_MEDIO       # Onde usar: Fundo do card de métrica
VAR_COR_METRICA_BORDA = VERMELHO_NBA_MEDIO # Onde usar: Borda lateral de destaque da métrica
VAR_COR_METRICA_LABEL = AZUL_NBA_MEDIO  # Onde usar: Rótulo (título) da métrica
VAR_COR_METRICA_VALOR = VERMELHO_NBA_MEDIO  # Onde usar: Valor numérico da métrica
VAR_COR_ABA_TEXTO = AZUL_NBA_MEDIO      # Onde usar: Texto das abas NÃO selecionadas
VAR_COR_ABA_SELECIONADA_BG = AZUL_NBA_MEDIO # Onde usar: Cor de FUNDO da aba SELECIONADA
VAR_COR_ABA_SELECIONADA_TXT = BRANCO_CLARO   # Onde usar: Cor do TEXTO da aba SELECIONADA

# Cores para caixas de informação (st.info)
VAR_COR_INFO_BG = AZUL_NBA_MEDIO      # Onde usar: Fundo das caixas de informação (st.info)
VAR_COR_INFO_TXT = BRANCO_CLARO    # Onde usar: Texto dentro das caixas de informação


# Destaques Específicos
VAR_COR_DESTAQUE_LINHA_BG = VERMELHO_NBA_MEDIO # Onde usar: Fundo da linha do jogador selecionado
VAR_COR_DESTAQUE_LINHA_TXT = BRANCO_CLARO # Onde usar: Texto da linha do jogador selecionado

# Scrollbar
VAR_COR_SCROLLBAR_THUMB = VERMELHO_NBA_MEDIO # Onde usar: Cor da barra de rolagem
VAR_COR_SCROLLBAR_HOVER = VERMELHO_NBA_ESCURO # Onde usar: Cor da barra de rolagem ao passar o mouse

# --- Estilos CSS (Injetando as variáveis) ---
st.markdown(f"""
    <style>
        /* NBA Theme Variables Applied */
        
        /* Main App Background */
        .stApp {{
            background-color: {VAR_COR_FUNDO_APP};
            color: {VAR_COR_TEXTO_PRINCIPAL};
        }}

        /* Headers */
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: {VAR_COR_TITULOS} !important;
        }}

        /* Botões */
        div[data-testid="stButton"] > button {{
            background-color: {VAR_COR_BOTAO_FUNDO} !important;
            color: {VAR_COR_BOTAO_TEXTO} !important;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }}
        div[data-testid="stButton"] > button:hover {{
            background-color: {VAR_COR_BOTAO_HOVER} !important;
            color: {VAR_COR_BOTAO_TEXTO} !important;
        }}
        /* Botão Primário (Visão Geral - Vermelho) */
        div[data-testid="stButton"] > button[kind="primary"] {{
            background-color: {VAR_COR_BOTAO_RESET_FUNDO} !important;
            color: {VAR_COR_BOTAO_RESET_TEXTO} !important;
        }}
        div[data-testid="stButton"] > button[kind="primary"]:hover {{
            background-color: {VERMELHO_NBA_ESCURO} !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {VAR_COR_SIDEBAR_FUNDO};
        }}
        /* Textos na Sidebar */
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stSelectbox > label,
        [data-testid="stSidebar"] .stCaptionContainer,
        [data-testid="stSidebar"] span {{
            color: {VAR_COR_SIDEBAR_TEXTO} !important;
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
            color: {VAR_COR_SIDEBAR_TITULOS} !important;
        }}
        
        /* Opções de Radio Button na Sidebar (Próximos Jogos, Geral, Casa, Fora) */
        [data-testid="stSidebar"] .stRadio label p,
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div {{
            color: {VAR_COR_SIDEBAR_RADIO_TEXTO} !important;
        }}

        /* Inputs na Sidebar */
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background-color: {VAR_COR_SIDEBAR_INPUT_BG};
            color: {VAR_COR_SIDEBAR_INPUT_TXT} !important;
        }}
        [data-testid="stSidebar"] div[data-baseweb="select"] svg {{
            color: {VAR_COR_SIDEBAR_INPUT_TXT} !important;
        }}

        /* Cards, Expanders e Tabelas */
        .stExpander {{
            background-color: {VAR_COR_CARD_FUNDO} !important;
            border: 1px solid {VAR_COR_EXPANDER_BORDA} !important;
            border-radius: 5px;
            color: {VAR_COR_EXPANDER_TEXTO} !important;
        }}
        .stMetric, div[data-testid="stDataFrame"] {{
            background-color: {VAR_COR_METRICA_FUNDO} !important;
            border-radius: 5px;
        }}
        .stMetric {{
            border-left: 5px solid {VAR_COR_METRICA_BORDA};
            padding: 10px;
        }}
        /* Cor dos textos dentro das métricas */
        [data-testid="stMetricLabel"] {{
            color: {VAR_COR_METRICA_LABEL} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {VAR_COR_METRICA_VALOR} !important;
        }}

        /* --- AQUI VOCÊ COLORE AS ABAS --- */
        /* Texto das abas NÃO selecionadas */
        [data-testid="stTabs"] button p {{
            color: {VAR_COR_ABA_TEXTO} !important;
            font-weight: bold;
        }}
        /* Fundo e texto da aba que ESTÁ SELECIONADA */
        [data-testid="stTabs"] button[aria-selected="true"] {{
            background-color: {VAR_COR_ABA_SELECIONADA_BG} !important;
            border-radius: 5px 5px 0 0;
        }}
        [data-testid="stTabs"] button[aria-selected="true"] p {{
            color: {VAR_COR_ABA_SELECIONADA_TXT} !important;
        }}
        
        /* Caixas de Informação (st.info) */
        div[data-testid="stAlert"] {{
            background-color: {VAR_COR_INFO_BG} !important;
            border-radius: 5px;
            border: 1px solid {VAR_COR_INFO_BG};
        }}
        div[data-testid="stAlert"] p, div[data-testid="stAlert"] div, div[data-testid="stAlert"] span {{
            color: {VAR_COR_INFO_TXT} !important;
        }}
        
        /* Reduzir espaçamento no sidebar */
        [data-testid="stSidebar"] .stElementContainer {{
            margin-bottom: -10px;
        }}

        /* --- Custom Scrollbar --- */
        /* Works on Webkit browsers (Chrome, Safari, Edge) */
        ::-webkit-scrollbar {{
            width: 12px;
        }}
        ::-webkit-scrollbar-track {{
            background: {VAR_COR_FUNDO_APP}; 
        }}
        ::-webkit-scrollbar-thumb {{
            background-color: {VAR_COR_SCROLLBAR_THUMB};
            border-radius: 10px;
            border: 3px solid {VAR_COR_FUNDO_APP};
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background-color: {VAR_COR_SCROLLBAR_HOVER};
        }}
    </style>
""", unsafe_allow_html=True)

# --- Dicionários e Constantes ---
TIME_PARA_FULL = {
    "76ers": "Philadelphia 76ers", "Bucks": "Milwaukee Bucks", "Bulls": "Chicago Bulls",
    "Cavaliers": "Cleveland Cavaliers", "Celtics": "Boston Celtics", "Clippers": "Los Angeles Clippers",
    "Grizzlies": "Memphis Grizzlies", "Hawks": "Atlanta Hawks", "Heat": "Miami Heat",
    "Hornets": "Charlotte Hornets", "Jazz": "Utah Jazz", "Kings": "Sacramento Kings",
    "Knicks": "New York Knicks", "Lakers": "Los Angeles Lakers", "Magic": "Orlando Magic",
    "Mavericks": "Dallas Mavericks", "Nets": "Brooklyn Nets", "Nuggets": "Denver Nuggets",
    "Pacers": "Indiana Pacers", "Pelicans": "New Orleans Pelicans", "Pistons": "Detroit Pistons",
    "Raptors": "Toronto Raptors", "Rockets": "Houston Rockets", "Spurs": "San Antonio Spurs",
    "Suns": "Phoenix Suns", "Thunder": "Oklahoma City Thunder", "Timberwolves": "Minnesota Timberwolves",
    "Trail Blazers": "Portland Trail Blazers", "Warriors": "Golden State Warriors", "Wizards": "Washington Wizards",
}
ABREV_PARA_FULL = {
    "ATL": "Atlanta Hawks", "BOS": "Boston Celtics", "BKN": "Brooklyn Nets", "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls", "CLE": "Cleveland Cavaliers", "DAL": "Dallas Mavericks", "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons", "GSW": "Golden State Warriors", "HOU": "Houston Rockets", "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers", "LAL": "Los Angeles Lakers", "MEM": "Memphis Grizzlies", "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks", "MIN": "Minnesota Timberwolves", "NOP": "New Orleans Pelicans", "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder", "ORL": "Orlando Magic", "PHI": "Philadelphia 76ers", "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers", "SAC": "Sacramento Kings", "SAS": "San Antonio Spurs", "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz", "WAS": "Washington Wizards",
}

# --- Funções de Carregamento de Dados (com cache) ---
@st.cache_data
def load_all_data():
    path_base = os.path.dirname(os.path.abspath(__file__))
    
    # Caminhos dos arquivos
    csv_file = os.path.join(path_base, "PlayerStatistics_Clean.csv")
    csv_linhas = os.path.join(path_base, "linhas.csv")
    csv_jogadores = os.path.join(path_base, "jogadoresnba.csv")

    # Verifica se arquivos existem
    if not all(os.path.exists(p) for p in [csv_file, csv_linhas, csv_jogadores]):
        st.error("Arquivos CSV não encontrados! Verifique se 'PlayerStatistics_Clean.csv', 'linhas.csv' e 'jogadoresnba.csv' estão na pasta do app.")
        return None, None, None

    # Carrega DF principal
    df_completo = pd.read_csv(csv_file, sep=';', engine='python', encoding='utf-8-sig')
    df_completo.columns = [c.strip() for c in df_completo.columns]
    df_completo['Data_Hora_Jogo'] = pd.to_datetime(df_completo['Data_Hora_Jogo'], dayfirst=True, errors='coerce')
    df_completo['Data_Limpa'] = df_completo['Data_Hora_Jogo'].dt.strftime('%d/%m/%Y')
    df_completo['Time_Full'] = df_completo['Nome_Time'].astype(str).map(TIME_PARA_FULL).fillna(df_completo['Nome_Time'].astype(str))
    df_completo['Opp_Full'] = df_completo['Nome_Oponente'].astype(str).map(TIME_PARA_FULL).fillna(df_completo['Nome_Oponente'].astype(str))
    df_completo['Nome_Full'] = df_completo['Nome'].astype(str).str.strip() + " " + df_completo['Sobrenome'].astype(str).str.strip()

    # Carrega DF de linhas
    try:
        df_linhas = pd.read_csv(csv_linhas, sep=None, engine='python', encoding='utf-8-sig')
    except UnicodeDecodeError:
        df_linhas = pd.read_csv(csv_linhas, sep=None, engine='python', encoding='latin1')
    df_linhas.columns = [c.strip().lower() for c in df_linhas.columns]

    # Carrega DF de jogadores/imagens
    df_players_images = pd.read_csv(csv_jogadores, sep=None, engine='python', encoding='utf-8')
    df_players_images.columns = [c.strip() for c in df_players_images.columns]
    if 'Nome' in df_players_images.columns and 'Sobrenome' in df_players_images.columns:
        df_players_images['Nome_Full'] = df_players_images['Nome'].astype(str).str.strip() + " " + df_players_images['Sobrenome'].astype(str).str.strip()

    return df_completo, df_linhas, df_players_images

# --- Carregamento Inicial ---
df_completo, df_linhas, df_players_images = load_all_data()

if df_completo is None:
    st.stop() # Para a execução se os arquivos não foram carregados

# --- Função para buscar Próximos Jogos (API NBA) ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_nba_schedule():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "jogos.csv")
    if not os.path.exists(file_path):
        return {}
    
    try:
        # Tenta ler com separador ;
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        
        # Normaliza colunas para minúsculo e remove espaços
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Verifica se as colunas essenciais existem
        if 'data' not in df.columns or 'equipe_casa' not in df.columns:
             # Fallback para tentar ler com vírgula se o separador não for ;
             df = pd.read_csv(file_path, sep=',', encoding='utf-8')
             df.columns = [c.strip().lower() for c in df.columns]

        # Converte data
        df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
        
        # Filtra hoje e próximos 2 dias
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = today + timedelta(days=3) 
        
        mask = (df['data'] >= today) & (df['data'] < end_date)
        df_filtered = df[mask].copy().sort_values('data')
        
        schedule = {}
        
        for _, row in df_filtered.iterrows():
            d_lbl = row['data'].strftime('%d/%m/%Y')
            
            # Nomes dos times
            home_full = str(row.get('equipe_casa', '')).strip()
            away_full = str(row.get('equipe_fora', '')).strip()
            
            game_id = row.get('gameid', f"{home_full}-{away_full}")
            
            # Extrai o último nome para o logo (ex: "Chicago Bulls" -> "bulls")
            home_last = home_full.split()[-1].lower() if home_full else ""
            away_last = away_full.split()[-1].lower() if away_full else ""
            
            # Caminhos dos logos
            home_logo = os.path.join(base_dir, "assets", "teams", f"{home_last}.png")
            away_logo = os.path.join(base_dir, "assets", "teams", f"{away_last}.png")
            
            # Status (Horário ou VS)
            if row['data'].hour != 0 or row['data'].minute != 0:
                status = row['data'].strftime('%H:%M')
            else:
                status = "VS"
            
            if d_lbl not in schedule:
                schedule[d_lbl] = []
                
            schedule[d_lbl].append({
                "id": game_id,
                "home": home_full,
                "away": away_full,
                "status": status,
                "home_logo": home_logo,
                "away_logo": away_logo
            })
            
        return schedule

    except Exception as e:
        print(f"Erro ao ler jogos.csv: {e}")
        return {}

def ir_para_analise(equipe, oponente, local):
    st.session_state.nav_radio = "Análise Individual"
    st.session_state.combo_eq = equipe
    st.session_state.combo_opp = oponente
    st.session_state.radio_local = local
    
    # Seleciona automaticamente o jogador com mais minutos (Top 1)
    df_eq = df_completo[df_completo['Time_Full'] == equipe]
    if not df_eq.empty:
        df_min = df_eq.groupby('Nome_Full')['Minutos'].mean().sort_values(ascending=False)
        if not df_min.empty:
            st.session_state.combo_jog = df_min.index[0]

def inverter_times_local():
    # Pega valores atuais
    eq_atual = st.session_state.get("combo_eq", "Selecione a Equipe...")
    opp_atual = st.session_state.get("combo_opp", "Selecione...")
    loc_atual = st.session_state.get("radio_local", "Geral")
    
    # Inverte Equipes
    new_eq = opp_atual if opp_atual != "Selecione..." else "Selecione a Equipe..."
    new_opp = eq_atual if eq_atual != "Selecione a Equipe..." else "Selecione..."
    
    st.session_state.combo_eq = new_eq
    st.session_state.combo_opp = new_opp
    
    # Inverte Local
    if loc_atual == "Casa":
        st.session_state.radio_local = "Fora"
    elif loc_atual == "Fora":
        st.session_state.radio_local = "Casa"
        
    # Seleciona automaticamente o jogador com mais minutos da nova equipe
    if new_eq != "Selecione a Equipe...":
        df_eq = df_completo[df_completo['Time_Full'] == new_eq]
        if not df_eq.empty:
            df_min = df_eq.groupby('Nome_Full')['Minutos'].mean().sort_values(ascending=False)
            if not df_min.empty:
                st.session_state.combo_jog = df_min.index[0]

# --- Inicialização do Estado da Sessão ---
if 'filtro_local' not in st.session_state:
    st.session_state.filtro_local = "Geral"

# --- Funções de Lógica ---
def get_player_photo_path(nome_jogador):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_foto = None
    path_assets_players = os.path.join(base_dir, "assets", "players")

    if df_players_images is not None and 'Nome_Full' in df_players_images.columns:
        match = df_players_images[df_players_images['Nome_Full'].str.lower() == nome_jogador.lower()]
        if not match.empty:
            rel_path = match.iloc[0].get('image_path')
            if pd.notna(rel_path):
                str_path = str(rel_path).replace("/", os.sep)
                path_foto = os.path.join(base_dir, str_path)

    if not path_foto or not os.path.exists(path_foto):
        path_foto = os.path.join(path_assets_players, f"{nome_jogador}.png")

    if os.path.exists(path_foto):
        return path_foto
    
    # Fallback para imagem padrão
    return os.path.join(base_dir, "assets", "perfiljogador.png")


# =================================================================
# INTERFACE DO USUÁRIO (UI)
# =================================================================

# --- Barra Lateral (Sidebar) para Filtros ---
with st.sidebar:
    st.title("Carielo NBA")
    
    # Navegação Principal
    nav_opcao = st.radio("Navegação", ["Próximos Jogos", "Análise Individual"], key="nav_radio")
    
    st.markdown("---")

    if nav_opcao == "Análise Individual":
        st.header("Filtros de Análise")

        # Filtro de Equipe
        lista_equipes = sorted([e for e in df_completo['Time_Full'].unique() if str(e) != 'nan'])
        equipe_selecionada = st.selectbox(
            "Equipe",
            options=["Selecione a Equipe..."] + lista_equipes,
            key="combo_eq"
        )
        # Filtro de Jogador (dinâmico)
        if equipe_selecionada != "Selecione a Equipe...":
            df_eq = df_completo[df_completo['Time_Full'] == equipe_selecionada].copy()
            df_min_medias = df_eq.groupby('Nome_Full')['Minutos'].mean().sort_values(ascending=False)
            lista_jogadores = df_min_medias.index.tolist()
        else:
            lista_jogadores = []

        jogador_selecionado = st.selectbox(
            "Jogador",
            options=["Selecione o Jogador..."] + lista_jogadores,
            key="combo_jog"
        )

        # Filtro de Adversário
        lista_opp = sorted([e for e in df_completo['Opp_Full'].unique() if str(e) != 'nan'])
        opp_selecionado = st.selectbox(
            "Próximo Adversário",
            options=["Selecione..."] + lista_opp,
            key="combo_opp"
        )

        if st.button("🔄 Inverter Seleção", on_click=inverter_times_local):
            pass

        # Filtros de Contexto
        st.caption("CONTEXTO DA ANÁLISE")
        st.session_state.filtro_local = st.radio(
            "Local da Partida",
            options=["Geral", "Casa", "Fora"],
            horizontal=True,
            key="radio_local"
        )

        periodo_selecionado = st.selectbox(
            "Período dos Jogos",
            options=["Todos", "Últimos 5", "Últimos 10"],
            index=2, # Padrão "Últimos 10"
            key="combo_qtd"
        )

        st.markdown("---")
        if st.button("🔄 Limpar Filtros"):
            keys_to_reset = ["combo_eq", "combo_jog", "combo_opp", "radio_local", "combo_qtd"]
            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]
            for key in st.session_state.keys():
                if key.startswith("bet_"): del st.session_state[key]
            st.rerun()

# --- Área Principal ---
col_main, col_info = st.columns([2.5, 1])

if st.session_state.nav_radio == "Próximos Jogos":
    st.markdown("### 📅 Próximos Jogos (NBA)")
    schedule = get_nba_schedule()
    
    if not schedule:
        st.info("Nenhum jogo encontrado para os próximos dias ou erro na API.")
    else:
        for date_lbl, games in schedule.items():
            st.subheader(f"Jogos de {date_lbl}")
            if not games:
                st.write("Sem jogos agendados.")
                continue
                
            for game in games:
                with st.container(border=True): # Cada jogo em seu container
                    c1, c2, c3 = st.columns([2.5, 0.8, 2.5]) # Colunas para Casa | VS | Fora
                    
                    # Time da Casa
                    with c1:
                        col_i, col_b = st.columns([1, 2]) # Coluna para Logo e Botão
                        with col_i:
                            if os.path.exists(game['home_logo']):
                                st.image(game['home_logo'], width=40) # Imagem menor
                        with col_b:
                            st.button(f"{game['home']}", key=f"btn_home_{game['id']}", use_container_width=True,
                                      on_click=ir_para_analise, args=(game['home'], game['away'], "Casa"))
                    
                    # Info Central
                    with c2:
                        # Adiciona um pouco de margem para alinhar melhor verticalmente
                        st.markdown(f"<div style='text-align: center; font-weight: bold; margin-top: 5px;'>VS<br><span style='font-size: 0.7em; color: gray;'>{game['status']}</span></div>", unsafe_allow_html=True)
                    
                    # Time Visitante
                    with c3:
                        col_b, col_i = st.columns([2, 1]) # Coluna para Botão e Logo
                        with col_b:
                            st.button(f"{game['away']}", key=f"btn_away_{game['id']}", use_container_width=True,
                                      on_click=ir_para_analise, args=(game['away'], game['home'], "Fora"))
                        with col_i:
                            if os.path.exists(game['away_logo']):
                                st.image(game['away_logo'], width=40) # Imagem menor

else:
    # --- Lógica Original da Tela de Análise ---
    with col_main:
        st.markdown("### Carielo NBA Scouts 🏀")

    # --- Lógica de Filtragem Principal ---
    df_jogador = df_completo[df_completo['Nome_Full'] == jogador_selecionado].copy()
    df_jogador = df_jogador.sort_values(by='Data_Hora_Jogo', ascending=False)

    for c in ['Pontos', 'Rebotes', 'Assistencias', '3PTS_Feitos', 'Minutos']:
        df_jogador[c] = pd.to_numeric(df_jogador[c], errors='coerce').fillna(0)

    df_jogador['P+R'] = df_jogador['Pontos'] + df_jogador['Rebotes']
    df_jogador = df_jogador[(df_jogador['Pontos'] + df_jogador['Rebotes'] + df_jogador['Assistencias']) > 0].copy()

    # Aplica filtros de contexto (local e período)
    df_filtrado = df_jogador.copy()
    if st.session_state.filtro_local == "Casa":
        df_filtrado = df_filtrado[df_filtrado['Casa'] == 1]
    elif st.session_state.filtro_local == "Fora":
        df_filtrado = df_filtrado[df_filtrado['Casa'] == 0]

    if periodo_selecionado == "Últimos 5":
        df_filtrado = df_filtrado.head(5)
    elif periodo_selecionado == "Últimos 10":
        df_filtrado = df_filtrado.head(10)


    # --- Coluna da Direita: Perfil e Análise de Confronto ---
    with col_info:
        # 2. Análise de Confronto (MOVEMOS PARA CIMA)
        st.subheader("Confronto")
        
        # H2H
        with st.container(border=True):
            st.markdown("**Head-to-Head (H2H)**")
            if opp_selecionado != "Selecione...":
                df_h2h = df_jogador[df_jogador['Opp_Full'] == opp_selecionado]
                if not df_h2h.empty:
                    mean_h2h = df_h2h[['Pontos', 'Rebotes', 'Assistencias', 'P+R']].mean()
                    st.markdown(f"Jogos: **{len(df_h2h)}**")
                    st.markdown(f"PTS: **{mean_h2h['Pontos']:.1f}** | REB: **{mean_h2h['Rebotes']:.1f}** | AST: **{mean_h2h['Assistencias']:.1f}**")
                else:
                    st.warning("Sem histórico")
            else:
                st.info("Selecione adversário")

        # Defensive Gaps
        st.markdown("**Defensive Gaps**")
        if opp_selecionado != "Selecione...":
            df_opp_sofre = df_completo[df_completo['Opp_Full'] == opp_selecionado].copy()
            if not df_opp_sofre.empty and 'Posicao_Jogador' in df_opp_sofre.columns:
                stats_pos = df_opp_sofre.groupby('Posicao_Jogador')[['Pontos', 'Rebotes', '3PTS_Feitos']].mean().sort_values(by='Pontos', ascending=False).head(3)
                stats_pos = stats_pos.reset_index().rename(columns={"Posicao_Jogador": "POS", "Pontos": "PTS", "Rebotes": "REB", "3PTS_Feitos": "3PTS"})
                st.dataframe(stats_pos, hide_index=True, use_container_width=True)
        else:
            st.info("Selecione adversário")

        # 2. Linha da Bet (Reposicionado)
        with st.container(border=True):
            st.markdown("**🎯 Linha da Bet**")
            bet_cols = st.columns(5) # Lado a lado
            bet_inputs = {}
            bet_labels = ["PTS", "REB", "AST", "P+R", "3P"] # Reorganizado para fluir melhor
            bet_keys = ["pts", "reb", "ast", "pr", "3p"]

            linha_jogador_df = df_linhas[df_linhas['jogador'].astype(str).str.contains(jogador_selecionado, case=False, na=False, regex=False)]
            
            for i, (label, key) in enumerate(zip(bet_labels, bet_keys)):
                default_val = ""
                if not linha_jogador_df.empty and key in linha_jogador_df.columns:
                    val = linha_jogador_df.iloc[0][key]
                    if pd.notna(val):
                        default_val = str(val)
                
                col = bet_cols[i]
                bet_inputs[key] = col.text_input(label, value=default_val, key=f"bet_{key}")

        # Projeção vs Linha
        with st.container(border=True):
            st.markdown("**Projeção vs Linha**")
            if not df_filtrado.empty:
                # Garante coluna P+R
                df_filtrado['P+R'] = df_filtrado['Pontos'] + df_filtrado['Rebotes']
                
                stats_config = [
                    ("PTS", "Pontos", "pts"),
                    ("REB", "Rebotes", "reb"),
                    ("P+R", "P+R", "pr"),
                    ("AST", "Assistencias", "ast")
                ]
                
                proj_data = []
                for label, col_df, key_bet in stats_config:
                    # 1. Mediana (Insights)
                    mediana = df_filtrado[col_df].median()
                    qtd_over_med = len(df_filtrado[df_filtrado[col_df] > mediana])
                    pct_med = (qtd_over_med / len(df_filtrado)) * 100
                    
                    # 2. Linha da Bet (Input do usuário)
                    linha_val_str = st.session_state.get(f"bet_{key_bet}", "")
                    pct_line_str = "-"
                    if linha_val_str:
                        try:
                            linha_val = float(linha_val_str.replace(",", "."))
                            qtd_over_line = len(df_filtrado[df_filtrado[col_df] > linha_val])
                            pct_line = (qtd_over_line / len(df_filtrado)) * 100
                            pct_line_str = f"{pct_line:.0f}%"
                        except ValueError:
                            pass
                    
                    proj_data.append({"Stat": label, "% > Med": f"{pct_med:.0f}%", "% > Line": pct_line_str})
                
                st.dataframe(pd.DataFrame(proj_data), hide_index=True, use_container_width=True)
            else:
                st.write("Sem dados.")

    # --- Coluna Principal: Abas e Tabelas ---
    with col_main:
        # --- Perfil do Jogador (Movido para cá) ---
        with st.container(border=True):
            c1, c2 = st.columns([0.5, 4])
            path_foto = get_player_photo_path(jogador_selecionado)
            if os.path.exists(path_foto):
                c1.image(path_foto, width=80)
            
            posicao = df_jogador['Posicao_Jogador'].iloc[0] if 'Posicao_Jogador' in df_jogador.columns and not df_jogador.empty else "N/A"
            c2.markdown(f"### {jogador_selecionado.upper()}")
            c2.caption(f"Posição: {posicao}")

        # --- Função de Estilo para Destaque ---
        def highlight_selected_row(row):
            if 'JOGADOR' in row.index and row['JOGADOR'] == jogador_selecionado:
                # Usa as variáveis definidas no topo
                return [f'background-color: {VAR_COR_DESTAQUE_LINHA_BG}; color: {VAR_COR_DESTAQUE_LINHA_TXT}; font-weight: bold'] * len(row)
            return [''] * len(row)

        # --- Botão Visão Geral (Reset) ---
        c_spacer, c_reset = st.columns([5, 1])
        with c_reset:
            if st.button("Visão Geral", type="primary", use_container_width=True, help="Reseta filtros de equipe, jogador e oponente"):
                for k in ['combo_eq', 'combo_jog', 'combo_opp', 'radio_local', 'combo_qtd']:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()

        # --- Abas de Conteúdo ---
        tab_analise, tab_linhas, tab_mediana, tab_tips = st.tabs([
            "  📊 ANÁLISE INDIVIDUAL  ",
            "  📈 INSIGHTS DE LINHAS  ",
            "  📊 INSIGHTS DE MEDIANA  ",
            "   TIPS DO DIA 💰  "
        ])

        with tab_analise:
            if df_filtrado.empty:
                st.info("Selecione um jogador na barra lateral para visualizar a análise individual.")
            else:
                st.subheader("Histórico de Jogos")
                
                df_display = df_filtrado.copy()
                df_display['LOCAL'] = df_display['Casa'].apply(lambda x: "Casa" if x == 1 else "Fora")
                
                colunas_tabela = {
                    "Pontos": "PTS", "Rebotes": "REB", "P+R": "P+R",
                    "Assistencias": "AST", "3PTS_Feitos": "3PTS",
                    "Minutos": "MIN", "Data_Limpa": "DATA", "LOCAL": "LOCAL", "Opp_Full": "OPONENTE"
                }
                
                st.dataframe(
                    df_display[list(colunas_tabela.keys())].rename(columns=colunas_tabela),
                    hide_index=True,
                    use_container_width=True
                )

                st.divider()
                st.subheader("Insights Rápidos")
                
                cols_nba = {"MIN": "Minutos", "PTS": "Pontos", "REB": "Rebotes", "P+R": "P+R", "AST": "Assistencias", "3P": "3PTS_Feitos"}
                stats = df_filtrado[list(cols_nba.values())].agg(['median', 'mean', 'min', 'max'])
                stats.columns = list(cols_nba.keys())
                stats.index = ["Mediana", "Média", "Mínimo", "Máximo"]
                st.dataframe(stats.style.format("{:.1f}"), use_container_width=True)

        with tab_linhas:
            st.header("🎯 Insights de Linhas (via linhas.csv)")
            st.caption(f"Análise baseada no contexto: **{st.session_state.filtro_local}** | Período: **{periodo_selecionado}**")

        metric_data = []
        tips_automaticas = []

        for _, row_l in df_linhas.iterrows():
            nome_j = str(row_l.get('jogador', '')).strip()
            equipe_j_abrev = str(row_l.get('equipe', '')).strip()
            equipe_j_full = ABREV_PARA_FULL.get(equipe_j_abrev, equipe_j_abrev)
            detalhe = str(row_l.get('detalhe', '')).strip()
            
            # Filtro Casa/Fora baseado na coluna 'casa' do linhas.csv
            # 1 = Casa, 0 = Fora
            try:
                is_home_game = int(float(str(row_l.get('casa', -1))))
            except:
                is_home_game = -1

            if st.session_state.filtro_local == "Casa" and is_home_game != 1:
                continue
            if st.session_state.filtro_local == "Fora" and is_home_game != 0:
                continue

            # Filtro de equipe
            if equipe_selecionada != "Selecione a Equipe..." and equipe_j_full != equipe_selecionada:
                continue

            try:
                v_pts = float(str(row_l.get('pts', 0)).replace(',', '.'))
                v_rbt = float(str(row_l.get('reb', 0)).replace(',', '.'))
                v_pr = float(str(row_l.get('pr', 0)).replace(',', '.'))
            except: continue

            df_j_metric = df_completo[df_completo['Nome_Full'].str.contains(nome_j, case=False, na=False)].copy()
            
            if not df_j_metric.empty:
                # Aplica filtros de contexto
                if st.session_state.filtro_local == "Casa": df_j_metric = df_j_metric[df_j_metric['Casa'] == 1]
                elif st.session_state.filtro_local == "Fora": df_j_metric = df_j_metric[df_j_metric['Casa'] == 0]
                
                df_j_metric = df_j_metric.sort_values(by='Data_Hora_Jogo', ascending=False)
                if periodo_selecionado == "Últimos 5": df_j_metric = df_j_metric.head(5)
                elif periodo_selecionado == "Últimos 10": df_j_metric = df_j_metric.head(10)

                total = len(df_j_metric)
                if total > 0:
                    # Garante que as colunas de estatísticas sejam numéricas e sem NaN
                    for col in ['Pontos', 'Rebotes']:
                        df_j_metric[col] = pd.to_numeric(df_j_metric[col], errors='coerce').fillna(0)
                    df_j_metric['P+R'] = df_j_metric['Pontos'] + df_j_metric['Rebotes']
                    
                    # Mins
                    mins = df_j_metric[['Pontos', 'Rebotes', 'P+R']].min()

                    p_pts = (len(df_j_metric[df_j_metric['Pontos'] > v_pts]) / total * 100) if not pd.isna(v_pts) else 0
                    p_rbt = (len(df_j_metric[df_j_metric['Rebotes'] > v_rbt]) / total * 100) if not pd.isna(v_rbt) else 0
                    p_pr = (len(df_j_metric[df_j_metric['P+R'] > v_pr]) / total * 100) if v_pr > 0 and not pd.isna(v_pr) else 0

                    # Confidence (Floor vs Line)
                    def calc_conf(min_val, line_val):
                        if pd.isna(line_val) or line_val == 0: return 0.0
                        if pd.isna(min_val): return 0.0
                        return (min_val / line_val) * 100

                    conf_pts = calc_conf(mins['Pontos'], v_pts)
                    conf_reb = calc_conf(mins['Rebotes'], v_rbt)
                    conf_pr = calc_conf(mins['P+R'], v_pr)

                    # Lógica para Tips Automáticas (> 75% Confiança)
                    if conf_pts > 75:
                        over_count = len(df_j_metric[df_j_metric['Pontos'] > v_pts])
                        tips_automaticas.append({
                            "JOGADOR": nome_j, "TIME": equipe_j_full, "MERCADO": "Pontos", 
                            "LINHA": v_pts, "PISO": int(mins['Pontos']), "CONFIANÇA": conf_pts,
                            "MÉDIA": f"{over_count} de {total}"
                        })
                    if conf_reb > 75:
                        over_count = len(df_j_metric[df_j_metric['Rebotes'] > v_rbt])
                        tips_automaticas.append({
                            "JOGADOR": nome_j, "TIME": equipe_j_full, "MERCADO": "Rebotes", 
                            "LINHA": v_rbt, "PISO": int(mins['Rebotes']), "CONFIANÇA": conf_reb,
                            "MÉDIA": f"{over_count} de {total}"
                        })
                    if conf_pr > 75:
                        over_count = len(df_j_metric[df_j_metric['P+R'] > v_pr])
                        tips_automaticas.append({
                            "JOGADOR": nome_j, "TIME": equipe_j_full, "MERCADO": "P+R", 
                            "LINHA": v_pr, "PISO": int(mins['P+R']), "CONFIANÇA": conf_pr,
                            "MÉDIA": f"{over_count} de {total}"
                        })

                    # Garante que os valores que serão convertidos para int não sejam NaN
                    metric_data.append({
                        "EQUIPE": equipe_j_full, "JOGADOR": nome_j, 
                        "L_PTS": int(v_pts) if not pd.isna(v_pts) else 0, "MIN PTS": int(mins['Pontos']), "CONF PTS": conf_pts, "PTS %": f"{p_pts:.0f}%",
                        "L_REB": int(v_rbt) if not pd.isna(v_rbt) else 0, "MIN REB": int(mins['Rebotes']), "CONF REB": conf_reb, "REB %": f"{p_rbt:.0f}%",
                        "L_PR": int(v_pr) if not pd.isna(v_pr) else 0, "MIN PR": int(mins['P+R']), "CONF PR": conf_pr, "PR %": f"{p_pr:.0f}%",
                        "DETALHE": detalhe
                    })

        if metric_data:
            df_metricas_display = pd.DataFrame(metric_data)
            st.dataframe(
                df_metricas_display.style.apply(highlight_selected_row, axis=1), 
                use_container_width=True, 
                hide_index=True,
                column_config={
                     "CONF PTS": st.column_config.NumberColumn(format="%d%%"),
                     "CONF REB": st.column_config.NumberColumn(format="%d%%"),
                     "CONF PR": st.column_config.NumberColumn(format="%d%%"),
                }
            )
        else:
            st.info("Nenhuma métrica encontrada para os filtros atuais.")

        with st.expander("ℹ️ Legenda das Métricas (Clique para ver)"):
            st.markdown("""
            *   **L_ (Linha):** Valor da linha oferecida pela casa de apostas.
            *   **MIN (Piso):** O menor valor registrado pelo jogador no período selecionado (ex: Últimos 10 jogos).
            *   **CONF (Confiança):** Relação entre o Piso e a Linha ($$\\frac{\\text{Piso}}{\\text{Linha}} \\times 100$$).
                *   *Acima de 100%:* O jogador bateu a linha em **todos** os jogos do período (Piso > Linha).
                *   *Próximo de 100%:* O pior jogo do jogador foi muito próximo da linha.
            *   **% (Hit Rate):** Porcentagem de jogos em que o jogador superou a linha.
            """)

        with tab_mediana:
            st.header("📊 Insights de Mediana (Tendência)")
            st.caption(f"Jogadores com ≥ 50% de jogos acima da mediana da temporada nos {periodo_selecionado}.")
            
            if equipe_selecionada != "Selecione a Equipe...":
                players_to_scan = df_completo[df_completo['Time_Full'] == equipe_selecionada]['Nome_Full'].unique()
            else:
                players_to_scan = df_completo['Nome_Full'].unique()
                
            data_mediana = []
            data_consistencia = []
            data_teto = []
            
            # Contexto global para cálculo de mediana (Temporada)
            df_context_global = df_completo.copy()
            if st.session_state.filtro_local == "Casa":
                df_context_global = df_context_global[df_context_global['Casa'] == 1]
            elif st.session_state.filtro_local == "Fora":
                df_context_global = df_context_global[df_context_global['Casa'] == 0]
                
            for player in players_to_scan:
                df_p = df_context_global[df_context_global['Nome_Full'] == player].sort_values(by='Data_Hora_Jogo', ascending=False)
                if df_p.empty: continue
                
                # Mediana da Temporada (Baseline)
                # Garante conversão numérica para cálculo
                for c in ['Pontos', 'Rebotes', 'Assistencias', 'Minutos']:
                    df_p[c] = pd.to_numeric(df_p[c], errors='coerce').fillna(0)

                if df_p['Minutos'].mean() < 25: continue

                team_name = df_p['Nome_Time'].iloc[0] if 'Nome_Time' in df_p.columns else "-"
                df_p['P+R'] = df_p['Pontos'] + df_p['Rebotes']
                medians = df_p[['Pontos', 'Rebotes', 'Assistencias', 'P+R']].median()
                
                # Período Recente
                if periodo_selecionado == "Últimos 5": df_p_period = df_p.head(5)
                elif periodo_selecionado == "Últimos 10": df_p_period = df_p.head(10)
                else: df_p_period = df_p

                if df_p_period.empty: continue
                
                total_games = len(df_p_period)
                
                # --- Lógica 1: Tendência (% Over Mediana) ---
                pct_pts = (len(df_p_period[df_p_period['Pontos'] > medians['Pontos']]) / total_games) * 100
                pct_reb = (len(df_p_period[df_p_period['Rebotes'] > medians['Rebotes']]) / total_games) * 100
                pct_ast = (len(df_p_period[df_p_period['Assistencias'] > medians['Assistencias']]) / total_games) * 100
                pct_pr = (len(df_p_period[df_p_period['P+R'] > medians['P+R']]) / total_games) * 100
                
                if pct_pts >= 50 or pct_reb >= 50 or pct_ast >= 50 or pct_pr >= 50:
                    data_mediana.append({
                        "TIME": team_name, "JOGADOR": player,
                        "MED PTS": int(medians['Pontos']), "% PTS": f"{pct_pts:.0f}%",
                        "MED REB": int(medians['Rebotes']), "% REB": f"{pct_reb:.0f}%",
                        "MED P+R": int(medians['P+R']), "% P+R": f"{pct_pr:.0f}%",
                        "MED AST": int(medians['Assistencias']), "% AST": f"{pct_ast:.0f}%"
                    })
                
                # --- Lógica 2: Consistência (Mínimo vs Mediana) ---
                mins = df_p_period[['Pontos', 'Rebotes', 'Assistencias', 'P+R']].min()
                
                def calc_conf(min_val, med_val):
                    if med_val == 0: return 0.0
                    return (min_val / med_val) * 100

                conf_pts = calc_conf(mins['Pontos'], medians['Pontos'])
                conf_reb = calc_conf(mins['Rebotes'], medians['Rebotes'])
                conf_ast = calc_conf(mins['Assistencias'], medians['Assistencias'])
                conf_pr = calc_conf(mins['P+R'], medians['P+R'])

                data_consistencia.append({
                    "TIME": team_name, "JOGADOR": player,
                    "MED PTS": int(medians['Pontos']), "MIN PTS": int(mins['Pontos']), "CONF PTS": conf_pts,
                    "MED REB": int(medians['Rebotes']), "MIN REB": int(mins['Rebotes']), "CONF REB": conf_reb,
                    "MED P+R": int(medians['P+R']), "MIN P+R": int(mins['P+R']), "CONF P+R": conf_pr,
                    "MED AST": int(medians['Assistencias']), "MIN AST": int(mins['Assistencias']), "CONF AST": conf_ast
                })

                # --- Lógica 3: Consistência (Teto vs Mediana - Foco em Under) ---
                maxs = df_p_period[['Pontos', 'Rebotes', 'Assistencias', 'P+R']].max()

                def calc_conf_teto(med_val, max_val):
                    if max_val == 0: return 0.0
                    # Quanto mais próximo de 100%, mais o Maximo está colado na Mediana (Bom para Under)
                    return (med_val / max_val) * 100

                conf_teto_pts = calc_conf_teto(medians['Pontos'], maxs['Pontos'])
                conf_teto_reb = calc_conf_teto(medians['Rebotes'], maxs['Rebotes'])
                conf_teto_ast = calc_conf_teto(medians['Assistencias'], maxs['Assistencias'])
                conf_teto_pr = calc_conf_teto(medians['P+R'], maxs['P+R'])

                data_teto.append({
                    "TIME": team_name, "JOGADOR": player,
                    "MED PTS": int(medians['Pontos']), "MAX PTS": int(maxs['Pontos']), "CONF PTS": conf_teto_pts,
                    "MED REB": int(medians['Rebotes']), "MAX REB": int(maxs['Rebotes']), "CONF REB": conf_teto_reb,
                    "MED P+R": int(medians['P+R']), "MAX P+R": int(maxs['P+R']), "CONF P+R": conf_teto_pr,
                    "MED AST": int(medians['Assistencias']), "MAX AST": int(maxs['Assistencias']), "CONF AST": conf_teto_ast
                })
                    
            if data_mediana:
                df_med = pd.DataFrame(data_mediana)
                cols_order_med = ["TIME", "JOGADOR", 
                                  "MED PTS", "% PTS", 
                                  "MED REB", "% REB", 
                                  "MED P+R", "% P+R",
                                  "MED AST", "% AST"]
                cols_final_med = [c for c in cols_order_med if c in df_med.columns]
                st.dataframe(df_med[cols_final_med].style.apply(highlight_selected_row, axis=1), use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum jogador encontrado com os critérios.")
                
            with st.expander("ℹ️ Legenda - Tendência"):
                st.markdown("""
                *   **MED (Mediana):** O valor central das estatísticas do jogador na temporada. Representa o desempenho "padrão".
                *   **% (Frequência):** Porcentagem de jogos no período recente onde o jogador superou sua própria mediana da temporada.
                    *   *Indica:* Se o jogador está em uma fase melhor (quente) ou pior (fria) que o seu normal.
                """)

            # --- Exibição da Seção de Consistência ---
            st.divider()
            st.subheader("🛡️ Consistência (Piso vs Mediana)")
            
            with st.expander("ℹ️ Como funciona este cálculo? (Clique para ver)"):
                st.markdown("""
                **Objetivo:** Identificar jogadores com um "piso" alto, ou seja, que mesmo em seus piores jogos recentes, mantiveram uma pontuação próxima à sua mediana habitual.
                
                **Fórmula:** $$\\frac{\\text{Mínimo do Período}}{\\text{Mediana da Temporada}} \\times 100$$
                
                *   **Mínimo do Período:** O menor valor que o jogador fez nos jogos selecionados (ex: Últimos 10).
                *   **Mediana da Temporada:** O valor central das estatísticas do jogador na temporada (filtrado por Casa/Fora).
                
                **Interpretação:**
                *   **Alta % (perto de 100%):** O jogador é muito consistente. Seu pior jogo é quase igual à sua média normal.
                *   **Baixa %:** O jogador tem alta variância. Em dias ruins, pontua muito pouco.
                """)

            if data_consistencia:
                df_consist = pd.DataFrame(data_consistencia)
                
                # Ordenar por padrão pela confiança de pontos
                df_consist = df_consist.sort_values(by="CONF PTS", ascending=False)

                # Ordenar colunas para facilitar leitura
                cols_order = ["TIME", "JOGADOR", 
                              "MED PTS", "MIN PTS", "CONF PTS", 
                              "MED REB", "MIN REB", "CONF REB",
                              "MED P+R", "MIN P+R", "CONF P+R",
                              "MED AST", "MIN AST", "CONF AST"]
                cols_final = [c for c in cols_order if c in df_consist.columns]
                st.dataframe(df_consist[cols_final].style.apply(highlight_selected_row, axis=1), 
                             use_container_width=True, 
                             hide_index=True,
                             column_config={
                                 "CONF PTS": st.column_config.NumberColumn(format="%d%%"),
                                 "CONF REB": st.column_config.NumberColumn(format="%d%%"),
                                 "CONF AST": st.column_config.NumberColumn(format="%d%%"),
                                 "CONF P+R": st.column_config.NumberColumn(format="%d%%"),
                             })
            else:
                st.write("Sem dados para consistência.")

            # --- Exibição da Seção de Teto (Under) ---
            st.divider()
            st.subheader("📉 Consistência (Teto vs Mediana) - Foco em Under")
            
            with st.expander("ℹ️ Como usar para Under? (Clique para ver)"):
                st.markdown("""
                **Objetivo:** Identificar jogadores com um "teto" baixo ou controlado. Ideal para buscar linhas de **UNDER**.
                
                **Fórmula:** $$\\frac{\\text{Mediana da Temporada}}{\\text{Máximo do Período}} \\times 100$$
                
                **Interpretação:**
                *   **Alta % (perto de 100%):** O Máximo que o jogador fez é muito próximo da sua Mediana. Isso sugere que ele raramente "explode" em pontuação. **Bom para Under.**
                *   **Baixa %:** O jogador tem um teto muito alto (ex: Mediana 20, Máximo 40 -> 50%). Perigoso para Under.
                """)

            if data_teto:
                df_teto_display = pd.DataFrame(data_teto)
                # Ordenar por padrão pela confiança de pontos (maior % = melhor para under)
                df_teto_display = df_teto_display.sort_values(by="CONF PTS", ascending=False)

                cols_order_teto = ["TIME", "JOGADOR", 
                              "MED PTS", "MAX PTS", "CONF PTS", 
                              "MED REB", "MAX REB", "CONF REB",
                              "MED P+R", "MAX P+R", "CONF P+R",
                              "MED AST", "MAX AST", "CONF AST"]
                cols_final_teto = [c for c in cols_order_teto if c in df_teto_display.columns]
                
                st.dataframe(df_teto_display[cols_final_teto].style.apply(highlight_selected_row, axis=1), 
                             use_container_width=True, 
                             hide_index=True,
                             column_config={
                                 "CONF PTS": st.column_config.NumberColumn(format="%d%%"),
                                 "CONF REB": st.column_config.NumberColumn(format="%d%%"),
                                 "CONF AST": st.column_config.NumberColumn(format="%d%%"),
                                 "CONF P+R": st.column_config.NumberColumn(format="%d%%"),
                             })
            else:
                st.write("Sem dados para teto.")

    with tab_tips:
        st.header("🔥 Consolidado de Dicas de Apostas")
        st.caption(f"Jogadores com Confiança (Piso vs Linha) > 75% | Filtro: {st.session_state.filtro_local}")
        
        if tips_automaticas:
            df_tips = pd.DataFrame(tips_automaticas)
            # Ordena por confiança
            df_tips = df_tips.sort_values(by="CONFIANÇA", ascending=False)
            
            st.dataframe(
                df_tips, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "CONFIANÇA": st.column_config.NumberColumn(format="%d%%")
                }
            )
        else:
            st.info("Nenhuma oportunidade de alta confiança (>75%) encontrada com os filtros atuais.")

        st.divider()
        st.header("🤝 Confiança H2H")
        st.caption("Jogadores que bateram a linha no último confronto direto.")
        
        h2h_tips = []

        for _, row_l in df_linhas.iterrows():
            nome_j = str(row_l.get('jogador', '')).strip()
            equipe_j_abrev = str(row_l.get('equipe', '')).strip()
            equipe_j_full = ABREV_PARA_FULL.get(equipe_j_abrev, equipe_j_abrev)
            
            opp_j_full = str(row_l.get('detalhe', '')).strip()
            if not opp_j_full:
                continue

            df_player_all = df_completo[df_completo['Nome_Full'].str.contains(nome_j, case=False, na=False)].copy()
            if df_player_all.empty:
                continue
            
            for col in ['Pontos', 'Rebotes', 'Assistencias']:
                df_player_all[col] = pd.to_numeric(df_player_all[col], errors='coerce').fillna(0)
            df_player_all['P+R'] = df_player_all['Pontos'] + df_player_all['Rebotes']

            df_h2h = df_player_all[df_player_all['Opp_Full'] == opp_j_full].sort_values('Data_Hora_Jogo', ascending=False)
            if df_h2h.empty:
                continue
            
            last_h2h_game = df_h2h.head(1)

            df_j_metric = df_player_all.copy()
            if st.session_state.filtro_local == "Casa": df_j_metric = df_j_metric[df_j_metric['Casa'] == 1]
            elif st.session_state.filtro_local == "Fora": df_j_metric = df_j_metric[df_j_metric['Casa'] == 0]
            df_j_metric = df_j_metric.sort_values(by='Data_Hora_Jogo', ascending=False)
            
            if periodo_selecionado == "Últimos 5": df_j_metric = df_j_metric.head(5)
            elif periodo_selecionado == "Últimos 10": df_j_metric = df_j_metric.head(10)

            total_media_games = len(df_j_metric)
            if total_media_games == 0:
                continue

            markets = {'pts': 'Pontos', 'reb': 'Rebotes', 'pr': 'P+R', 'ast': 'Assistencias'}
            
            for key, col_name in markets.items():
                try:
                    line = float(str(row_l.get(key, 'nan')).replace(',', '.'))
                    if pd.isna(line) or line == 0: continue
                except (ValueError, TypeError): continue

                last_h2h_stat = last_h2h_game[col_name].iloc[0]
                
                if last_h2h_stat > line:
                    h2h_overs = len(df_h2h[df_h2h[col_name] > line])
                    h2h_total = len(df_h2h)
                    h2h_pct = (h2h_overs / h2h_total) * 100 if h2h_total > 0 else 0
                    h2h_text = f"{h2h_overs} de {h2h_total} ({h2h_pct:.0f}%)"

                    media_overs = len(df_j_metric[df_j_metric[col_name] > line])
                    media_pct = (media_overs / total_media_games) * 100
                    media_text = f"{media_overs} de {total_media_games} ({media_pct:.0f}%)"

                    h2h_tips.append({
                        "EQUIPE": equipe_j_full, "JOGADOR": nome_j, "MERCADO": col_name,
                        "LINHA": line, "% H2H": h2h_text, "% MEDIA": media_text
                    })

        if h2h_tips:
            df_h2h_tips = pd.DataFrame(h2h_tips)
            st.dataframe(df_h2h_tips, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma dica H2H encontrada com base nos critérios.")