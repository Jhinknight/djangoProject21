# importer les bibliothèques nécessaires
import base64
import urllib
import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
from PyPDF4 import PdfFileReader
from docx import Document
import html2text
import docx
import io
import sqlite3

from flask import request

def home(request):
    if request.method == 'POST':
        link = request.POST.get("link")
        # Récupération du contenu HTML de la page web
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraction des tableaux HTML de la page web
        tables = soup.find_all('table')

        # Affichage des données sous forme de graphique
        for table in tables:
            data = []
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                data.append(cols)
            data = np.array(data)

            # Affichage des données sous forme de graphique#
            x = data[:, 0]
            y = data[:, 1]
            try:
                y = y.astype(float)
            except ValueError:
                continue

            plt.bar(x, y)
            plt.show()
    else:
        link = None

    context = {'link': link}
    return render(request, 'home.html', context)

#url = request.POST.get('url')
#url = 'https://fr.wikipedia.org/wiki/Liste_des_pays_par_population'
#url = 'https://fr.wikipedia.org/wiki/Liste_des_villes_par_population'
#url = 'https://fr.wikipedia.org/wiki/Population_mondiale'



# Create your view here.
def table_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # récupère le tableau de la page
        tables = soup.find_all('table')
        for table in tables:
            data = []
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                data.append(cols)
            data = np.array(data)

            # Affichage des données sous forme de graphique#
            x = data[:, 0]
            y = data[:, 1]
            try:
                y = y.astype(float)
            except ValueError:
                continue

            plt.bar(x, y)
            plt.show()
    else:
        link = None

    context = {'url': url}
    return render(request, 'formulaire.html', context)
    '''
        # Initialisation de la liste pour stocker les tableaux
        table_data = []
        # récupérer les données du tableau et les stocker dans une liste ou un dictionnaire
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                row_data = []
                for cell in cells:
                    row_data.append(cell.text.strip())
                table_data.append(row_data)

        # passer les données au modèle de rendu HTML
        return render(request, 'affiche.html', table_data=table_data)

        # connexion à la base de données
        
        conn = sqlite3.connect('C:/Users/jhink/PycharmProjects/djangoProject2/db.sqlite3')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS table_data 
                     (column1 TEXT, column2 TEXT, column3 TEXT)""")
        
        for row in table.find_all("tr"):
            data = []
            for cell in row.find_all("td"):
                data.append(cell.text)
            if len(data) == 3:  # Vérifiez que la ligne a exactement 3 colonnes
                c.execute("INSERT INTO table_data VALUES (?, ?, ?)", data)

        conn.commit()

        # Requête SQL pour récupérer les données
        c.execute("SELECT column1, column2, column3 FROM table_data")

        # Stockage des données dans des listes séparées
        x_data = []
        y_data = []
        z_data = []

        for row in c.fetchall():
            x_data.append(row[0])
            y_data.append(row[1])
            z_data.append(row[2])

        # Création du graphique avec Matplotlib
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Mon graphique')

        # Exportation du graphique au format PNG
        fig.savefig('mon_graphique.png')

        # Fermeture de la connexion à la base de données
        conn.close()
        '''



# Afficher le graphique dans une page Django
def graph_view(request):
    return render(request, 'graph.html', {'image_path': 'C:/Users/jhink/OneDrive/Images/image64.png'})

# Create your view here.
def accueil(request):
    return render(request, "accueil.html")

# Create your view here.
def formulaire(request):
    return render(request, "formulaire.html")

# Create your view here.
def pdf(request):
    return render(request, "pdf.html")

# Create your view here.
def word(request):
    return render(request, "word.html")

# Create your view here.
def defilement(request):
    return render(request, "defilement.html")

def extract_table_from_pdf(file_path, page_num):
    with open(file_path, 'rb') as f:
        pdf = PdfFileReader(f)
        page = pdf.getPage(page_num)
        text = page.extractText()
        table_data = []
        rows = re.findall('\d+\.\d+.*\n', text)
        for row in rows:
            cells = re.findall('\d+\.\d+|[A-Za-z]+', row)
            table_data.append(cells)
        return table_data


def display_table(request):
    table_data = extract_table_from_pdf("C:/Users/jhink/OneDrive/Bureau/tableau.pdf", 0)
    context = {'table_data': table_data}
    return render(request, 'tableauPDF.html', context)

# vue qui extrait le tableau du fichier Word et le rend dans un template HTML
def extract_table(request):
    # Chemin vers le fichier Word contenant le tableau
    filepath = 'C:/Users/jhink/OneDrive/Bureau/tableau.docx'

    # Ouvre le fichier Word avec la bibliothèque python-docx
    document = Document(filepath)

    # Récupère le premier tableau du document
    table = document.tables[0]
    data = []

    for row in table.rows:
        data_row = []  # stockage des données d'une ligne
        for cell in row.cells:
            data_row.append(cell.text)
        data.append(data_row)

    # Convertit le tableau en HTML avec la bibliothèque html2text
    html_table = html2text.html2text(table._element.xml)

    # Affiche le tableau dans une page HTML avec le template 'table.html'
    return render(request, 'tableauWord.html', {'html_table': html_table})

def graphiqueW(request):
    doc = docx.Document('C:/Users/jhink/OneDrive/Bureau/tableau.docx')
    table = doc.tables[0]  # première table dans le document
    data1 = []  # stockage des données du tableau
    data = []
    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)
        if i == 0:
            keys = tuple(text)
            continue
        row_data = dict(zip(keys, text))
        data.append(row_data)

    # se connecter à la base de données SQLite3
    conn = sqlite3.connect('C:/Users/jhink/PycharmProjects/djangoProject2/db.sqlite3')
    cursor = conn.cursor()

    # créer une table pour stocker les données du tableau
    cursor.execute('''CREATE TABLE IF NOT EXISTS table_name
                      (column1 TEXT, column2 TEXT)''')

    # insérer les données du tableau dans la table
    for row in data:
        cursor.execute("INSERT INTO table_name (column1, column2) VALUES (?, ?)",
                       (row['Column 1'], row['Column 2']))

    # enregistrer les modifications et fermer la connexion à la base de données
    conn.commit()
    conn.close()

    for row in table.rows:
        data_row = []  # stockage des données d'une ligne
        for cell in row.cells:
            data_row.append(cell.text)
        data1.append(data_row)
    # conversion des données en listes de valeurs
    # première colonne du tableau
    x = [row[0] for row in data1[1:]]
    # deuxième colonne du tableau
    y = [str(row[1].replace(',', '.')) for row in data1[1:]]

    # création du graphique
    plt.plot(x, y)
    # titre de la première colonne
    plt.xlabel(data1[0][0])
    # titre de la deuxième colonne
    plt.ylabel(data1[0][1])
    plt.title('Titre du graphique')

    # génération du code HTML du graphique
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'graphiqueW.html', {'data': uri})

def graphiqueP(request):
    return render(request, 'graphiqueP.html')


