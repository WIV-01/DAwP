Winc Academy project - Data Analyst with Python.
----------------------------------------------------------------------------------

📊 DAwP – CO2, Energie en GDP Analyse

📌 Projectbeschrijving
----------------------------------------------------------------------------------
In dit project wordt een data-analyse uitgevoerd op wereldwijde gegevens over CO2-uitstoot, energieverbruik en GDP per capita.

De analyse is opgezet met herbruikbare functies en maakt gebruik van datasets van Our World in Data.
Per onderzoeksvraag wordt de data gefilterd, opgeschoond en gevisualiseerd.

🎯 Doel van het project
----------------------------------------------------------------------------------
Het doel is om inzicht te krijgen in:

De relatie tussen CO2-uitstoot, energieverbruik en economische groei
Welke landen hun CO2-uitstoot het sterkst verminderen
Hoe energiegebruik is verdeeld over verschillende bronnen

❓ Onderzoeksvragen
----------------------------------------------------------------------------------
Vraag 1
---------
---------
Wat is de relatie tussen:

CO2 per capita
Energieverbruik per capita
GDP per capita

➡️ Analyse met correlatie + scatterplot + top 10 landen
----------------------------------------------------------------------------------
Vraag 2
---------
---------
Welke landen maken de grootste stappen in het verminderen van CO2-uitstoot?

➡️ Analyse met procentuele verandering per land
➡️ Resultaat: landen met grootste daling in CO2 per capita
----------------------------------------------------------------------------------
Vraag 3
---------
---------
Hoe is het aandeel van energiebronnen verdeeld?

➡️ Analyse van:
----------------------------------------------------------------------------------
Zon (solar)
Wind
Waterkracht (hydro)
Kernenergie (nuclear)

➡️ Visualisatie van energieverdeling
----------------------------------------------------------------------------------
📂 Data

De datasets worden direct geladen via URL (geen lokale bestanden):

CO2 dataset
Energie dataset
GDP dataset

Alle data wordt ingeladen met een generieke functie:
def data_ophalen(url):
    df = pd.read_csv(url)
    return df.copy()

🛠️ Gebruikte technologieën
----------------------------------------------------------------------------------
Python
Pandas
NumPy
Matplotlib

⚙️ Werkwijze
----------------------------------------------------------------------------------
De code is opgebouwd volgens deze stappen:
Data ophalen
Data opschonen (dropna op relevante kolommen)
Kolommen selecteren
Berekeningen uitvoeren (correlatie / procentuele verandering)
Visualisatie maken (grafieken)

Alle stappen zijn uitgewerkt met functies voor herbruikbaarheid.

▶️ Gebruik
----------------------------------------------------------------------------------
Run het script:
python main.py

📈 Resultaten
----------------------------------------------------------------------------------
Het project bevat:

3 analyses (één per vraag)
3 grafieken
Data-gedreven inzichten per vraag

📊 Belangrijkste inzichten
----------------------------------------------------------------------------------
Er is een duidelijke positieve relatie tussen energieverbruik en CO2-uitstoot.
Sommige landen laten een sterke daling zien in CO2 per capita.
Hernieuwbare energiebronnen nemen toe, maar verschillen per land.

📁 Projectstructuur
----------------------------------------------------------------------------------
DAwP/
│
├── main.py
├── Report.docx
├── README.md

👤 Auteur
----------------------------------------------------------------------------------
Fred C. Wilson IV
Data & Automation Specialist
(in ontwikkeling als Data Analyst met Python)