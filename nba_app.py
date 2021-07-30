import streamlit as st
import pandas as pd
import plotly.express as px


#DATA_URL = https://www.basketball-reference.com/leagues/NBA_2006_per_game.html
## Things to do: Rename shooting df columns, add extra vizs. Make the logic for if else in pl and pos.
## Configure the sidebar selections better, i.e, if pl is selected how pos changes, if all players selected then unselected,how pos changes and graph changes, etc.
st.title('Basic NBA Visualizations')
@st.cache
def load_data(yr):
    playerpergame = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(str(yr)),header=None)
    playertotals = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_totals.html".format(str(yr)),header=None)
    playeradvanced = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(str(yr)),header = None)
    playershooting = pd.read_html("https://www.basketball-reference.com/leagues/NBA_{}_shooting.html".format(str(yr)),header = None)
    playerpergame = playerpergame[0]
    playertotals = playertotals[0]
    playeradvanced = playeradvanced[0]
    playershooting = playershooting[0]
    print(playeradvanced.columns.nlevels,playershooting.columns.nlevels)
    if(playershooting.columns.nlevels > 1):
        playershooting.columns = playershooting.columns.droplevel(0)
    unwanted1 = ["Unnamed: 9_level_1","Unnamed: 16_level_1","Unnamed: 23_level_1","Unnamed: 26_level_1","Unnamed: 29_level_1","Unnamed: 32_level_1"]
    unwanted2 = ["Unnamed: 19","Unnamed: 24"]
    #playershooting = playershooting.drop()
    if(len(playershooting.columns) > 30):
        playershooting = playershooting.drop(unwanted1,axis = 1)
        playeradvanced = playeradvanced.drop(unwanted2,axis = 1)
    #print(playershooting.head())
    #print(playeradvanced.head())
    #print(playertotals.head())
    #print(playerpergame.head())
    #print(len(playeradvanced),len(playerpergame),len(playershooting),len(playertotals))
    if(len(playerpergame[playerpergame.Age == "Age"]) != 0):
        playerpergame = playerpergame.drop(playerpergame[playerpergame.Age == "Age"].index)
        playertotals = playertotals.drop(playertotals[playertotals.Age == "Age"].index)
        playershooting = playershooting.drop(playershooting[playershooting.Age == "Age"].index)
        playeradvanced = playeradvanced.drop(playeradvanced[playeradvanced.Age == "Age"].index)
    #print(len(playeradvanced),len(playerpergame),len(playershooting),len(playertotals))
    playershooting.columns = ['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'FG%', 'Dist.', '% of FG 2P ft',
       '% of FG 0-3 ft', '% of FG 3-10 ft', '% of FG 10-16 ft', '% of FG 16-3P', '% of FG 3P', 'FG% 2P', 'FG%  0-3 ft', 'FG% 3-10 ft', 'FG% 10-16 ft',
       'FG% 16-3P', 'FG% 3P', 'Asst 2P', 'Asst 3P', '%FGA Dunks', '# Dunks', '%3PA Corner', '3P% Corner', 'Att. Heaves', '# Heaves']
    (playerpergame, playertotals, playeradvanced, playershooting) = betterFiles(playerpergame,playertotals,playeradvanced,playershooting)
    return playerpergame, playertotals,playeradvanced,playershooting
#@st.cache
def betterFiles(playerpergame,playertotals,playeradvanced,playershooting):
    indices = []
    #print(len(playeradvanced),len(playerpergame),len(playershooting),len(playertotals))
    indices = playerpergame[playerpergame.Tm == "TOT"].index
    #print(len(indices))   
    if(len(indices)!=0):
        playertotals = playertotals.drop(indices)
        playerpergame = playerpergame.drop(indices)
        playeradvanced = playeradvanced.drop(indices)
        playershooting = playershooting.drop(indices)
    #print(len(playeradvanced),len(playerpergame),len(playershooting),len(playertotals))
    return (playerpergame,playertotals,playeradvanced,playershooting)
## No shooting data from 1951-1997
year_options = list(range(1997,2022))
title = st.sidebar.title("Make a selection")
yr = st.sidebar.select_slider("Choose year",year_options,2021)
playerpergame,playertotals,playeradvanced, playershooting = load_data(yr)
player_options = playerpergame.Player.unique().tolist() 
pos_options = playerpergame.Pos.unique().tolist()
pl = st.sidebar.multiselect("Choose Players",player_options,player_options[0])
all_players = st.sidebar.checkbox("Select all players")
posits = playerpergame[playerpergame.Player.isin(pl)]["Pos"].unique().tolist()
if(len(posits)):
    pos = st.sidebar.multiselect("Choose Positions",pos_options,posits)
else:
    pos = st.sidebar.multiselect("Choose Positions",pos_options)
#https://discuss.streamlit.io/t/select-all-on-a-streamlit-multiselect/9799/2
if(all_players):
    pl = player_options
    pos = pos_options

if(len(pl)):
    st.dataframe(playeradvanced[playeradvanced.Player.isin(pl)])
    if(len(playeradvanced[playeradvanced.Player.isin(pl)])):
        fig = px.scatter(playerpergame[playerpergame["Player"].isin(pl)],x = "PTS",y = "eFG%",hover_name= "Player",range_x=[0,40],range_y=[0,1.2],color = "Tm")
        fig.update_layout(title = {'text' : "PPG vs eFG%", 'xanchor' : 'center', 'x' : 0.5}, yaxis=dict(
            autorange = True,
            type = "linear"
        ),xaxis = dict(
            autorange = True,
            type = "linear"
        ))
        st.plotly_chart(fig)
    ## For Guards
    if("PG" or "SG" or "SF" in pos):
        if(len(playeradvanced[playeradvanced.Player.isin(pl)])):
            fig1 = px.scatter(playershooting[playershooting["Player"].isin(pl)], x = "FG%  0-3 ft",y = "FG% 3P", hover_name="Player",color = "Tm")
            fig1.update_layout(title = {'text': "Finishing vs 3P%", 'xanchor' : 'center', 'x': 0.5},xaxis = dict(autorange = True, type = "linear"),yaxis = dict(autorange = True, type = "linear"))
            st.write(fig1)

    ## For front court
    if("PF" or "C" or "SF" in pos):
        if(len(playeradvanced[playeradvanced.Player.isin(pl)])):
            fig2 = px.scatter(playerpergame[playerpergame["Player"].isin(pl)], x = "TRB",y = "BLK", hover_name="Player",color = "Tm")
            fig2.update_layout(title = {'text': "Rebounding vs Blocking", 'xanchor' : 'center', 'x': 0.5},xaxis = dict(autorange = True, type = "linear"),yaxis = dict(autorange = True, type = "linear"))
            st.write(fig2)


else:
    st.dataframe(playeradvanced[playeradvanced.Pos.isin(pos)])
    if(len(playeradvanced[playeradvanced.Pos.isin(pos)])):
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
## For Guards
    if("PG" or "SG" or "SF" in pos):
        if(len(playeradvanced[playeradvanced.Pos.isin(pos)])):
            fig1 = px.scatter(playershooting[playershooting["Pos"].isin(pos)], x = "FG%  0-3 ft",y = "FG% 3P", hover_name="Player",color = "Tm")
            fig1.update_layout(title = {'text': "Finishing vs 3P%", 'xanchor' : 'center', 'x': 0.5},xaxis = dict(autorange = True, type = "linear"),yaxis = dict(autorange = True, type = "linear"))
            st.write(fig1)

    ## For front court
    if("PF" or "C" or "SF" in pos):
        if(len(playeradvanced[playeradvanced.Pos.isin(pos)])):
            fig2 = px.scatter(playerpergame[playerpergame["Pos"].isin(pos)], x = "TRB",y = "BLK", hover_name="Player",color = "Tm")
            fig2.update_layout(title = {'text': "Rebounding vs Blocking", 'xanchor' : 'center', 'x': 0.5},xaxis = dict(autorange = True, type = "linear"),yaxis = dict(autorange = True, type = "linear"))
            st.write(fig2)


