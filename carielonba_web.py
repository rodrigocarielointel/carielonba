import streamlit as st
import pandas as pd
import os
from PIL import Image

# --- Configuração da Página ---
st.set_page_config(
    page_title="Carielo NBA Scouts",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS (Opcional, para refinamento) ---
st.markdown("""
    <style>
        .stExpander {
            border: 1px solid #e0e0e0 !important;
            border-radius: 5px;
        }
        .stMetric {
            border-left: 5px solid #1D428A;
            padding-left: 10px;
            border-radius: 5px;
            background-color: #f8f9fa;
        }
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
    path_base = "." # Assume que os arquivos estão na mesma pasta do script
    
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

# --- Inicialização do Estado da Sessão ---
if 'filtro_local' not in st.session_state:
    st.session_state.filtro_local = "Geral"

# --- Funções de Lógica ---
def get_player_photo_path(nome_jogador):
    path_foto = None
    path_assets_players = os.path.join("assets", "players")

    if df_players_images is not None and 'Nome_Full' in df_players_images.columns:
        match = df_players_images[df_players_images['Nome_Full'].str.lower() == nome_jogador.lower()]
        if not match.empty:
            rel_path = match.iloc[0].get('image_path')
            if pd.notna(rel_path):
                str_path = str(rel_path).replace("/", os.sep)
                path_foto = os.path.join(str_path) # Caminho relativo direto

    if not path_foto or not os.path.exists(path_foto):
        path_foto = os.path.join(path_assets_players, f"{nome_jogador}.png")

    if os.path.exists(path_foto):
        return path_foto
    
    # Fallback para imagem padrão
    return os.path.join("assets", "perfiljogador.png")


# =================================================================
# INTERFACE DO USUÁRIO (UI)
# =================================================================

# --- Barra Lateral (Sidebar) para Filtros ---
with st.sidebar:
    if os.path.exists("assets/logos/logo.png"):
        st.image("assets/logos/logo.png", width=70)
    st.title("Filtros de Análise")

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

    st.divider()

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

    st.divider()
    if st.button("🔄 Limpar Filtros"):
        st.session_state.combo_eq = "Selecione a Equipe..."
        st.session_state.combo_jog = "Selecione o Jogador..."
        st.session_state.combo_opp = "Selecione..."
        st.rerun()

# --- Área Principal ---
st.title("Carielo NBA Scouts 🏀")

if jogador_selecionado == "Selecione o Jogador...":
    st.info("Selecione uma equipe e um jogador na barra lateral para iniciar a análise.")
    st.stop()

# --- Lógica de Filtragem Principal ---
df_jogador = df_completo[df_completo['Nome_Full'] == jogador_selecionado].copy()
df_jogador = df_jogador.sort_values(by='Data_Hora_Jogo', ascending=False)

for c in ['Pontos', 'Rebotes', 'Assistencias', '3PTS_Feitos', 'Minutos']:
    df_jogador[c] = pd.to_numeric(df_jogador[c], errors='coerce').fillna(0)

df_jogador['PR'] = df_jogador['Pontos'] + df_jogador['Rebotes']
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


# --- Abas de Conteúdo ---
tab_analise, tab_metricas, tab_tips = st.tabs([
    "  📊 ANÁLISE INDIVIDUAL  ",
    "  📈 MÉTRICAS DA EQUIPE (CSV)  ",
    "  💰 TIPS DO DIA 💰  "
])


with tab_analise:
    col_perfil, col_tabela, col_confronto = st.columns([1, 2, 1.2])

    # --- Coluna da Esquerda: Perfil e Insights ---
    with col_perfil:
        st.subheader("Perfil do Jogador")
        
        # Card do Perfil
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            path_foto = get_player_photo_path(jogador_selecionado)
            if os.path.exists(path_foto):
                c1.image(path_foto, width=100)
            
            posicao = df_jogador['Posicao_Jogador'].iloc[0] if 'Posicao_Jogador' in df_jogador.columns and not df_jogador.empty else "N/A"
            c2.markdown(f"**{jogador_selecionado.upper()}**")
            c2.caption(f"Posição: {posicao}")

        st.subheader("Insights Rápidos")
        map_func = [("MEDIANA", "median"), ("MÉDIA", "mean"), ("MÍNIMO", "min"), ("MÁXIMO", "max")]
        cols_nba = {"MIN": "Minutos", "PTS": "Pontos", "REB": "Rebotes", "P+R": "PR", "AST": "Assistencias", "3P": "3PTS_Feitos"}

        for titulo, func in map_func:
            with st.expander(f"📊 {titulo}", expanded=(titulo == "MEDIANA")):
                cols = st.columns(len(cols_nba))
                for i, (label, col_csv) in enumerate(cols_nba.items()):
                    val = getattr(df_filtrado[col_csv], func)() if not df_filtrado.empty else 0
                    formatted_val = f"{val:.1f}" if func in ["mean", "median"] else f"{int(val)}"
                    cols[i].metric(label, formatted_val)

        # Seção da Linha da Bet
        st.subheader("🎯 Linha da Bet")
        with st.container(border=True):
            bet_cols = st.columns(5)
            bet_inputs = {}
            bet_labels = ["PTS", "REB", "P+R", "AST", "3P"]
            bet_keys = ["pts", "reb", "pr", "ast", "3p"]

            # Preencher com dados do linhas.csv
            linha_jogador_df = df_linhas[df_linhas['jogador'].str.contains(jogador_selecionado, case=False, na=False)]
            
            for i, (label, key) in enumerate(zip(bet_labels, bet_keys)):
                default_val = ""
                if not linha_jogador_df.empty and key in linha_jogador_df.columns:
                    default_val = linha_jogador_df.iloc[0][key]
                bet_inputs[key] = bet_cols[i].text_input(label, value=default_val, key=f"bet_{key}")

    # --- Coluna Central: Tabela de Jogos ---
    with col_tabela:
        st.subheader("Histórico de Jogos")
        
        df_display = df_filtrado.copy()
        df_display['LOCAL'] = df_display['Casa'].apply(lambda x: "Casa" if x == 1 else "Fora")
        
        colunas_tabela = {
            "Data_Limpa": "DATA", "LOCAL": "LOCAL", "Opp_Full": "OPONENTE",
            "Minutos": "MIN", "Pontos": "PTS", "Rebotes": "REB", "PR": "P+R",
            "Assistencias": "AST", "3PTS_Feitos": "3PTS"
        }
        
        st.dataframe(
            df_display[list(colunas_tabela.keys())].rename(columns=colunas_tabela),
            hide_index=True,
            use_container_width=True
        )

    # --- Coluna da Direita: Análise de Confronto ---
    with col_confronto:
        st.subheader("Análise de Confronto")

        # H2H e Projeção
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Head-to-Head (H2H)**")
                if opp_selecionado != "Selecione...":
                    df_h2h = df_jogador[df_jogador['Opp_Full'] == opp_selecionado]
                    if not df_h2h.empty:
                        mean_h2h = df_h2h[['Pontos', 'Rebotes', 'PR']].mean()
                        st.markdown(f"Jogos: **{len(df_h2h)}**")
                        st.markdown(f"PTS: **{mean_h2h['Pontos']:.1f}** | REB: **{mean_h2h['Rebotes']:.1f}**")
                    else:
                        st.warning("Sem histórico")
                else:
                    st.info("Selecione um adversário")
        with c2:
            with st.container(border=True):
                st.markdown("**Projeção vs Linha**")
                # Lógica de projeção e comparação com a linha da bet
                # (Simplificado para demonstração)
                if not df_filtrado.empty:
                    median_geral = df_filtrado[['Pontos', 'Rebotes', 'PR']].median()
                    try:
                        linha_pts = float(bet_inputs['pts']) if bet_inputs['pts'] else 0
                        diff = median_geral['Pontos'] - linha_pts
                        if diff > 0.5: st.success(f"OVER PTS ({diff:+.1f})")
                        elif diff < -0.5: st.error(f"UNDER PTS ({diff:+.1f})")
                        else: st.warning("Linha Justa")
                    except (ValueError, KeyError):
                        st.write("...")
                else:
                    st.write("...")

        # Defensive Gaps
        st.markdown("**Defensive Gaps do Adversário**")
        if opp_selecionado != "Selecione...":
            df_opp_sofre = df_completo[df_completo['Opp_Full'] == opp_selecionado].copy()
            if not df_opp_sofre.empty and 'Posicao_Jogador' in df_opp_sofre.columns:
                stats_pos = df_opp_sofre.groupby('Posicao_Jogador')[['Pontos', 'Rebotes', '3PTS_Feitos']].mean().sort_values(by='Pontos', ascending=False).head(3)
                stats_pos = stats_pos.reset_index().rename(columns={"Posicao_Jogador": "POS", "Pontos": "PTS", "Rebotes": "REB", "3PTS_Feitos": "3PTS"})
                st.dataframe(stats_pos, hide_index=True, use_container_width=True)
        else:
            st.info("Selecione um adversário para ver os gaps.")


with tab_metricas:
    st.header("🎯 Métricas Automáticas (via linhas.csv)")
    st.caption(f"Análise baseada no contexto: **{st.session_state.filtro_local}** | Período: **{periodo_selecionado}**")

    metric_data = []
    for _, row_l in df_linhas.iterrows():
        nome_j = str(row_l.get('jogador', '')).strip()
        equipe_j_abrev = str(row_l.get('equipe', '')).strip()
        equipe_j_full = ABREV_PARA_FULL.get(equipe_j_abrev, equipe_j_abrev)
        detalhe = str(row_l.get('detalhe', '')).strip()

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
                df_j_metric['PR'] = df_j_metric['Pontos'].fillna(0) + df_j_metric['Rebotes'].fillna(0)
                p_pts = (len(df_j_metric[df_j_metric['Pontos'] > v_pts]) / total * 100)
                p_rbt = (len(df_j_metric[df_j_metric['Rebotes'] > v_rbt]) / total * 100)
                p_pr = (len(df_j_metric[df_j_metric['PR'] > v_pr]) / total * 100) if v_pr > 0 else 0

                metric_data.append({
                    "EQUIPE": equipe_j_full, "JOGADOR": nome_j, "L_PTS": v_pts, "L_REB": v_rbt, "L_PR": v_pr,
                    "PTS %": f"{p_pts:.0f}%", "REB %": f"{p_rbt:.0f}%", "PR %": f"{p_pr:.0f}%", "DETALHE": detalhe
                })

    if metric_data:
        df_metricas_display = pd.DataFrame(metric_data)
        st.dataframe(df_metricas_display, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma métrica encontrada para os filtros atuais.")

with tab_tips:
    st.header("🔥 Consolidado de Dicas de Apostas")
    st.info("Esta seção é um exemplo e pode ser desenvolvida para consolidar dicas manuais e automáticas.")
    
    if 'tips' not in st.session_state:
        st.session_state.tips = []

    # Exemplo de como adicionar uma dica (a lógica completa pode ser implementada aqui)
    # if st.button("Adicionar Dica de Exemplo"):
    #     st.session_state.tips.append({"Jogador": jogador_selecionado, "Mercado": "Pontos OVER", "Linha": 25.5})

    if st.session_state.tips:
        st.dataframe(pd.DataFrame(st.session_state.tips), use_container_width=True, hide_index=True)
    else:
        st.write("Nenhuma dica adicionada ainda.")