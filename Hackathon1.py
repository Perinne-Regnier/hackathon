### LES IMPORTS
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import altair as alt
from datetime import datetime
from datetime import timedelta
import plotly.express as px

### LE DATASET
link="https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
hackathon = pd.read_csv(link)
hackathon2 =hackathon.copy()


# variable qui contient uniquement les valeurs aggrégées de WORLD
worldstat = hackathon2.loc[hackathon2["country"]=="World"]

worldstat.rename(columns={"coal_co2": "Charbon","oil_co2": "Pétrole","gas_co2": "Gaz","cement_co2": "Ciment",
                     "flaring_co2": "Torchage","other_industry_co2": "Autres industries"}, inplace=True)
# table pivot pour avoir les valeur par année 
co2consumption = pd.pivot_table(worldstat, values='co2', index='year')
co2consumption.reset_index(inplace=True)


### LA PAGE DE CONFIGURATION ###
st.set_page_config(
     page_title="Régler le problème de CO2 dans le monde une bonne fois pour toute",
     page_icon="🌍",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
        'Get Help':  None,
         'Report a bug': None,
         'About': "# Bienvenue ! # \n"
         "Xavier, Charles et Périnne vous présentent leur analyse sur les émissions de CO2 au niveau mondial réalisé lors d'un Hackathon.\n"
       "Nous disposions d'une trentaine d'heures pour réaliser une analyse suivant la thématique suivante : comment, au niveau mondial, nous situons nous \n"
       "par rapport à l'objectif de neutralité carbone de 2050.\n"
       "Avant de parler de 2050, nous avons souhaité faire un constat à un horizon plus court, l'objectif de 2030. \n"
       "Pour cela, nous nous sommes donc intéressés aux populations et aux habitudes de consommations dans les émissions de CO2. \n"
         "Et Enfin dans quelle mesure la suppression des habitudes impactait les émissions par rapport aux objectifs fixés en 2030.\n"
         "Bonne découverte! \n"
         "Etudiants et étudiantes à la Wild Code School de Nantes \n"
     }
 )

### TITRE PRINCIPAL ###
st.title("Comment atteindre l'objectif 2030 d'émission de CO2 dans le monde ?")
st.write("                                                   ")

###############################
### PREMIERE PARTIE : BILAN ###
###############################

### TITRE DE LA PARTIE
st.subheader(" Bilan à 2020 des émissions de CO2 généré par le secteur de l'énergie")

# On change la colonne des années en string sinon il est pas content pour la suite
co2consumption["year"]=co2consumption["year"].apply(lambda x : str(x))


### GRAPHIQUE PRINCIPALE
line_chart = alt.Chart(co2consumption).mark_line().encode(
    x=alt.X("year:T",title='Années'), 
    y=alt.Y('co2', title='Emission de CO2 en millions de tonnes en fonction du temps'),
    color=alt.value("#FF27D0"),
)
objective=alt.Chart(co2consumption).mark_rule().encode(y=alt.datum(15000))

st.altair_chart(objective + line_chart, use_container_width=True)

with st.container():
    col1, col2= st.columns(2)

    col1.write("L'objectif de baisse de CO2 mondial fourni par l'ONU pour l'année 2030 est d'environ **15 milliards de tonnes par an**, comme vous pouvez le constater nous sommes légèrement au-dessus rien de bien inquiètant 😊 (sarcasme).")
    col1.write("\n")
    col1.write("Il y a une grosse montée des émissions dans le monde depuis l'après-guerre, mais c'est devenu incontrôlable... Aujourd'hui en 2022, à l'heure où est créée cette interface, nous n'avons pas de clés pour inverser cette tendance, mais nous allons quand même tenter de voir ensemble ce qui pourrait l'impact.")
    col2.image(
            "https://media.giphy.com/media/l3vR5UgInxQW8wK6k/giphy.gif",
            use_column_width="auto")

#######################################
### PARTIE 2 : SECTEURS INDUSTRIELS ###
#######################################


### TITRE
st.write("                                                   ")
st.subheader("Quels ajustements faire sur les différents secteurs industriels ?")
st.write("                                                   ")




col1, col2= st.columns((3,1))
### GRAPHIQUE DES SECTEURS INDUSTRIELS
with col1:
    fig =px.area(data_frame =worldstat, x='year',y=['Charbon','Pétrole','Gaz','Ciment','Torchage','Autres industries'],
                 color_discrete_sequence= px.colors.diverging.PiYG, 

                )

    fig.update_layout(
#         font_family="IBM Plex Sans",
        title = "Parts des différents secteurs industriels dans l'émission de CO2 à travers le temps",
        xaxis_title="Années",
        yaxis_title="Émission de CO2 en mt/an",
        legend_title="Industries",
    )

    st.plotly_chart(fig, use_container_width=True)
    
### TEXTE DES SECTEURS INDUSTRIELS    
with col2:        
    st.write("\n")
    st.write("\n")
    st.write("Le graphique ci-contre nous montre la belle performance du charbon,\n"
             "qui non seulement est la source de CO2 la plus ancienne mais toujours\n"
             "la plus forte aujourd'hui.\n"
             "Le pétrole n'est pas en reste, depuis 1950 il ne cesse de progresser et reste à une belle place de second.")
    st.write("\n")
    st.write("Ce qu'on vous propose c'est de jouer avec les différentes industries ci-bas.\n"
             "Nous vous laissons déterminer sur quelles industries nous pouvons taper pour\n"
             "que demain soit un monde meilleur. 💖\n")


st.write("                                                   ")

### GRAPHIQUE MODIFIABLE DES SECTEURS INDUSTRIELS
col1, col2, col3 = st.columns((1,1,3))
with col1:
    with st.expander("Charbon"):
        charbon=st.slider("Modifier la proportion de l'industrie", -100, 100, 0, key="charbon")
    with st.expander("Pétrole"):
        petrole=st.slider("Modifier la proportion de l'industrie", -100, 100, 0, key="petrole")
    with st.expander("Gaz"):
        gaz = st.slider("Modifier la proportion de l'industrie", -100, 100, 0, key="gaz")
with col2: 
    with st.expander("Ciment"):
        ciment = st.slider("Modifier la proportion de l'industrie", -100, 100, 0, key="ciment")
    with st.expander("Torchage"):
        torchage = st.slider("Modifier la proportion de l'industrie", -100, 100, 0, key="torchage")
    with st.expander("Autres industries"):
        autres = st.slider("Modifier la proportion de ces industries", -100, 100, 0, key="autres")
    
pourcentreglette = (charbon*0.4015) + (petrole*0.3181) + (gaz*0.2125) + (ciment*0.0467) + (torchage*0.0125) + (autres*0.0087)
#stock la valeur additionné de nos reglettes
worldstat2000=worldstat.copy()
worldstat2000['Courbe']= 'Réel'
worldstat2000Dystopie=worldstat2000.copy()
worldstat2000Dystopie['Courbe']= 'Avec modifications'
worldstat2000Dystopie["co2"]=worldstat2000Dystopie["co2"].apply(lambda x : x*((100+pourcentreglette)/100))
worldstat2000complete = pd.concat([worldstat2000,worldstat2000Dystopie])
worldstat2000complete["year"]=worldstat2000complete["year"].apply(lambda x : str(x))


with col3:
    line_chart_test = alt.Chart(worldstat2000complete).mark_line().encode(
    x=alt.X("year:T",title='Années'), 
    y=alt.Y('co2', title='Emission de CO2 en millions de tonnes'),
    color= alt.Color('Courbe',scale=alt.Scale(range=["plum", "darkorchid"]))
    ).properties(
    height=400)

    objective=alt.Chart(worldstat2000complete).mark_rule().encode(y=alt.datum(15000))
    st.altair_chart(line_chart_test + objective, use_container_width=True)

#############################    
### PARTIE 3 : CONTINENTS ###
#############################

# On va créer un data frame
continent2020 = hackathon2.loc[hackathon2["year"]== 2020]
continent2020 = continent2020.loc[(continent2020["country"]=="North America")|(continent2020["country"]=="Europe")|(continent2020["country"]=="Asia")|(continent2020["country"]=="Africa")|(continent2020["country"]=="Antarctica")|(continent2020["country"]=="Oceania")|(continent2020["country"]=="South America")]
continent2020 = continent2020.fillna(0)

### TITRE DE LA PARTIE
st.write("                                                   ")
st.subheader("Y a-t-il des ajustements à faire au niveau des continents ? 💣")
st.write("                                                   ")

col1, col2= st.columns((1,3))

### GRAPHIQUE SUR LA PROPORTION D'EMISSION DE CO2 PAR CONTINENT
with col1:
    fig1, ax1 = plt.subplots()

    sns.barplot(data = continent2020, x = "country",y = "co2", color= "plum",
                ax = ax1, order=continent2020.sort_values('co2').country).set(title="Répartition des émissions de CO2 des continents en 2020")
    plt.xticks(rotation=45)
    st.pyplot(fig1, use_container_width=True)

    
### TEXTE DE LA PARTIE    
with col2:   
    col2.write("Ce que nous constatons dans un premier temps dans le graphique ci-contre, c'est que l'Asie est le continent qui pollue le plus avec plus de 60% des émissions de CO2 mondiales en 2020 (la Chine a elle toute seule représente environ 30% des émission de CO2 dans le monde).")
    col2.write("\n")
    col2.write("Vous voyez déjà la suite, on va vous proposer de diminuer l'impact des différents continents, mais avant d'établir une politique dictatoriale en Asie, il faut quand même se souvenir qu'il s'agit de l'usine du monde, ce qui fait qu'ils polluent également pour le plaisir de tous les autres continents.")



st.write("                                                   ")

### GRAPHIQUE SUR LA MODIFICATION DES CONTINENTS
col1, col2, col3 = st.columns((3,1,1))
with col2:
    with st.expander("Antarctique"):
        antarctique=st.slider("Tentez ce que vous voulez, ça ne fera rien", -100, 100, 0, key="antarctique")
    with st.expander("Océanie"):
        oceanie =st.slider("Modifier la population du continent", -100, 100, 0, key="oceanie")
    with st.expander("Amérique du Sud"):
        ameriquesud = st.slider("Modifier la population du continent", -100, 100, 0, key="ameriquesud")
    with st.expander("Afrique"):
        afrique = st.slider("Modifier la population du continent", -100, 100, 0, key="afrique")
with col3: 
    with st.expander("Europe"):
        europe = st.slider("Modifier la population du continent", -100, 100, 0, key="europe")
    with st.expander("Amérique du Nord"):
        ameriquenord = st.slider("Modifier la population du continent", -100, 100, 0, key="ameriquenord")
    with st.expander("Asie"):
        asie = st.slider("Modifier la population du continent", -100, 100, 0, key="asie")
    
pourcentreglette = (antarctique*0) + (oceanie*0.013) + (ameriquesud*0.029) + (afrique*0.039) + (europe*0.146) + (ameriquenord*0.171) + (asie*0.601)

worldstat2000=worldstat.copy()
worldstat2000['Courbe']= 'Réel'
worldstat2000Dystopie=worldstat2000.copy()
worldstat2000Dystopie['Courbe']= 'Dystopie nucléaire'
worldstat2000Dystopie["co2"]=worldstat2000Dystopie["co2"].apply(lambda x : x*((100+pourcentreglette)/100))
worldstat2000complete = pd.concat([worldstat2000,worldstat2000Dystopie])
worldstat2000complete["year"]=worldstat2000complete["year"].apply(lambda x : str(x))


with col1:
    line_chart_test = alt.Chart(worldstat2000complete).mark_line().encode(
    x=alt.X("year:T",title='Années'), 
    y=alt.Y('co2', title='Emission de CO2 en millions de tonnes'),
    color= alt.Color('Courbe',scale=alt.Scale(range=["plum", "darkorchid"]))
    ).properties(
    height=400)

    objective=alt.Chart(worldstat2000complete).mark_rule().encode(y=alt.datum(15000))
    st.altair_chart(line_chart_test + objective, use_container_width=True)

###########################    
### PARTIE 4 : PLAISIRS ###
###########################

### TITRE
st.write("                                                   ")
st.subheader("Réduire nos loisirs pour réduire l'émission de CO2 ?")

### TEXTE POUR PRESENTER LE GRAPHIQUE
st.write("Le graphique ci-dessous va vous permettre de visualiser l'impact de vos loisirs sur l'émission de CO2 mondial si jamais vous décidez de les interdir complètement (ou si vous les doublez, petits filous !). Nous tenons à préciser que nous nous basons sur de vraies données pour vous fournir ce graphique !")


### GRAPHIQUE SUR LA MODIFICATION DES PLAISIRS
col1, col2, col3 = st.columns((3,1,1))
with col2:
    with st.expander("Voyages "):
        avions=st.slider("Modifier le taux d'avions", -100, 100, 0, key="avions")
    with st.expander("Netflix"):
        streaming=st.slider("Modifier le taux de streaming", -100, 100, 0, key="streaming")
with col3: 
    with st.expander("Alcool"):
        alcool = st.slider("Modifier l'alcoolisme mondial", -100, 100, 0, key="alcool")
    with st.expander("Smartphone"):
        smartphone = st.slider("Modifier le nombre de smartphone", -100, 100, 0, key="smartphone")
    
resultat = (avions*0.0136) + (streaming*0.01) + (alcool*0.007) + (smartphone*0.004) #stock la valeur additionné de nos reglettes
worldstat2000=worldstat.copy()
worldstat2000['Courbe']= 'Réel'
worldstat2000Dystopie=worldstat2000.copy()
worldstat2000Dystopie['Courbe']= 'Avec modifications'
worldstat2000Dystopie["co2"]=worldstat2000Dystopie["co2"].apply(lambda x : x*((100+resultat)/100))
worldstat2000complete = pd.concat([worldstat2000,worldstat2000Dystopie])
worldstat2000complete["year"]=worldstat2000complete["year"].apply(lambda x : str(x))


with col1:
    line_chart_test = alt.Chart(worldstat2000complete).mark_line().encode(
    x=alt.X("year:T",title='Années'), 
    y=alt.Y('co2', title='Emission de CO2 en millions de tonnes'),
    color= alt.Color('Courbe',scale=alt.Scale(range=["plum", "darkorchid"]))
    ).properties(
    height=400)

    objective=alt.Chart(worldstat2000complete).mark_rule().encode(y=alt.datum(15000))
    st.altair_chart(line_chart_test + objective, use_container_width=True)

    
### LE MOT DE LA FIN    
st.write("Vous êtes surpris ? Nous aussi.")
st.write("L'impact réél de l'avion a été notre **grande** surprise. Supprimer le transport aérien aurait un impact très faible par rapport à d'autres actions qui pourraient être entreprises. Sachant qu'il s'agit d'un argument souvent utilisé pour culpabiliser les amoureux du voyage, il faut définitivement mettre celui-ci en perspective.")
st.write("\n")
st.write("Pour terminer, comme vous pouvez le constater nous ne proposons pas de solution miracle.\n")
st.write("En effet, les émissions de CO2 sont un problème complexe assujeti à plusieurs variables. Cependant, nous espérons vous avoir diverti avec cette analyse et restons disponibles si vous avez des questions.")
st.write("Pour information, toutes les données sont issues du site : https://ourworldindata.org/ que nous vous recommandons de visiter !\n")




