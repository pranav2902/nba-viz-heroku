import streamlit as st
import pandas as pd
import plotly.express as px

#DATA_URL = https://www.basketball-reference.com/leagues/NBA_2006_per_game.html

st.title('Basic NBA Visualizations')
@st.cache
def load_data(yr):
    playerpergame = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(str(yr)),header=0)
    playertotals = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_totals.html".format(str(yr)),header=0)
    #playeradvanced = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(str(yr)))
    #playershooting = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(str(yr)))
    (playerpergame, playertotals) = betterFiles(playertotals[0],playerpergame[0])
    playerpergame = playerpergame.drop(playerpergame[playerpergame.Age == "Age"].index)
    playertotals = playertotals.drop(playertotals[playertotals.Age == "Age"].index)
    return playerpergame, playertotals
@st.cache
def betterFiles(playertotals,playerpergame):
    indices = []
    for i in range(len(playertotals)):
        if(playertotals["Tm"][i] == "TOT"):
            indices.append(i)    
    playertotals = playertotals.drop(indices)
    playerpergame = playerpergame.drop(indices)
    #playeradvanced = playeradvanced.drop(indices)
    #playershooting = playershooting.drop(indices)
    return (playerpergame,playertotals)

year_options = list(range(1951,2022))
title = st.sidebar.title("Make a selection")
yr = st.sidebar.select_slider("Choose year",year_options,2021)
playerpergame,playertotals = load_data(yr)
player_options = playerpergame.Player.unique().tolist() 
pos_options = playerpergame.Pos.unique().tolist()
pl = st.sidebar.multiselect("Choose Players",player_options,player_options[0])
all_players = st.sidebar.checkbox("Select all players")
#https://discuss.streamlit.io/t/select-all-on-a-streamlit-multiselect/9799/2
if(all_players):
    pl = player_options
posits = playerpergame[playerpergame.Player.isin(pl)]["Pos"].unique().tolist()
pos = st.sidebar.multiselect("Choose Positions",pos_options,posits)
if(len(pl)):
    st.dataframe(playerpergame[playerpergame.Player.isin(pl)])
    fig = px.scatter(playerpergame[playerpergame["Player"].isin(pl)],x = "PTS",y = "eFG%",hover_name= "Player",range_x=[0,40],range_y=[0,1.2],color = "Tm")
    fig.update_layout(title = {'text' : "PPG vs eFG%", 'xanchor' : 'center', 'x' : 0.5}, yaxis=dict(
        autorange = True,
        type = "linear"
    ),xaxis = dict(
        autorange = True,
        type = "linear"
    ))
    st.plotly_chart(fig)

elif(len(pos)):
    st.dataframe(playerpergame[playerpergame.Pos.isin(pos)])
    fig = px.scatter(playerpergame[playerpergame["Pos"].isin(pos)],x = "PTS",y = "eFG%",hover_name= "Player",range_x=[0,40],range_y=[0,1.2],color = "Tm")
    fig.update_layout(title = {'text' : "PPG vs eFG%", 'xanchor' : 'center', 'x' : 0.5}, yaxis=dict(
        autorange = True,
        type = "linear"
    ),xaxis = dict(
        autorange = True,
        type = "linear"
    ))
    st.plotly_chart(fig)

#px.scatter()