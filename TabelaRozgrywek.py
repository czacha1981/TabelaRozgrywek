import streamlit as st
import pandas as pd
import os

# Plik do zapisu danych
DATA_FILE = "matches.csv"

# Funkcja do wczytywania danych
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict(orient="records")
    return []

# Funkcja do zapisu danych
def save_data():
    df = pd.DataFrame(st.session_state.matches)
    df.to_csv(DATA_FILE, index=False)

# Inicjalizacja zmiennych
if "matches" not in st.session_state:
    st.session_state.matches = load_data()

if "players" not in st.session_state:
    st.session_state.players = ["Adam", "Sylwek", "Bartek", "Piotrek"]

# Aktualizacja rankingu
def update_ranking():
    ranking = {player: {"Mecze": 0, "Wygrane": 0, "Przegrane": 0, "Remisy": 0, "Punkty": 0} for player in st.session_state.players}

    for match in st.session_state.matches:
        player1, player2, score1, score2 = match["Zawodnik 1"], match["Zawodnik 2"], match["Gole 1"], match["Gole 2"]
        ranking[player1]["Mecze"] += 1
        ranking[player2]["Mecze"] += 1

        if score1 > score2:
            ranking[player1]["Wygrane"] += 1
            ranking[player2]["Przegrane"] += 1
            ranking[player1]["Punkty"] += 3
        elif score2 > score1:
            ranking[player2]["Wygrane"] += 1
            ranking[player1]["Przegrane"] += 1
            ranking[player2]["Punkty"] += 3
        else:
            ranking[player1]["Remisy"] += 1
            ranking[player2]["Remisy"] += 1
            ranking[player1]["Punkty"] += 1
            ranking[player2]["Punkty"] += 1

    return pd.DataFrame(ranking).T.sort_values(by=["Punkty", "Wygrane"], ascending=False)

# Strona główna
st.title("🏆 Liga Piłkarzyków Stołowych")

# **Dodawanie meczu**
st.header("⚽ Dodaj wynik meczu")

col1, col2, col3, col4 = st.columns(4)
with col1:
    player1 = st.selectbox("Zawodnik 1", st.session_state.players)
with col2:
    score1 = st.number_input("Gole Zawodnik 1", min_value=0, step=1)
with col3:
    player2 = st.selectbox("Zawodnik 2", st.session_state.players, index=1)
with col4:
    score2 = st.number_input("Gole Zawodnik 2", min_value=0, step=1)

if st.button("📌 Zapisz wynik meczu"):
    if player1 != player2:
        st.session_state.matches.append({"Zawodnik 1": player1, "Gole 1": score1, "Zawodnik 2": player2, "Gole 2": score2})
        save_data()
        st.success(f"✅ Wynik zapisany: {player1} {score1} - {score2} {player2}")
    else:
        st.error("❌ Wybierz różnych zawodników!")

# **Tabela ligowa**
st.header("📊 Tabela ligowa")
df_ranking = update_ranking()
st.dataframe(df_ranking.style.format({"Mecze": "{:.0f}", "Wygrane": "{:.0f}", "Przegrane": "{:.0f}", "Remisy": "{:.0f}", "Punkty": "{:.0f}"}))

# **Historia meczów**
st.header("📜 Historia meczów")
if st.session_state.matches:
    df_matches = pd.DataFrame(st.session_state.matches)

    # Edytowanie meczów
    match_to_edit = st.selectbox("🔧 Wybierz mecz do edycji", df_matches.index.tolist(), format_func=lambda x: f"{df_matches.loc[x, 'Zawodnik 1']} {df_matches.loc[x, 'Gole 1']} - {df_matches.loc[x, 'Gole 2']} {df_matches.loc[x, 'Zawodnik 2']}" if not df_matches.empty else "Brak meczów")
    
    if match_to_edit is not None and not df_matches.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_score1 = st.number_input("Nowe gole Zawodnik 1", min_value=0, step=1, value=int(df_matches.loc[match_to_edit, "Gole 1"]))
        with col2:
            new_score2 = st.number_input("Nowe gole Zawodnik 2", min_value=0, step=1, value=int(df_matches.loc[match_to_edit, "Gole 2"]))
        with col3:
            if st.button("✏️ Zmień wynik"):
                st.session_state.matches[match_to_edit]["Gole 1"] = new_score1
                st.session_state.matches[match_to_edit]["Gole 2"] = new_score2
                save_data()
                st.success("✅ Wynik meczu zaktualizowany!")

    # Usuwanie meczu
    if st.button("🗑️ Usuń mecz"):
        if match_to_edit is not None:
            st.session_state.matches.pop(match_to_edit)
            save_data()
            st.success("✅ Mecz usunięty!")

    st.table(df_matches)
else:
    st.write("Brak rozegranych meczów.")

# **Dodawanie zawodników**
st.header("🧑‍🤝‍🧑 Zarządzanie zawodnikami")
new_player = st.text_input("Dodaj nowego zawodnika")

if st.button("➕ Dodaj zawodnika"):
    if new_player and new_player not in st.session_state.players:
        st.session_state.players.append(new_player)
        st.success(f"✅ {new_player} został dodany!")
    elif new_player in st.session_state.players:
        st.warning("⚠️ Ten zawodnik już istnieje!")
    else:
        st.error("❌ Podaj poprawne imię.")

# **Resetowanie danych**
if st.button("🗑️ Reset wyników"):
    st.session_state.matches = []
    save_data()
    st.success("✅ Wyniki zostały zresetowane!")
