import pandas as pd
import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth 
import yaml
from PIL import Image



st.set_page_config(page_title="Scouting Dashboard", page_icon=":bar_chart:", layout="wide")


@st.cache(show_spinner=False)
def getData():
            # loading outfield players' cleaned data and engine
            player_df = pd.read_pickle(r'players')
            with open(r'player_ID.pickle', 'rb') as file:
                    player_ID = pickle.load(file)
            with open(r'playengine.pickle', 'rb') as file:
                    engine = pickle.load(file)

                # loading gk players' cleaned data and engine
            gk_df = pd.read_pickle(r'gk')
            with open(r'gk_ID.pickle', 'rb') as file:
                    gk_ID = pickle.load(file)
            with open(r'gkengine.pickle', 'rb') as file:
                    gk_engine = pickle.load(file)

            return [player_df, player_ID, engine], [gk_df, gk_ID, gk_engine]
                

players, gk = getData()


header = st.container()
data_info1 = st.container()
params = st.container()
result = st.container()


with header:
            st.title('Scouters Tool')
                


with data_info1:
                st.markdown('Based on the 22/23 season data for the **Big 5** leagues :soccer:')
                @st.cache
                def read_info(path):
                    return Path(path).read_text(encoding='utf8')

                st.markdown(read_info('info.md'), unsafe_allow_html=True)



with params:
    st.text(' \n')
    st.text(' \n')
    st.header('Tweak the parameters')
    
    col1, col2, col3 = st.columns([1, 2.2, 0.8])
    with col1:
        radio = st.radio('Player type', ['Players', 'Goal Keepers'])    
    with col2:
        if radio=='Players':
            df, player_ID, engine = players
        else:
            df, player_ID, engine = gk
        players = sorted(list(player_ID.keys()))
        age_default = (min(df['Age']), max(df['Age']))
        con_default = (min(df['Contract Year']), max(df['Contract Year']))

        query = st.selectbox('Player name', players, 
            help='Type without deleting a character. To search from a specific team, just type in the club\'s name.')
    with col3:
        foot = st.selectbox('Preferred foot', ['All', 'Automatic', 'Right', 'Left'], 
        help='\'Automatic\' matches the preferred foot of the selected player with the players automatically. \
            \'All\' by default. Preferred foot data is not available for GK\'s.')
    

    col4, col5, col6, col7 = st.columns([0.7, 1, 1, 1])
    with col4:
        if radio=='Players':
            res, val, step = (5, 20), 10, 5
        else:
            res, val, step = (3, 10), 5, 1
        count = st.slider('Number of results', min_value=res[0], max_value=res[1], value=val, step=step)
    with col5:
        comp = st.selectbox('League', ['All', 'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'],
            help='Leagues to get recommendations from. \'All\' leagues by default.')
    with col6:
        con = st.slider('Contract Year', min_value=con_default[0], max_value=con_default[1], value=con_default, 
        help='Age range to get recommendations from. Drag the sliders on either side. \'All\' ages by default.')
    with col7:
        age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default, 
        help='Age range to get recommendations from. Drag the sliders on either side. \'All\' ages by default.')
    

    
with result:
    st.text(' \n')
    st.text(' \n')
    st.text(' \n')
    st.markdown('_showing recommendations for_ **{}**'.format(query))
    

    def getRecommendations(metric, df_type, league='All', foot='All', con=con_default, age=age_default, count=val):
        if df_type == 'outfield':
            df_res = df.iloc[:, [1, 7, 9, 2,3,5,14,4]].copy()
        else:
            df_res = df.iloc[:, [1, 7, 9, 2,3,5,14,4]].copy()
        df_res['Player'] = list(player_ID.keys())
        df_res.insert(1, 'Similarity', metric)
        df_res = df_res.sort_values(by=['Similarity'], ascending=False)
        metric = [str(num) + '%' for num in df_res['Similarity']]
        df_res['Similarity'] = metric
        df_res = df_res.iloc[1:, :]

        
        if con==con_default:
            pass
        else:
            df_res = df_res[(df_res['Contract Year'] >= con[0]) & (df_res['Contract Year'] <= con[1])]


        if league=='All':
            pass
        else:
            df_res = df_res[df_res['Comp']==league]

        
        if age==age_default:
            pass
        else:
            df_res = df_res[(df_res['Age'] >= age[0]) & (df_res['Age'] <= age[1])]
        

        if foot=='All' or df_type == 'gk':
            pass
        elif foot=='Automatic':
            query_foot = df['Foot'][player_ID[query]]
            df_res = df_res[df_res['Foot']==query_foot]
        elif foot=='Left':
            df_res = df_res[df_res['Foot']=='left']
        else:
            df_res = df_res[df_res['Foot']=='right']
        
        
        df_res = df_res.iloc[:count, :].reset_index(drop=True)
        df_res.index = df_res.index + 1
        if len(df)==1416:
            mp90 = [str(round(num, 1)) for num in df_res['90s']]
            df_res['90s'] = mp90
        df_res.rename(columns={'Pos':'Position', 'Comp':'League'}, inplace=True)
        return df_res


    sims = engine[query]
    df_type = 'outfield' if len(df) ==1416  else 'gk'
    recoms = getRecommendations(sims, df_type=df_type, foot=foot, league=comp, con=con, age=age, count=count)
    st.table(recoms)
st.sidebar.header("Menu")
image = Image.open('scouterr.jpeg')
image1= Image.open('sid3.jpeg')
st.sidebar.image(image1,channels="RGB", output_format="auto")
st.sidebar.image(image,channels="RGB", output_format="auto",width=336)