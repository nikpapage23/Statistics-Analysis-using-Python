import requests
import pandas as pd
import sqlite3
import csv
import io
import simplejson
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np
import sys

total_arrivals_list = []
quarter_list = []


def download_excels():
    # Χρήση dictionary για την αποθήκευση των links για τα αρχεία excel
    url_dictionary = {
        "2011d": "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113865&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
        "2012d": "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113886&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
        "2013d": "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113905&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
        "2014d": "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113925&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el"
    }

    # Προσπέλαση του dictionary και κατέβασμα των αρχείων excel με όνομα το εκάστοτε key που έχει στο dictionary
    for i in url_dictionary:
        resp = requests.get(url_dictionary[i])
        output = open(i + '.xls', 'wb')
        output.write(resp.content)
        output.close()


def arrivals_per_year():

    # Χρήση της βιβλιοθήκης pandas για ανάγνωση των αρχείων excel και αποθήκευση στη λίστα total_arrivals_list
    # τη τιμή που δείχνει τις συνολικές αφίξεις κάθε χρονιάς

    df = pd.read_excel(r'2011d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    total_arrivals_list.append(df['Total'].iloc[133])

    df = pd.read_excel(r'2012d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    total_arrivals_list.append(df['Total'].iloc[135])

    df = pd.read_excel(r'2013d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    total_arrivals_list.append(df['Total'].iloc[135])

    df = pd.read_excel(r'2014d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    total_arrivals_list.append(df['Total'].iloc[135])


def countries_arrivals():

    # Χρήση της βιβλιοθήκης pandas για ανάγνωση των excel και μετατροπή τους σε dictionary με key το όνομα κάθε χώρας
    # και value τις αφίξεις που σημειώθηκαν από την εκάστοτε χώρα. Έπειτα γίνεται καθαρισμός του κάθε dictionary,
    # διαγράφοντας τα keys που συμπεριλαμβάνονται στο entriesToRemove, ενώ επίσης με χρήση της βιβλιοθήκης simplejson
    # διαγράφουμε τις NaN τιμές. Η παραπάνω διαδικασία επαναλαμβάνεται για κάθε excel αρχείο.

    # ~~ 2011 ~~
    df = pd.read_excel(r'2011d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    dict_1 = df.set_index('Country')['Total'].to_dict()
    entriesToRemove_1 = ('ΜΗΝΑΣ: Δεκέμβριος 2011', 'από τΙς οποίες:', 'ΠΕΡΙΟΔΟΣ:Ιανουάριος 2011-Δεκέμβριος 2011',
                         'Μη προσδιορίσιμες χώρες ταξιδιωτών', 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ', 'null')
    clean_dict_1 = simplejson.loads(simplejson.dumps(dict_1, ignore_nan=True))
    for k in entriesToRemove_1:
        clean_dict_1.pop(k, None)
    # print(clean_dict_1)

    # ~~ 2012 ~~
    df = pd.read_excel(r'2012d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    dict_2 = df.set_index('Country')['Total'].to_dict()
    entriesToRemove_2 = ('ΜΗΝΑΣ: Δεκέμβριος 2012', 'από τΙς οποίες:', 'ΠΕΡΙΟΔΟΣ:Ιανουάριος 2012 - Δεκέμβριος 2012',
                         'Μη προσδιορίσιμες χώρες ταξιδιωτών', 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ', 'null')
    clean_dict_2 = simplejson.loads(simplejson.dumps(dict_2, ignore_nan=True))
    for k in entriesToRemove_2:
        clean_dict_2.pop(k, None)
    # print(clean_dict_2)

    # ~~ 2013 ~~
    df = pd.read_excel(r'2013d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    dict_3 = df.set_index('Country')['Total'].to_dict()
    entriesToRemove_3 = ('ΜΗΝΑΣ: Δεκέμβριος 2013', 'από τΙς οποίες:', 'ΠΕΡΙΟΔΟΣ:Ιανουάριος 2013 - Δεκέμβριος 2013',
                         'Μη προσδιορίσιμες χώρες ταξιδιωτών', 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ', 'null', 'Σερβία')
    clean_dict_3 = simplejson.loads(simplejson.dumps(dict_3, ignore_nan=True))
    for k in entriesToRemove_3:
        clean_dict_3.pop(k, None)
    clean_dict_3['Σερβία'] = clean_dict_3.pop('Σερβία ')
    clean_dict_3['Κροατία'] = clean_dict_3.pop('Κροατία (2)')
    # print(clean_dict_3)

    # ~~ 2014 ~~
    df = pd.read_excel(r'2014d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    dict_4 = df.set_index('Country')['Total'].to_dict()
    entriesToRemove_4 = ('ΜΗΝΑΣ: Δεκέμβριος 2014', 'από τΙς οποίες:', 'ΠΕΡΙΟΔΟΣ:Ιανουάριος 2014 - Δεκέμβριος 2014',
                         'Μη προσδιορίσιμες χώρες ταξιδιωτών', 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ', 'null',
                         '(1)  Μετά την ένταξη της Κροατίας στην Ε.Ε. την 1η Ιουλίου 2013 τα σχετικά στοιχεία για τη χώρα αυτή εμφανίζονται πλέον στις χώρες της\n     Ε.Ε.  Τα αντίστοιχα στοιχεία για το πρώτο εξάμηνο 2013, καθώς και για τα προηγούμενα έτη περιλαμβάνονται στις "Λοιπές χώρες\n     Ευρώπης".',
                         '(2)  Από το Μάιο 2014 η σιδηροδρομική σύνδεση της Ελλάδος με το εξωτερικό τέθηκε εκ νέου σε λειτουργία, ως εκ τούτου δεν είναι δυνατή\n      η σύγκριση με το αντίστοιχο εξάμηνο του έτους 2013.  ')
    clean_dict_4 = simplejson.loads(simplejson.dumps(dict_4, ignore_nan=True))
    for k in entriesToRemove_4:
        clean_dict_4.pop(k, None)
    clean_dict_4['Σερβία'] = clean_dict_4.pop('Σερβία ')
    clean_dict_4['Κροατία'] = clean_dict_4.pop('Κροατία (1)')
    # print(clean_dict_4)

    # Τελικά με χρήση του Counter της βιβλιοθήκης collections αθροίζουμε τα dictionaries που προέκυψαν, σχηματίζοντας ένα
    # τελικό dictionary ονόματι result που περιέχει τις τελικές αφίξεις που σημειώθηκαν την τετραετία 2011-2014 για κάθε χώρα

    result = Counter(clean_dict_1) + Counter(clean_dict_2) + Counter(clean_dict_3) + Counter(clean_dict_4)
    # print(result)
    return result


def means_of_transport():

    # Χρήση dictionary με key το κάθε μεταφορικό μέσο και value τον αριθμό αφίξεων που σημειώθηκε με το κάθε μέσο
    # κατά την τετραετία 2011-2014

    transport = {
        "ΑΕΡΟΠΟΡΙΚΩΣ": "",
        "ΣΙΔ/ΚΩΣ": "",
        "ΘΑΛΑΣΣΙΩΣ": "",
        "ΟΔΙΚΩΣ": ""
    }

    # Γίνεται ανάγνωση των excel αρχείων κάθε χρονιάς και ενημερώνονται αντίστοιχα οι μεταβλητές air, railway, sea και
    # road, οι τελικές τιμές των οποίων ενημερώνουν τελικά τις θέσεις του dictionary

    # ~~ 2011 ~~
    df = pd.read_excel(r'2011d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    air = df['Air'].iloc[133]
    railway = df['Railway'].iloc[133]
    sea = df['Sea'].iloc[133]
    road = df['Road'].iloc[133]

    # ~~ 2012 ~~
    df = pd.read_excel(r'2012d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    air += df['Air'].iloc[135]
    railway += df['Railway'].iloc[135]
    sea += df['Sea'].iloc[135]
    road += df['Road'].iloc[135]

    # ~~ 2013 ~~
    df = pd.read_excel(r'2013d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    air += df['Air'].iloc[135]
    railway += df['Railway'].iloc[135]
    sea += df['Sea'].iloc[135]
    road += df['Road'].iloc[135]

    # ~~ 2014 ~~
    df = pd.read_excel(r'2014d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    air += df['Air'].iloc[135]
    railway += df['Railway'].iloc[135]
    sea += df['Sea'].iloc[135]
    road += df['Road'].iloc[135]

    # Ενημέρωση θέσεων του dictionary
    transport.update([('ΑΕΡΟΠΟΡΙΚΩΣ', air), ('ΣΙΔ/ΚΩΣ', railway),
                      ('ΘΑΛΑΣΣΙΩΣ', sea), ('ΟΔΙΚΩΣ', road)])
    # print(transport)
    return transport


def arrivals_per_quarter():

    # Ακολουθείται παρόμοια διαδικασία με προηγούμενες συναρτήσεις, αποθηκεύοντας τελικά σε κάθε θέση του dictionary
    # quarter τον αριθμό των αφίξεων που σημειώθηκαν στο αντίστοιχο τρίμηνο

    quarter = {
        "2011 Α'": "",
        "2011 Β'": "",
        "2011 Γ'": "",
        "2011 Δ'": "",
        "2012 Α'": "",
        "2012 Β'": "",
        "2012 Γ'": "",
        "2012 Δ'": "",
        "2013 Α'": "",
        "2013 Β'": "",
        "2013 Γ'": "",
        "2013 Δ'": "",
        "2014 Α'": "",
        "2014 Β'": "",
        "2014 Γ'": "",
        "2014 Δ'": ""
    }

    # ~~ 2011 ~~
    # Α' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2011d.xls', 'ΜΑΡ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Β' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2011d.xls', 'ΙΟΥΝ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Γ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2011d.xls', 'ΣΕΠ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Δ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2011d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # ~~ 2012 ~~
    # Α' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2012d.xls', 'ΜΑΡ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Β' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2012d.xls', 'ΙΟΥΝ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Γ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2012d.xls', 'ΣΕΠΤ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Δ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2012d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[135])

    # ~~ 2013 ~~
    # Α' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2013d.xls', 'ΜΑΡ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[131])

    # Β' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2013d.xls', 'ΙΟΥΝ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[131])

    # Γ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2013d.xls', 'ΣΕΠ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[135])

    # Δ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2013d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[135])

    # ~~ 2014 ~~
    # Α' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2014d.xls', 'ΜΑΡ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[134])

    # Β' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2014d.xls', 'ΙΟΥΝ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[135])

    # Γ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2014d.xls', 'ΣΕΠΤ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[133])

    # Δ' ΤΡΙΜΗΝΟ
    df = pd.read_excel(r'2014d.xls', 'ΔΕΚ')
    df.columns = ['ID', 'Country', 'Air', 'Railway', 'Sea', 'Road', 'Total']
    quarter_list.append(df['Total'].iloc[135])

    # Ενημέρωση θέσεων του dictionary
    quarter.update([("2011 Α'", quarter_list[0]), ("2011 Β'", quarter_list[1]), ("2011 Γ'", quarter_list[2]),
                    ("2011 Δ'", quarter_list[3]),
                    ("2012 Α'", quarter_list[4]), ("2012 Β'", quarter_list[5]), ("2012 Γ'", quarter_list[6]),
                    ("2012 Δ'", quarter_list[7]),
                    ("2013 Α'", quarter_list[8]), ("2013 Β'", quarter_list[9]), ("2013 Γ'", quarter_list[10]),
                    ("2013 Δ'", quarter_list[11]),
                    ("2014 Α'", quarter_list[12]), ("2014 Β'", quarter_list[13]), ("2014 Γ'", quarter_list[14]),
                    ("2014 Δ'", quarter_list[15])])

    return quarter


# Συνάρτηση για δημιουργία και εισαγωγή των επιθυμητών δεδομένων σε βάση δεδομένων της SQlite
def import_to_DB():

    # Δημιουργία και σύνδεση στη βάση δεδομένων tourism.db και δημιουργία των αντίστοιχων tables για την αποθήκευση
    # των δεδομένων που έχουμε συλλέξει από τα αρχεία excel
    try:
        mydb = sqlite3.connect('tourism.db')

        mycursor = mydb.cursor()

        mycursor.execute("CREATE TABLE IF NOT EXISTS Arrivals_Per_Year ("
                         "year INT(4) PRIMARY KEY,"
                         "total_arrivals FLOAT);")

        mycursor.execute("CREATE TABLE IF NOT EXISTS Arrivals_Per_Country ("
                         "country VARCHAR(100) PRIMARY KEY,"
                         "arrivals FLOAT);")

        mycursor.execute("CREATE TABLE IF NOT EXISTS Arrivals_Per_Mean_Of_Transport ("
                         "mean_of_transport VARCHAR(20) PRIMARY KEY,"
                         "arrivals FLOAT);")

        mycursor.execute("CREATE TABLE IF NOT EXISTS Arrivals_Per_Quarter ("
                         "quarter VARCHAR(10) PRIMARY KEY,"
                         "arrivals FLOAT);")

        mydb.commit()

        years_list = ['2011', '2012', '2013', '2014']

        # Εισαγωγή στο table Arrivals_Per_Year της αντίστοιχης χρονιάς και των συνολικών αφίξεών της
        for i, j in zip(years_list, total_arrivals_list):
            mycursor.execute("INSERT INTO Arrivals_Per_Year VALUES (?, ?)", (i, j))
        mydb.commit()

        # Εισαγωγή στο table Arrivals_Per_Country των keys και values του countries_dict
        for i in countries_dict:
            mycursor.execute("INSERT INTO Arrivals_Per_Country VALUES (?, ?)", (i, countries_dict[i]))
        mydb.commit()

        # Εισαγωγή στο table Arrivals_Per_Mean_Of_Transport των keys και values του transport_dict
        for i in transport_dict:
            mycursor.execute("INSERT INTO Arrivals_Per_Mean_Of_Transport VALUES (?, ?)", (i, transport_dict[i]))
        mydb.commit()

        # Εισαγωγή στο table Arrivals_Per_Quarter των keys και values του quarter_dict
        for i in quarter_dict:
            mycursor.execute("INSERT INTO Arrivals_Per_Quarter VALUES (?, ?)", (i, quarter_dict[i]))
        mydb.commit()

        mydb.close()

    # Σε οποιαδήποτε περίπτωση εκδήλωσης εξαίρεσης τυπώνεται σχετικό μήνυμα και τερματίζει το πρόγραμμα
    except Exception as e:
        print(e)
        sys.exit()


# Συνάρτηση για εξαγωγή των επιθυμητών δεδομένων που φορτώθηκαν στα tables της βάσης δεδομένων σε αρχεία csv,
# χρήση του encoding utf-8 για αναγνώριση των ελληνικών χαρακτήρων που περιέχονται σε ορισμένα tables
def export_to_csv():

    mydb = sqlite3.connect('tourism.db')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Arrivals_Per_Year")
    with open("arrivals_per_year.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in mycursor.description])
        csv_writer.writerows(mycursor)

    mycursor.execute("SELECT * FROM Arrivals_Per_Country ORDER BY arrivals DESC")
    with io.open("arrivals_per_country.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in mycursor.description])
        csv_writer.writerows(mycursor)

    mycursor.execute("SELECT * FROM Arrivals_Per_Mean_Of_Transport")
    with io.open("arrivals_per_mean_of_transport.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in mycursor.description])
        csv_writer.writerows(mycursor)

    mycursor.execute("SELECT * FROM Arrivals_Per_Quarter")
    with io.open("arrivals_per_quarter.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in mycursor.description])
        csv_writer.writerows(mycursor)

    mydb.close()


def graph_arrivals_per_year():
    # Ανάγνωση του αρχείου csv
    table = pd.read_csv('arrivals_per_year.csv')

    # Δημιουργία του bar chart
    plt.bar(x=np.arange(1, 5), height=table['total_arrivals'])

    # Τίτλος για το bar chart
    plt.title('Συνολικές αφίξεις τουριστών ανά χρονιά (2011-2014)')

    # Ονοματοδοσία του άξονα x με τα ονόματα των αντίστοιχων χρονιών
    plt.xticks(np.arange(1, 5), table['year'])

    # Τίτλοι για τους άξονες x και y
    plt.xlabel('Χρονιά')
    plt.ylabel('Συνολικές αφίξεις')

    # Εμφάνιση του τελικού γραφήματος
    plt.show()


def graph_arrivals_per_country():
    # Ανάγνωση του αρχείου csv
    table = pd.read_csv('arrivals_per_country.csv')

    # Δημιουργία του bar chart
    plt.bar(x=np.arange(1, 56), height=table['arrivals'])

    # Τίτλος για το bar chart
    plt.title('Αφίξεις τουριστών ανά χώρα (2011-2014)')

    # Ονοματοδοσία του άξονα x με τα ονόματα των χωρών και εμφάνισή τους σε περιστροφή 90 μοιρών κάτω από κάθε bar
    plt.xticks(np.arange(1, 56), table['country'], rotation=90)

    # Τίτλοι για τους άξονες x και y
    plt.xlabel('Χώρα')
    plt.ylabel('Αφίξεις')

    # Εμφάνιση του τελικού γραφήματος
    plt.show()


def graph_arrivals_per_mean_of_transport():
    # Ανάγνωση του αρχείου csv
    table = pd.read_csv('arrivals_per_mean_of_transport.csv')

    # Δημιουργία του bar chart
    plt.bar(x=np.arange(1, 5), height=table['arrivals'])

    # Τίτλος για το bar chart
    plt.title('Αφίξεις τουριστών ανά μέσο μεταφοράς (2011-2014)')

    # Ονοματοδοσία του άξονα x με τα ονόματα των μέσων μεταφοράς
    plt.xticks(np.arange(1, 5), table['mean_of_transport'])

    # Τίτλοι για τους άξονες x και y
    plt.xlabel('Μέσο μεταφοράς')
    plt.ylabel('Αφίξεις')

    # Εμφάνιση του τελικού γραφήματος
    plt.show()


def graph_arrivals_per_quarter():
    # Ανάγνωση του αρχείου csv
    table = pd.read_csv('arrivals_per_quarter.csv')

    # Δημιουργία του bar chart
    plt.bar(x=np.arange(1, 17), height=table['arrivals'])

    # Τίτλος για το bar chart
    plt.title('Αφίξεις τουριστών ανά τρίμηνο (2011-2014)')

    # Ονοματοδοσία του άξονα x με τα ονόματα των αντίστοιχων τριμήνων και εμφάνισή τους σε περιστροφή 45 μοιρών
    plt.xticks(np.arange(1, 17), table['quarter'], rotation=45)

    # Τίτλοι για τους άξονες x και y
    plt.xlabel('Τρίμηνο')
    plt.ylabel('Αφίξεις')

    # Εμφάνιση του τελικού γραφήματος
    plt.show()


download_excels()
arrivals_per_year()
countries_dict = countries_arrivals()
transport_dict = means_of_transport()
quarter_dict = arrivals_per_quarter()
import_to_DB()
export_to_csv()

print("  _____       _   _                    _____           _           _      ___  _    ___   ___  ")
print(" |  __ \     | | | |                  |  __ \         (_)         | |    |__ \| |  |__ \ / _ \ ")
print(" | |__) |   _| |_| |__   ___  _ __    | |__) | __ ___  _  ___  ___| |_      ) | | __  ) | | | |")
print(" |  ___/ | | | __| '_ \ / _ \| '_ \   |  ___/ '__/ _ \| |/ _ \/ __| __|    / /| |/ / / /| | | |")
print(" | |   | |_| | |_| | | | (_) | | | |  | |   | | | (_) | |  __/ (__| |_    / /_|   < / /_| |_| |")
print(" |_|    \__, |\__|_| |_|\___/|_| |_|  |_|   |_|  \___/| |\___|\___|\__|  |____|_|\_\____|\___/ ")
print("         __/ |                                       _/ |                                      ")
print("        |___/                                       |__/                                       ")

# Κεντρικό Μενού της εφαρμογής, ανάλογα με την επιλογή του χρήστη εμφανίζεται το αντίστοιχο γράφημα στην οθόνη
answer = True
while answer:
    print("\nAPPLICATION MENU")
    print("===================================")
    print("1. Tourist Arrivals per Year")
    print("2. Tourist Arrivals per Country")
    print("3. Tourist Arrivals pen Mean of Transport")
    print("4. Tourist Arrivals per Quarter of Year")
    print("OR\nPress 5 to exit the application")
    answer = input("\nSelect: ")
    if answer == "1":
        graph_arrivals_per_year()
    elif answer == "2":
        graph_arrivals_per_country()
    elif answer == "3":
        graph_arrivals_per_mean_of_transport()
    elif answer == "4":
        graph_arrivals_per_quarter()
    elif answer == "5":
        print("Goodbye!")
        break
    else:
        print("\nInvalid option! Try again!")