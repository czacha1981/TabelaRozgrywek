import streamlit as st
import pandas as pd

# Inicjalizacja zmiennych sesji
if "matches" not in st.session_state:
    st.session_state.matches = []
if "players" not in st.session_state:
    st.session_state.players = ["Adam", "Sylwek", "Bartek", "Piotrek"]

# Funkcja do aktualizacji tabeli ligowej
def update_ranking():
    ranking = {player: {"Mecze": 0, "Wygrane": 0, "Przegrane": 0, "Remisy": 0, "Punkty": 0} for player in st.session_state.players}
    
    for match in st.session_state.matches:
        player1, player2, score1, score2 = match
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

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    player1 = st.selectbox("Zawodnik 1", st.session_state.players)
with col2:
    st.write("VS")
with col3:
    player2 = st.selectbox("Zawodnik 2", st.session_state.players, index=1)

if player1 == player2:
    st.warning("⚠️ Wybierz dwóch różnych zawodników!")

# **Suwaki do wyboru wyniku**
score1, score2 = st.slider("Wynik meczu", 0, 10, (0, 0))

if st.button("📌 Zapisz wynik meczu"):
    if player1 != player2:
        st.session_state.matches.append((player1, player2, score1, score2))
        st.success(f"✅ Wynik zapisany: {player1} {score1} - {score2} {player2}")
    else:
        st.error("❌ Wybierz różnych zawodników!")

# **Tabela ligowa**
st.header("📊 Tabela ligowa")
df_ranking = update_ranking()
st.dataframe(df_ranking.style.format({
    "Mecze": "{:.0f}", "Wygrane": "{:.0f}", "Przegrane": "{:.0f}", "Remisy": "{:.0f}", "Punkty": "{:.0f}"
}).applymap(lambda val: "background-color: #c7f9cc" if val > 0 else ""))

# **Historia meczów**
st.header("📜 Historia meczów")
if st.session_state.matches:
    df_matches = pd.DataFrame(st.session_state.matches, columns=["Zawodnik 1", "Zawodnik 2", "Gole 1", "Gole 2"])
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
    st.success("✅ Wyniki zostały zresetowane!")
    
