###################################
### Import ########################
###################################
import sys  # Stopt het programma direct en voorkomt dat de rest van de code doorgaat.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###################################
### Functies ######################
###################################
def data_ophalen(url):
    """
    Laadt data uit een CSV-bestand en retourneert een kopie van de DataFrame.
    """
    try:
        df = pd.read_csv(url)
        return df.copy()
    except Exception as error:
        print(f"Fout bij het ophalen van de data: {error}")
        sys.exit()

def data_opschonen(df, kolommen):
    """
    Verwijdert rijen met ontbrekende waarden in belangrijke kolommen.
    """
    return df.dropna(subset=kolommen).copy()

def selecteer_kolommen(df, kolommen):
    """
    Selecteert de kolommen die nodig zijn voor de analyse.
    """
    try:
        return df[kolommen].copy()
    except KeyError as error:
        print(f"Een of meer kolommen ontbreken in de dataset: {error}")
        sys.exit()

###################################
### Vraag 1 #######################
###################################
# Vraag - What is the biggest predictor of a large CO2 output per capita of a country?
###################################

# In deze vraag wordt onderzocht welke factor de grootste invloed heeft
# op CO2-uitstoot per persoon. Hiervoor worden energieverbruik en
# economische welvaart geanalyseerd met behulp van correlatie en grafieken.

#--- Data ophalen ---
#--------------------
# De dataset wordt ingeladen vanuit een externe bron (Our World in Data)
# en bevat gegevens over CO2-uitstoot, energieverbruik en GDP per land en jaar.

CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

df  = data_ophalen(CO2_URL)

#--- Data informatie tonen ---
#-----------------------------
# De eerste rijen, structuur en kolomnamen van de dataset worden weergegeven
# om inzicht te krijgen in de inhoud en kwaliteit van de data.

print("\n\nDe data:\n-------------------------------------------------")

print(df.head())
print("\n\nInformatie van de data:\n-------------------------------------------------")
df.info()
print("\n\nKolommen van de data:\n-------------------------------------------------")
print(df.columns,"\n-------------------------------------------------")

#--- Relevante kolommen selecteren ---
#-------------------------------------
# Alleen de kolommen die nodig zijn voor de analyse worden geselecteerd
# om de dataset overzichtelijk en gericht te houden.

kolommen = [
    "iso_code",
    "country",
    "year",
    "population",
    "gdp",
    "co2_per_capita",
    "energy_per_capita"
]

df = selecteer_kolommen(df, kolommen)

#--- Alleen landen selecteren ---
#--------------------------------
# Alleen echte landen worden geselecteerd op basis van ISO-code.
# Aggregaties zoals 'World' en continenten worden verwijderd.

df = df[df["iso_code"].str.len() == 3].copy()

#--- Data opschonen ---
#----------------------
# Rijen met ontbrekende waarden in de belangrijkste variabelen worden verwijderd
# om betrouwbare analyses en correcte berekeningen te garanderen.

df = data_opschonen(df, kolommen)

#--- GDP per capita berekenen ---
#--------------------------------
# GDP per capita wordt berekend door het totale GDP te delen door de populatie.
# Hiermee ontstaat een maat voor welvaart per persoon, die gebruikt wordt
# om de relatie tussen economische ontwikkeling en CO2-uitstoot te analyseren.

df["gdp_per_capita"] = df["gdp"] / df["population"]

#--- Top 10 landen weergeven ---
#-------------------------------
# Hier worden de landen met de hoogste gemiddelde CO2-uitstoot per persoon
# geselecteerd. Deze ranglijst helpt om concreet te laten zien welke landen
# hoge uitstoot hebben en ondersteunt de resultaten van de analyse.

top10 = (
    df.groupby("country")["co2_per_capita"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 landen:\n-------------------------------------------------\n", top10, "\n")

#--- Correlatie weergeven ---
#----------------------------
# De correlatieanalyse wordt gebruikt om de sterkte van de relatie tussen
# CO2-uitstoot per persoon en andere variabelen (energieverbruik en GDP)
# te bepalen. Op basis hiervan kan worden vastgesteld welke variabele de
# sterkste relatie heeft en daardoor de beste indicator is voor CO2-uitstoot.

correlatie = df[[
    "co2_per_capita",
    "energy_per_capita",
    "gdp_per_capita"
]].corr()

print("\nCorrelatie:\n-------------------------------------------------\n", correlatie, "\n")

# Energy_per_capita heeft de sterkste positieve correlatie met CO2-uitstoot,
# omdat deze de hoogste correlatie heeft (~0.73).
# Dit suggereert dat energieverbruik per persoon de belangrijkste indicator is.



###################################
### Vraag 2 #######################
###################################
# Vraag - Which countries are making the biggest strides in decreasing CO2 output?
###################################
#
# In deze analyse wordt onderzocht welke landen de grootste afname
# in CO2-uitstoot hebben gerealiseerd over tijd.
#
# Hiervoor wordt CO2-uitstoot per capita gebruikt in plaats van totale CO2.
# Dit zorgt voor een eerlijke vergelijking tussen landen, omdat verschillen
# in bevolkingsgrootte en veranderingen in populatie worden meegenomen.
#
# Per land wordt vervolgens de procentuele verandering berekend tussen de eerste en
# laatste beschikbare waarde. Dit laat zien hoe de uitstoot zich relatief heeft ontwikkeld.
#
# Landen met de grootste negatieve verandering hebben de grootste afname
# in CO2-uitstoot per persoon gerealiseerd en worden daarom beschouwd als
# de landen die de grootste vooruitgang hebben geboekt.
###################################

#--- Data opnieuw ophalen ---
#----------------------------
# Voor Vraag 2 wordt de originele dataset opnieuw gebruikt.
# Zo wordt voorkomen dat data die in Vraag 1 is verwijderd,
# onnodig ontbreekt in deze analyse.

df_2 = data_ophalen(CO2_URL)

kolommen_2 = [
    "iso_code",
    "country",
    "year",
    "co2_per_capita"
]

df_2 = selecteer_kolommen(df_2, kolommen_2)

#--- Alleen landen selecteren ---
df_2 = df_2[df_2["iso_code"].str.len() == 3].copy()

#--- Data opschonen ---
#----------------------
# Rijen met ontbrekende waarden worden verwijderd.

df_2 = data_opschonen(df_2, kolommen_2)

#--- Zorg dat kolom 'year' numeriek is ---
#--------------------------------------------
df_2["year"] = pd.to_numeric(df_2["year"], errors="coerce")

#--- Verwijder lege jaren ---
#----------------------------
df_2 = df_2.dropna(subset=["year"])

#--- Filter vanaf 1990 ---
#-------------------------
# Alleen data vanaf 1990 wordt gebruikt.
# De dataset bevat gegevens over een zeer lange periode,
# waarbij sommige landen al data hebben vanaf de 18e of 19e eeuw
# en andere landen pas veel later gegevens bevatten.
#
# Hierdoor ontstaan grote verschillen tussen de periodes
# die per land worden vergeleken.
#
# Door alleen data vanaf 1990 te gebruiken, worden landen
# over een recentere en beter vergelijkbare periode geanalyseerd.

df_2 = df_2[df_2["year"] >= 1990].copy()

#--- Data sorteren ---
#---------------------
# De data wordt gesorteerd op land en jaar, zodat per land de eerste
# en laatste beschikbare waarde correct kunnen worden bepaald.

df_2 = df_2.sort_values(by=["country", "year"]).copy()

#--- Eerste en laatste waarde bepalen ---
#----------------------------------------
# Voor elk land worden de eerste en laatste CO2 per capita waarden bepaald.

df_2_resultaat = df_2.groupby("country").agg(
    first_year=("year", "first"),
    last_year=("year", "last"),
    first_co2_per_capita=("co2_per_capita", "first"),
    last_co2_per_capita=("co2_per_capita", "last")
).copy()

#--- Deling door nul voorkomen ---
#---------------------------------
# Landen waarbij de eerste waarde 0 is worden verwijderd,
# om fouten bij percentage berekening te voorkomen.

df_2_resultaat = df_2_resultaat[
    df_2_resultaat["first_co2_per_capita"] > 0
].copy()

#--- Percentage CO2-verandering berekenen ---
#----------------------------------------
# Het percentage verschil tussen eerste en laatste waarde wordt berekend.
# Negatieve waarden betekenen een afname.

df_2_resultaat["co2_pct_change"] = (
    (df_2_resultaat["last_co2_per_capita"] -
     df_2_resultaat["first_co2_per_capita"])
    / df_2_resultaat["first_co2_per_capita"]
) * 100

#--- Alleen landen met daling selecteren ---
#-------------------------------------------
df_2_resultaat = df_2_resultaat[
    df_2_resultaat["co2_pct_change"] < 0
].copy()

#--- Top 10 landen weergeven ---
#-------------------------------
# De landen met de grootste daling worden geselecteerd.

top10_daling_co2 = (
    df_2_resultaat
    .sort_values(by="co2_pct_change")
    .head(10)
    .copy()
)

print("\nVraag 2 - Top 10 grootste procentuele daling in CO2 per capita:")
print("-------------------------------------------------")
print(top10_daling_co2)

#--- Staafdiagram weergeven ---
#------------------------------
# De resultaten worden visueel weergegeven in een staafdiagram.

top10_daling_co2_plot = top10_daling_co2.sort_values(by="co2_pct_change").copy()

plt.figure(figsize=(10, 6))

plt.barh(
    top10_daling_co2_plot.index,
    top10_daling_co2_plot["co2_pct_change"]
)

plt.xlabel("Percentage verandering in CO2 per capita (%)")
plt.ylabel("Land")
plt.title("Top 10 landen met grootste procentuele daling in CO2-uitstoot per capita")

plt.grid(axis="x")

plt.tight_layout()
plt.show()



###################################
### Vraag 3 #######################
###################################
# Which non-fossil fuel energy source is expected to grow the most in the future?
###################################
#
# In deze analyse wordt onderzocht welke non-fossil fuel energiebron
# naar verwachting de sterkste toekomstige groei laat zien.
#
# Omdat in de dataset geen directe prijsgegevens beschikbaar zijn,
# wordt het aandeel van duurzame energiebronnen in het totale
# energiegebruik gebruikt als indicator voor toekomstige groei.
#
# Hiervoor wordt lineaire regressie toegepast op historische wereldwijde
# data van zonne-energie, windenergie, waterkracht en kernenergie.
#
# De energiebron met de hoogste positieve helling wordt beschouwd als
# de energiebron met de sterkste voorspelde toekomstige groei.
###################################

#--- Energy data ophalen ---
#---------------------------
ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

df_3 = data_ophalen(ENERGY_URL)

#--- Relevante kolommen selecteren ---
#-------------------------------------
kolommen_vraag_3 = [
    "country",
    "year",
    "solar_share_energy",
    "wind_share_energy",
    "hydro_share_energy",
    "nuclear_share_energy"
]

df_3 = selecteer_kolommen(df_3, kolommen_vraag_3)

#--- Data opschonen ---
#----------------------
# Rijen met ontbrekende waarden in de gekozen energiekolommen worden verwijderd.
# Dit is nodig omdat lineaire regressie niet goed werkt met ontbrekende waarden.

df_3 = data_opschonen(
    df_3,
    [
        "solar_share_energy",
        "wind_share_energy",
        "hydro_share_energy",
        "nuclear_share_energy"
    ]
)

#--- Wereldwijde data selecteren ---
#-----------------------------------
# Voor deze voorspelling wordt gekeken naar de wereldwijde ontwikkeling.
# Hierdoor ontstaat een algemene trend voor non-fossil fuel energy.

df_wereld = df_3[df_3["country"] == "World"].copy()

#--- Energiebronnen vastleggen ---
#---------------------------------
# De energiekolommen worden gekoppeld aan duidelijke namen.
# Hierdoor kan de analyse generiek worden uitgevoerd met een for-loop.

energiebronnen = {
    "Solar": "solar_share_energy",
    "Wind": "wind_share_energy",
    "Hydro": "hydro_share_energy",
    "Nuclear": "nuclear_share_energy"
}

#--- Lineaire regressie toepassen ---
#------------------------------------
# Per energiebron wordt een regressiemodel gemaakt.
# De helling van de regressielijn geeft aan hoe snel de energiebron groeit.

toekomstige_jaren = np.array(range(2025, 2041))

groei_per_energiebron = {}

plt.figure(figsize=(10, 6))

for naam, kolom in energiebronnen.items():
    y = df_wereld[kolom].values

    helling, startwaarde = np.polyfit(df_wereld["year"], y, 1)

    voorspelling = helling * toekomstige_jaren + startwaarde

    groei_per_energiebron[naam] = helling

    plt.plot(
        toekomstige_jaren,
        voorspelling,
        label=naam
    )

#--- Beste energiebron bepalen ---
#---------------------------------
# De energiebron met de hoogste helling heeft de sterkste voorspelde groei.

beste_energiebron = max(groei_per_energiebron, key=groei_per_energiebron.get)

print("Voorspelde groei per energiebron:")
print("---------------------------------")

for naam, groei in groei_per_energiebron.items():
    print(f"{naam}: {groei:.4f}")

print("\nBeste toekomstige non-fossil fuel energiebron:")
print(beste_energiebron)

#--- Grafiek weergeven ---
#-------------------------
# De grafiek toont de voorspelde ontwikkeling van verschillende
# non-fossil fuel energiebronnen.

plt.title("Vraag 3: Toekomstige groei van non-fossil fuel energie")
plt.xlabel("Jaar")
plt.ylabel("Voorspeld aandeel in energiegebruik (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()