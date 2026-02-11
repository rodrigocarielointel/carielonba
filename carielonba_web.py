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
        /* Reduzir espaçamento no sidebar */
        [data-testid="stSidebar"] .stElementContainer {
            margin-bottom: -10px;
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

with col_main:
    st.markdown("### Carielo NBA Scouts 🏀")

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
                mean_h2h = df_h2h[['Pontos', 'Rebotes', 'Assistencias', 'PR']].mean()
                st.markdown(f"Jogos: **{len(df_h2h)}**")
                st.markdown(f"PTS: **{mean_h2h['Pontos']:.1f}** | REB: **{mean_h2h['Rebotes']:.1f}** | AST: **{mean_h2h['Assistencias']:.1f}**")
            else:
                st.warning("Sem histórico")
        else:
            st.info("Selecione adversário")

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

    # 2. Linha da Bet
    with st.container(border=True):
        st.markdown("**🎯 Linha da Bet**")
        bet_cols = st.columns(5) # Lado a lado
        bet_inputs = {}
        bet_labels = ["PTS", "REB", "AST", "P+R", "3P"] # Reorganizado para fluir melhor
        bet_keys = ["pts", "reb", "ast", "pr", "3p"]

        linha_jogador_df = df_linhas[df_linhas['jogador'].str.contains(jogador_selecionado, case=False, na=False)]
        
        for i, (label, key) in enumerate(zip(bet_labels, bet_keys)):
            default_val = ""
            if not linha_jogador_df.empty and key in linha_jogador_df.columns:
                default_val = linha_jogador_df.iloc[0][key]
            
            col = bet_cols[i]
            
            bet_inputs[key] = col.text_input(label, value=default_val, key=f"bet_{key}")

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
                "Pontos": "PTS", "Rebotes": "REB", "PR": "P+R",
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
            
            cols_nba = {"MIN": "Minutos", "PTS": "Pontos", "REB": "Rebotes", "P+R": "PR", "AST": "Assistencias", "3P": "3PTS_Feitos"}
            stats = df_filtrado[list(cols_nba.values())].agg(['median', 'mean', 'min', 'max'])
            stats.columns = list(cols_nba.keys())
            stats.index = ["Mediana", "Média", "Mínimo", "Máximo"]
            st.dataframe(stats.style.format("{:.1f}"), use_container_width=True)

    with tab_linhas:
        st.header("🎯 Insights de Linhas (via linhas.csv)")
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

    with tab_mediana:
        st.header("📊 Insights de Mediana (Tendência)")
        st.caption(f"Jogadores com ≥ 50% de jogos acima da mediana da temporada nos {periodo_selecionado}.")
        
        if equipe_selecionada != "Selecione a Equipe...":
            players_to_scan = df_completo[df_completo['Time_Full'] == equipe_selecionada]['Nome_Full'].unique()
        else:
            players_to_scan = df_completo['Nome_Full'].unique()
            
        data_mediana = []
        data_consistencia = []
        
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

            df_p['PR'] = df_p['Pontos'] + df_p['Rebotes']
            medians = df_p[['Pontos', 'Rebotes', 'Assistencias', 'PR']].median()
            
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
            pct_pr = (len(df_p_period[df_p_period['PR'] > medians['PR']]) / total_games) * 100
            
            if pct_pts >= 50 or pct_reb >= 50 or pct_ast >= 50 or pct_pr >= 50:
                data_mediana.append({
                    "JOGADOR": player,
                    "MED PTS": medians['Pontos'], "% PTS": f"{pct_pts:.0f}%",
                    "MED REB": medians['Rebotes'], "% REB": f"{pct_reb:.0f}%",
                    "MED AST": medians['Assistencias'], "% AST": f"{pct_ast:.0f}%",
                    "MED P+R": medians['PR'], "% P+R": f"{pct_pr:.0f}%"
                })
            
            # --- Lógica 2: Consistência (Mínimo vs Mediana) ---
            mins = df_p_period[['Pontos', 'Rebotes', 'Assistencias', 'PR']].min()
            
            def calc_conf(min_val, med_val):
                if med_val == 0: return 0.0
                return (min_val / med_val) * 100

            conf_pts = calc_conf(mins['Pontos'], medians['Pontos'])
            conf_reb = calc_conf(mins['Rebotes'], medians['Rebotes'])
            conf_ast = calc_conf(mins['Assistencias'], medians['Assistencias'])
            conf_pr = calc_conf(mins['PR'], medians['PR'])

            data_consistencia.append({
                "JOGADOR": player,
                "MED PTS": medians['Pontos'], "MIN PTS": mins['Pontos'], "CONF PTS": conf_pts,
                "MED REB": medians['Rebotes'], "MIN REB": mins['Rebotes'], "CONF REB": conf_reb,
                "MED AST": medians['Assistencias'], "MIN AST": mins['Assistencias'], "CONF AST": conf_ast,
                "MED P+R": medians['PR'], "MIN P+R": mins['PR'], "CONF P+R": conf_pr
            })
                
        if data_mediana:
            st.dataframe(pd.DataFrame(data_mediana), use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum jogador encontrado com os critérios.")
            
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
            cols_order = ["JOGADOR", 
                          "MED PTS", "MIN PTS", "CONF PTS", 
                          "MED REB", "MIN REB", "CONF REB",
                          "MED AST", "MIN AST", "CONF AST",
                          "MED P+R", "MIN P+R", "CONF P+R"]
            cols_final = [c for c in cols_order if c in df_consist.columns]
            st.dataframe(df_consist[cols_final], 
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