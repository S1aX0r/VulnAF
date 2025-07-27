from flask import Flask, request, render_template
import sqlite3, os
import xml.etree.ElementTree as ET
from ldap_mock import ldap_auth
from data.fake_mongo import nosql_auth

app = Flask(__name__)

# Init DB
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'f865b53623b121fd34ee5426c792e5c33af8c227')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    sql_result = cmd_result = xpath_result = ldap_result = nosql_result = ""

    if request.method == 'POST':
        form = request.form

        # SQL Injection
        try:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            query = f"SELECT * FROM users WHERE username='{form['sql_user']}' AND password='{form['sql_pass']}'"
            res = cur.execute(query).fetchone()
            conn.close()
            sql_result = "SQL Login Success" if res else "SQL Login Failed"
        except Exception as e:
            sql_result = str(e)

        # Command Injection
        try:
            target = form['cmd_target']
            cmd_result = os.popen(f"ping -c 1 {target}").read()
        except Exception as e:
            cmd_result = str(e)

        # XPath Injection
        try:
            tree = ET.parse('data/users.xml')
            root = tree.getroot()
            expr = f".//user[username='{form['xpath_user']}' and password='{form['xpath_pass']}']"
            user = root.find(expr)
            xpath_result = "XPath Auth Success" if user is not None else "XPath Auth Failed"
        except Exception as e:
            xpath_result = str(e)

        # LDAP Injection (mocked)
        try:
            ldap_result = ldap_auth(form['ldap_user'], form['ldap_pass'])
        except Exception as e:
            ldap_result = str(e)

        # NoSQL Injection (mocked)
        try:
            nosql_result = nosql_auth(form['nosql_user'], form['nosql_pass'])
        except Exception as e:
            nosql_result = str(e)

    return render_template("index.html", **locals())

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

