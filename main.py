import urllib.request
from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
import psycopg2

app = Flask(__name__)

# Set up Postgres database connection and cursor.
t_host = "localhost"
t_port = "5432"  # default postgres port
t_dbname = "scrapingdb"
t_user = "postgres"
t_pw = "eBaye1er"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor()


# Scrape accommodations
def scrape_accommodations():
    soup = BeautifulSoup(urllib.request.urlopen(
        'https://www.journaldunet.com/management/ville/classement/villes/hlm').read(), 'lxml')

    tbody = soup('tbody')[0].find_all('tr')

    for row in tbody:
        cols = row.findChildren(recursive=False)
        cols = [element.text.strip() for element in cols]
        if cols:
            col1 = cols[0]
            col2 = cols[1]
            col3 = cols[2]

            query = "INSERT INTO table_city_one(rang, ville, taux) VALUES (%s, %s, %s);"
            data = (col1, col2, col3)

            # Trap errors for opening the file
            try:
                db_cursor.execute(query, data)
                db_conn.commit()
            except psycopg2.Error as e:
                t_msg = "Database error: " + e + "/n open() SQL: " + query
                print(t_msg)

    # Success!
    # Show a message to user.
    t_msg = "Successful scrape!"
    print(t_msg)

    # Clean up the cursor and connection objects
    # db_cursor.close()
    # db_conn.close()


 # checking the database
sql = "SELECT COUNT(*) FROM table_city_one;"
db_cursor.execute(sql)
items = db_cursor.fetchall()
# Calling the scraping function
if items == 0:
    scrape_accommodations()


def scrape_cout_vie():
    soup = BeautifulSoup(urllib.request.urlopen(
        'https://www.studyrama.com/vie-etudiante/les-dernieres-news-du-monde-etudiant/cout-de-la-vie-etudiante-2020-paris-est-toujours-la-107254').read(), 'lxml')

    tbody = soup('tbody')[0].find_all('tr')

    for row in tbody:
        cols = row.findChildren(recursive=False)
        cols = [element.text.strip() for element in cols]
        if cols:
            col1 = cols[0]
            col2 = cols[1]
            col3 = cols[2]

            query = "INSERT INTO cout_vie(classement, ville, cout) VALUES (%s, %s, %s);"
            data = (col1, col2, col3)

            # Trap errors for opening the file
            try:
                db_cursor.execute(query, data)
                db_conn.commit()
            except psycopg2.Error as e:
                t_msg = "Database error: " + e + "/n open() SQL: " + query
                print(t_msg)

    # Success!
    # Show a message to user.
    t_msg = "Successful scrape!"
    print(t_msg)


# checking the database
sql = "SELECT COUNT(*) FROM cout_vie;"
db_cursor.execute(sql)
items = db_cursor.fetchall()
# Calling the scraping function
if items == 0:
    scrape_cout_vie()


@app.route('/')
def home():
    # Fetch all data of the database
    sql = "SELECT * FROM table_city_one;"
    db_cursor.execute(sql)
    items = db_cursor.fetchall()
    # db_cursor.close()
    # db_conn.close()

    return render_template("index.html", items=items)


@app.route('/immigres')
def immigres():
    sql = "SELECT * FROM table_people ORDER BY id ASC;"
    db_cursor.execute(sql)
    datas = db_cursor.fetchall()

    return render_template("pop_immigrees.html", datas=datas)


@app.route('/cout')
def cout():
    sql = "SELECT * FROM cout_vie;"
    db_cursor.execute(sql)
    my_datas = db_cursor.fetchall()

    return render_template("cout_vie.html", my_datas=my_datas)


if __name__ == "__main__":
    app.run(debug=True)