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
    
    # Correção para Linux/Github: Procura o arquivo ignorando maiúsculas/minúsculas
    if not os.path.exists(file_path):
        for f in os.listdir(base_dir):
            if f.lower() == "jogos.csv":
                file_path = os.path.join(base_dir, f)
                break
        if not os.path.exists(file_path): return {}
    
    try:
        # Tenta ler com separador ;
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        
        # Normaliza colunas para minúsculo e remove espaços
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Verifica se as colunas essenciais existem
        if 'data_partida' not in df.columns or 'equipe_casa' not in df.columns:
             # Fallback para tentar ler com vírgula se o separador não for ;
             df = pd.read_csv(file_path, sep=',', encoding='utf-8')
             df.columns = [c.strip().lower() for c in df.columns]

        # Converte data (Formato explícito: dd/mm/yyyy hh:mm)
        df['data_partida'] = df['data_partida'].astype(str).str.strip()
        df['data_partida'] = pd.to_datetime(df['data_partida'], format='%d/%m/%Y %H:%M', errors='coerce')
        
        # Remove linhas com datas inválidas (NaT)
        df = df.dropna(subset=['data_partida'])
        
        # Filtra hoje e próximos dias
        # Correção de Fuso Horário: Servidores Cloud usam UTC. 
        # Subtraímos 4h para garantir que jogos da noite (BRT/ET) apareçam mesmo se já virou o dia em UTC.
        today = (datetime.now() - timedelta(hours=4)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = today + timedelta(days=7) 
        
        mask = (df['data_partida'] >= today) & (df['data_partida'] < end_date)
        df_filtered = df[mask].copy().sort_values(by='data_partida', ascending=True)
        
        schedule = {}
        
        for _, row in df_filtered.iterrows():
            d_lbl = row['data_partida'].strftime('%d/%m/%Y')
            
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
            if row['data_partida'].hour != 0 or row['data_partida'].minute != 0:
                status = row['data_partida'].strftime('%H:%M')
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
        
        # --- Botão Visão Geral (Reset) ---
        c_reset, c_spacer = st.columns([1, 5])
        with c_reset:
            if st.button("Visão Geral", type="primary", use_container_width=True, help="Reseta filtros de equipe, jogador e oponente"):
                for k in ['combo_eq', 'combo_jog', 'combo_opp', 'radio_local', 'combo_qtd']:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()

    # --- Lógica de Filtragem Principal ---
    tem_jogador = jogador_selecionado != "Selecione o Jogador..."
    
    if tem_jogador:
        df_principal = df_completo[df_completo['Nome_Full'] == jogador_selecionado].copy()
    elif equipe_selecionada != "Selecione a Equipe...":
        df_principal = df_completo[df_completo['Time_Full'] == equipe_selecionada].copy()
    else:
        df_principal = df_completo.copy()

    df_principal = df_principal.sort_values(by='Data_Hora_Jogo', ascending=False)

    for c in ['Pontos', 'Rebotes', 'Assistencias', '3PTS_Feitos', 'Minutos', 'Tocos', 'Roubos de bola', 'Erros / Perdas de posse']:
        if c in df_principal.columns:
            df_principal[c] = pd.to_numeric(df_principal[c], errors='coerce').fillna(0)

    df_principal['P+R'] = df_principal['Pontos'] + df_principal['Rebotes']
    # df_principal = df_principal[(df_principal['Pontos'] + df_principal['Rebotes'] + df_principal['Assistencias']) > 0].copy()

    # Aplica filtros de contexto (local e período)
    df_filtrado = df_principal.copy()
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
        if tem_jogador:
            st.subheader("Confronto")
            
            # H2H
            with st.container(border=True):
                st.markdown("**Head-to-Head (H2H)**")
                if opp_selecionado != "Selecione...":
                    df_h2h = df_principal[df_principal['Opp_Full'] == opp_selecionado]
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
        else:
            st.info("Selecione um jogador para ver a análise detalhada de confronto e projeções.")

    # --- Coluna Principal: Abas e Tabelas ---
    with col_main:
        # --- Perfil do Jogador (Movido para cá) ---
        if tem_jogador:
            with st.container(border=True):
                c1, c2 = st.columns([0.5, 4])
                path_foto = get_player_photo_path(jogador_selecionado)
                if os.path.exists(path_foto):
                    c1.image(path_foto, width=80)
                
                posicao = df_principal['Posicao_Jogador'].iloc[0] if 'Posicao_Jogador' in df_principal.columns and not df_principal.empty else "N/A"
                c2.markdown(f"### {jogador_selecionado.upper()}")
                c2.caption(f"Posição: {posicao}")

        # --- Função de Estilo para Destaque ---
        def highlight_selected_row(row):
            if 'JOGADOR' in row.index and row['JOGADOR'] == jogador_selecionado:
                # Usa as variáveis definidas no topo
                return [f'background-color: {VAR_COR_DESTAQUE_LINHA_BG}; color: {VAR_COR_DESTAQUE_LINHA_TXT}; font-weight: bold'] * len(row)
            return [''] * len(row)

        # --- Cálculo de Métricas e Dicas (Movido para antes das abas) ---
        metric_data = []
        tips_automaticas = []

        for _, row_l in df_linhas.iterrows():
            nome_j = str(row_l.get('jogador', '')).strip()
            equipe_j_abrev = str(row_l.get('equipe', '')).strip()
            equipe_j_full = ABREV_PARA_FULL.get(equipe_j_abrev, equipe_j_abrev)
            detalhe = str(row_l.get('detalhe', '')).strip()
            
            # Filtro Casa/Fora baseado na coluna 'casa' do linhas.csv
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

            # Exibe somente jogadores que tem valores na planilha de linhas preenchidos (pelo menos uma linha > 0)
            if (pd.isna(v_pts) or v_pts <= 0) and (pd.isna(v_rbt) or v_rbt <= 0) and (pd.isna(v_pr) or v_pr <= 0):
                continue

            df_j_metric = df_completo[df_completo['Nome_Full'].str.contains(nome_j, case=False, na=False)].copy()
            
            if not df_j_metric.empty:
                # Filtra pelo jogador selecionado no sidebar, se houver
                if tem_jogador and jogador_selecionado not in df_j_metric['Nome_Full'].unique():
                    continue

                # Aplica filtros de contexto
                if st.session_state.filtro_local == "Casa": df_j_metric = df_j_metric[df_j_metric['Casa'] == 1]
                elif st.session_state.filtro_local == "Fora": df_j_metric = df_j_metric[df_j_metric['Casa'] == 0]
                
                df_j_metric = df_j_metric.sort_values(by='Data_Hora_Jogo', ascending=False)
                if periodo_selecionado == "Últimos 5": df_j_metric = df_j_metric.head(5)
                elif periodo_selecionado == "Últimos 10": df_j_metric = df_j_metric.head(10)

                total = len(df_j_metric)
                if total > 0:
                    # Garante que as colunas de estatísticas sejam numéricas e sem NaN
                    for col in ['Pontos', 'Rebotes', 'Assistencias', 'blocks', 'steals', 'turnovers']:
                        if col in df_j_metric.columns:
                            df_j_metric[col] = pd.to_numeric(df_j_metric[col], errors='coerce').fillna(0)
                    
                    df_j_metric['P+R'] = df_j_metric['Pontos'] + df_j_metric['Rebotes']
                    
                    # Mins
                    mins = df_j_metric[['Pontos', 'Rebotes', 'P+R']].min()

                    # ... (Lógica de cálculo de confiança mantida simplificada aqui para brevidade, mas o código original já faz isso) ...
                    # Recalculando confiança para garantir variáveis
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

                    p_pts = (len(df_j_metric[df_j_metric['Pontos'] > v_pts]) / total * 100) if not pd.isna(v_pts) else 0
                    p_rbt = (len(df_j_metric[df_j_metric['Rebotes'] > v_rbt]) / total * 100) if not pd.isna(v_rbt) else 0
                    p_pr = (len(df_j_metric[df_j_metric['P+R'] > v_pr]) / total * 100) if v_pr > 0 and not pd.isna(v_pr) else 0

                    metric_data.append({
                        "EQUIPE": equipe_j_full, "JOGADOR": nome_j, 
                        "L_PTS": int(v_pts) if not pd.isna(v_pts) else 0, "MIN PTS": int(mins['Pontos']), "CONF PTS": int(conf_pts), "PTS %": f"{p_pts:.0f}%",
                        "L_REB": int(v_rbt) if not pd.isna(v_rbt) else 0, "MIN REB": int(mins['Rebotes']), "CONF REB": int(conf_reb), "REB %": f"{p_rbt:.0f}%",
                        "L_PR": int(v_pr) if not pd.isna(v_pr) else 0, "MIN PR": int(mins['P+R']), "CONF PR": int(conf_pr), "PR %": f"{p_pr:.0f}%",
                        "DETALHE": detalhe
                    })

        if metric_data:
            df_consolidado_dicas = pd.DataFrame(metric_data)
        else:
            df_consolidado_dicas = pd.DataFrame()

        # --- Abas de Conteúdo ---
        tab_analise, tab_h2h, tab_linhas, tab_tips = st.tabs([
            "  📊 ANÁLISE INDIVIDUAL  ",
            "  🆚 H2H PLAYER  ",
            "  📈 INSIGHTS DE LINHAS  ",
            "   TIPS DO DIA 💰  "
        ])

        with tab_analise:
            if not tem_jogador:
                st.info("👆 Selecione um jogador no menu lateral para visualizar as estatísticas individuais.")
            elif df_filtrado.empty:
                st.warning("Nenhum dado encontrado para este jogador com os filtros atuais.")
            else:
                st.subheader("Estatísticas do Jogador")
                
                # Variável independente para esta tela para evitar conflitos
                df_stats_indiv = df_filtrado.copy()
                
                # Tratamento da coluna Local para exibição
                df_stats_indiv['LOCAL_DISPLAY'] = df_stats_indiv['Casa'].apply(lambda x: "Casa" if x == 1 else "Fora")
                
                # Mapeamento de colunas conforme solicitado
                colunas_tabela = {
                    "Pontos": "PTS", "Rebotes": "REB", "Assistencias": "AST",
                    "3PTS_Feitos": "3PM", "Tocos": "BLK", "Roubos de bola": "STL",
                    "Erros / Perdas de posse": "TOV", "Minutos": "MIN", "Data_Limpa": "DATA",
                    "LOCAL_DISPLAY": "LOCAL", "Opp_Full": "OPONENTE"
                }
                
                # Seleciona apenas as colunas que existem e renomeia
                cols_final = [c for c in colunas_tabela.keys() if c in df_stats_indiv.columns]
                st.dataframe(
                    df_stats_indiv[cols_final].rename(columns=colunas_tabela),
                    hide_index=True,
                    use_container_width=True
                )
                
                st.markdown("""
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">🏀 <b>PTS</b>: Pontos</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">🖐️ <b>REB</b>: Rebotes</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">🤝 <b>AST</b>: Assistências</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">⏱️ <b>MIN</b>: Minutos</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">👌 <b>3PM</b>: 3 Pontos</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">🚫 <b>BLK</b>: Tocos</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">🔒 <b>STL</b>: Roubos</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">⚠️ <b>TOV</b>: Erros</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">📅 <b>DATA</b>: Dia</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">📍 <b>LOCAL</b>: Casa/Fora</span>
                    <span style="background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; color: #31333F;">🆚 <b>OPP</b>: Adversário</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("MMM (Mediana / Mínimo / Máximo)")
                
                cols_mmm = ['Pontos', 'Rebotes', 'Assistencias', '3PTS_Feitos', 'Tocos', 'Roubos de bola', 'Erros / Perdas de posse']
                rename_mmm = {
                    'Pontos': 'PTS', 'Rebotes': 'REB', 'Assistencias': 'AST', 
                    '3PTS_Feitos': '3PM', 'Tocos': 'BLK', 'Roubos de bola': 'STL', 
                    'Erros / Perdas de posse': 'TOV'
                }
                
                cols_existentes = [c for c in cols_mmm if c in df_stats_indiv.columns]
                if cols_existentes:
                    df_mmm = df_stats_indiv[cols_existentes].agg(['median', 'min', 'max'])
                    df_mmm.index = ['Mediana', 'Mínimo', 'Máximo']
                    st.dataframe(df_mmm.rename(columns=rename_mmm), use_container_width=True)
                
                st.markdown("""
                <small>
                <b>Legenda MMM:</b><br>
                • <b>Mediana:</b> Mostra a mediana marcada pelo jogador nas partidas selecionadas.<br>
                • <b>Mínimo:</b> Mostra o mínimo marcado pelo jogador nas partidas selecionadas.<br>
                • <b>Máximo:</b> Mostra o máximo marcado pelo jogador nas partidas selecionadas.
                </small>
                """, unsafe_allow_html=True)

        with tab_h2h:
            if not tem_jogador:
                st.info("👆 Selecione um jogador no menu lateral.")
            elif opp_selecionado == "Selecione..." or opp_selecionado is None:
                st.info("👆 Selecione um oponente no menu lateral para ver o histórico H2H.")
            else:
                # Filtrar jogos contra o oponente (usando df_principal que já é do jogador)
                df_h2h = df_principal[df_principal['Opp_Full'] == opp_selecionado].copy()
                
                if df_h2h.empty:
                    st.warning(f"Nenhum jogo encontrado de {jogador_selecionado} contra {opp_selecionado} na base de dados.")
                else:
                    st.subheader(f"Histórico: {jogador_selecionado} vs {opp_selecionado}")
                    st.markdown(f"**Total de Jogos:** {len(df_h2h)}")
                    
                    # 1. Tabela Detalhada
                    colunas_h2h = {
                        "Pontos": "PTS", "Rebotes": "REB", "Assistencias": "AST",
                        "3PTS_Feitos": "3PM", "Tocos": "BLK", "Roubos de bola": "STL",
                        "Erros / Perdas de posse": "TOV", "Data_Limpa": "DATA",
                        "LOCAL_DISPLAY": "LOCAL", "Opp_Full": "OPONENTE"
                    }
                    # Preparar Local
                    df_h2h['LOCAL_DISPLAY'] = df_h2h['Casa'].apply(lambda x: "Casa" if x == 1 else "Fora")
                    
                    cols_show = [c for c in colunas_h2h.keys() if c in df_h2h.columns]
                    st.dataframe(
                        df_h2h[cols_show].rename(columns=colunas_h2h),
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # 2. Resumo MMM
                    st.markdown("##### Resumo de Desempenho (H2H)")
                    cols_mmm = ['Pontos', 'Rebotes', 'Assistencias', '3PTS_Feitos', 'Tocos', 'Roubos de bola', 'Erros / Perdas de posse']
                    rename_mmm = {
                        'Pontos': 'PTS', 'Rebotes': 'REB', 'Assistencias': 'AST', 
                        '3PTS_Feitos': '3PM', 'Tocos': 'BLK', 'Roubos de bola': 'STL', 
                        'Erros / Perdas de posse': 'TOV'
                    }
                    cols_existentes = [c for c in cols_mmm if c in df_h2h.columns]
                    if cols_existentes:
                        df_mmm_h2h = df_h2h[cols_existentes].agg(['median', 'min', 'max'])
                        df_mmm_h2h.index = ['Mediana', 'Mínimo', 'Máximo']
                        st.dataframe(df_mmm_h2h.rename(columns=rename_mmm), use_container_width=True)
                    
                    st.markdown("---")
                    
                    # 3. Análise Preditiva e Defensive Gaps
                    st.subheader("🔮 Análise de Confronto & Previsão")
                    
                    posicao = df_principal['Posicao_Jogador'].iloc[0] if 'Posicao_Jogador' in df_principal.columns else "N/A"
                    
                    # Defensive Gaps (Oponente vs Posição)
                    df_opp_defense = df_completo[df_completo['Opp_Full'] == opp_selecionado]
                    
                    if not df_opp_defense.empty and posicao != "N/A":
                        # Tenta match da posição
                        mask_pos = df_opp_defense['Posicao_Jogador'].astype(str).str.contains(posicao, na=False, regex=False)
                        if not mask_pos.any():
                             # Fallback se não achar exato, pega geral
                             stats_allowed = df_opp_defense[['Pontos', 'Rebotes', 'Assistencias']].mean()
                             pos_label = "Geral (Time)"
                        else:
                             stats_allowed = df_opp_defense[mask_pos][['Pontos', 'Rebotes', 'Assistencias']].mean()
                             pos_label = posicao
                        
                        player_med = df_principal[['Pontos', 'Rebotes', 'Assistencias']].median()
                        h2h_med = df_h2h[['Pontos', 'Rebotes', 'Assistencias']].median()
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric(f"Média Cedida ({pos_label})", f"{stats_allowed['Pontos']:.1f} PTS")
                        c2.metric(f"Mediana Jogador (Season)", f"{player_med['Pontos']:.1f} PTS")
                        c3.metric(f"Mediana H2H", f"{h2h_med['Pontos']:.1f} PTS")
                        
                        analise_texto = f"**Leitura de Jogo para {jogador_selecionado} ({posicao}):**\n\n"
                        analise_texto += f"O **{opp_selecionado}** tem uma defesa que permite, em média, **{stats_allowed['Pontos']:.1f} pontos**, **{stats_allowed['Rebotes']:.1f} rebotes** e **{stats_allowed['Assistencias']:.1f} assistências** para jogadores da posição **{posicao}**.\n\n"
                        
                        analise_texto += "**Comparativo:**\n"
                        diff_pts = stats_allowed['Pontos'] - player_med['Pontos']
                        if diff_pts > 2:
                            analise_texto += f"- 🔥 **Ataque vs Defesa:** O oponente cede **{diff_pts:.1f}** pontos ACIMA da média do jogador. Isso indica um *matchup* muito favorável.\n"
                        elif diff_pts < -2:
                            analise_texto += f"- 🛡️ **Ataque vs Defesa:** O oponente cede **{abs(diff_pts):.1f}** pontos ABAIXO da média do jogador. Defesa difícil.\n"
                        else:
                            analise_texto += f"- ⚖️ **Ataque vs Defesa:** O confronto é equilibrado estatisticamente.\n"
                            
                        if h2h_med['Pontos'] > player_med['Pontos']:
                            analise_texto += f"- 📈 **Histórico:** O jogador costuma pontuar MAIS contra este time ({h2h_med['Pontos']:.1f}) do que sua média geral.\n"
                        
                        st.info(analise_texto)
                    else:
                        st.warning("Dados insuficientes de posição ou defesa do oponente para gerar previsão detalhada.")

        with tab_linhas:
            if df_consolidado_dicas.empty:
                st.info("Nenhuma linha encontrada para os filtros selecionados.")
            else:
                st.subheader("Piso x Linhas (Análise de Confiança)")
                
                # Mapeamento e Renomeação de Colunas
                cols_map = {
                    "EQUIPE": "Equipe", "JOGADOR": "Jogador",
                    "L_PTS": "Line PTS", "MIN PTS": "Min PTS", "CONF PTS": "Conf PTS %", "PTS %": "Hit PTS %",
                    "L_REB": "Line REB", "MIN REB": "Min REB", "CONF REB": "Conf REB %", "REB %": "Hit REB %",
                    "L_PR": "Line PR", "MIN PR": "Min PR", "CONF PR": "Conf PR %", "PR %": "Hit PR %"
                }
                
                # Seleciona apenas colunas existentes e renomeia
                cols_to_show = [c for c in cols_map.keys() if c in df_consolidado_dicas.columns]
                df_show = df_consolidado_dicas[cols_to_show].rename(columns=cols_map)
                
                st.dataframe(df_show, hide_index=True, use_container_width=True)
                
                st.markdown("""
                <small>
                <b>Legenda:</b><br>
                • <b>Line:</b> Linha da casa de apostas.<br>
                • <b>Min:</b> Mínimo estatístico do jogador no período selecionado.<br>
                • <b>Conf %:</b> (Mínimo / Linha) * 100. Indica a segurança do piso em relação à linha.<br>
                • <b>Hit %:</b> Porcentagem de jogos no período em que o jogador bateu (superou) a linha.
                </small>
                """, unsafe_allow_html=True)

        with tab_tips:
            if df_consolidado_dicas.empty:
                st.info("Nenhuma tip disponível. Ajuste os filtros ou verifique se há linhas disponíveis.")
            else:
                tips_data = []
                
                # Itera sobre os dados consolidados para aplicar os filtros de Tips
                for _, row in df_consolidado_dicas.iterrows():
                    try:
                        # Converte Hit Rate para inteiro
                        hit_pts = int(str(row['PTS %']).replace('%', ''))
                        hit_reb = int(str(row['REB %']).replace('%', ''))
                        hit_pr = int(str(row['PR %']).replace('%', ''))
                    except:
                        continue
                    
                    conf_pts = row['CONF PTS']
                    conf_reb = row['CONF REB']
                    conf_pr = row['CONF PR']
                    
                    best_market = None
                    best_power = -1
                    
                    # Verifica critérios: Conf >= 70% E Hit >= 60%
                    # Mercado Pontos
                    if conf_pts >= 70 and hit_pts >= 60:
                        power = (conf_pts + hit_pts) / 2
                        if power > best_power:
                            best_power = power
                            best_market = "PTS"
                            
                    # Mercado Rebotes
                    if conf_reb >= 70 and hit_reb >= 60:
                        power = (conf_reb + hit_reb) / 2
                        if power > best_power:
                            best_power = power
                            best_market = "REB"
                            
                    # Mercado P+R
                    if conf_pr >= 70 and hit_pr >= 60:
                        power = (conf_pr + hit_pr) / 2
                        if power > best_power:
                            best_power = power
                            best_market = "PR"
                    
                    if best_market:
                        # Adiciona à lista final
                        tips_data.append({
                            "JOGADOR": row['JOGADOR'],
                            "EQUIPE": row['EQUIPE'],
                            "MERCADO": best_market,
                            "CONF PTS": f"{conf_pts}%", "HIT PTS": f"{hit_pts}%",
                            "CONF REB": f"{conf_reb}%", "HIT REB": f"{hit_reb}%",
                            "CONF PR": f"{conf_pr}%", "HIT PR": f"{hit_pr}%",
                            "POWER": int(best_power),
                            "_sort": best_power
                        })
                
                if tips_data:
                    df_tips = pd.DataFrame(tips_data).sort_values(by='_sort', ascending=False).drop(columns=['_sort'])
                    
                    st.subheader("🔥 Melhores Oportunidades (Power >= 65%)")
                    st.dataframe(
                        df_tips,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "POWER": st.column_config.ProgressColumn(
                                "Força (Power)",
                                help="Média entre Confiança e Hit Rate",
                                format="%d%%",
                                min_value=0,
                                max_value=100,
                            ),
                        }
                    )
                else:
                    st.info("Nenhum jogador atende aos critérios de Tips (Conf >= 70% e Hit >= 60%) nos filtros selecionados.")