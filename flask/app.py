from flask import Flask, jsonify, request
import mysql.connector as mysql

db = mysql.connect(host='db', database='projectik', user='root', password='5a87sd8fsdfsEjwo', use_pure=False)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/api")
def api():
    people = [{'name': 'Alice', 'birth-year': 1986},{'name': 'Jeff', 'birth-year': 2012},
          {'name': 'Bob', 'birth-year': 1985}]
    return jsonify(people)

# Getting all branches
@app.route("/api/get/branches")
def getAllBranches():
   cur = db.cursor()
   cur.execute('''
               SELECT branch.*, logo FROM branch, company
               WHERE branch.id_company=company.id
               ''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'address': result[1],
                  'lat': result[2],
                  'lon': result[3],
                  'id_company': result[4],
                  'logo': result[5]
                  }
       payload.append(content)
       content = {}
   cur.close()
   return jsonify(result=payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Getting branches assign to company
@app.route("/api/get/branches/company/<id>")
def getBranchesCompany(id):
   cur = db.cursor()
   cur.execute('''
                SELECT branch.*, logo
                FROM branch, company
                WHERE id_company=%s
                AND company.id = branch.id_company
                ''',(id,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'address': result[1],
                  'lat': result[2],
                  'lon': result[3],
                  'id_company': result[4],
                  'logo': result[5]
                  }
       payload.append(content)
       content = {}
   cur.close()
   return jsonify(result=payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Getting all companies
@app.route("/api/get/companies")
def getAllCompanies():
   cur = db.cursor()
   cur.execute('''SELECT * FROM company''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'company_name': result[1],
                  'company_logo': result[2] }
       payload.append(content)
       content = {}
   cur.close()
   return jsonify(result=payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new branch
@app.route("/api/add/branch", methods = ['POST', 'GET'])
def addBranch():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "address" in request_data:
            address = request_data['address']
        else:
            return jsonify({"error": "Forgot something like ad...",}), 403

        if "lat" in request_data:
            lat = request_data['lat']
        else:
            return jsonify({"error": "Forgot something like la...",}), 403

        if "lon" in request_data:
            lon = request_data['lon']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "id_company" in request_data:
            id_company = request_data['id_company']
        else:
            return jsonify({"error": "Forgot something like co...",}), 403

        cur = db.cursor()
        cur.execute(''' INSERT INTO branch(address,lat,lon,id_company) VALUES(%s,%s,%s,%s) ''',
                    (address,lat,lon,id_company))
        db.commit()
        cur.close()
        return f"Done"


# Adding new company
@app.route("/api/add/company", methods = ['POST', 'GET'])
def addCompany():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "company_name" in request_data:
            company_name = request_data['company_name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403
        if "company_logo" in request_data:
            company_logo = request_data['company_logo']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' INSERT INTO company (name,logo) VALUES (%s,%s) ''',
                    (company_name,company_logo))
        db.commit()
        cur.close()
        return f"Done"


# Eding new company
@app.route("/api/edit/company", methods = ['POST', 'GET'])
def editCompany():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "company_id" in request_data:
            company_id = request_data['company_id']
        else:
            return jsonify({"error": "Forgot something like id...",}), 403
        if "company_name" in request_data:
            company_name = request_data['company_name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403
        if "company_logo" in request_data:
            company_logo = request_data['company_logo']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' UPDATE company SET name = %s, logo = %s WHERE id = %s ''',
                    (company_name,company_logo,company_id))
        db.commit()
        cur.close()
        return f"Done"

# Adding new vacancy
@app.route("/api/add/vacancy", methods = ['POST', 'GET'])
def addVacancy():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "id_position" in request_data:
            id_position = request_data['id_position']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403
        if "id_branch" in request_data:
            id_branch = request_data['id_branch']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        if "count" in request_data:
            count = request_data['count']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        if "salary" in request_data:
            salary = request_data['salary']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' INSERT INTO vacancy (id_position, id_branch, count, salary) VALUES (%s,%s,%s,%s) ''',
                    (id_position,id_branch,count,salary))
        db.commit()
        cur.close()
        return f"Done"

# Getting all vacancyes
@app.route("/api/get/vacancies")
def getAllVacancies():
   cur = db.cursor()
   cur.execute('''
               SELECT  id,
               (select name from position where id = id_position) position_name,
               (select address from branch where id = id_branch) address,
               (select lat from branch where id = id_branch) lat,
               (select lon from branch where id = id_branch) lon,
               (select name from company where id = (select id_company from branch where id = id_branch)) company_name,
               salary,
               count
               FROM vacancy
               ''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'position_name': result[1],
                  'address': result[2],
                  'lat': result[3],
                  'lon': result[4],
                  'company_name': result[5],
                  'salary': result[6],
                  'count': result[7] }
       payload.append(content)
       content = {}
   cur.close()
   return jsonify(result=payload), 200, {'Content-Type': 'application/json; charset=utf-8'}


# Searching all opened vacancyes
@app.route("/api/get/vacancies/search/<id>")
def searchAllVacancies(id):
   cur = db.cursor()
   cur.execute('''
               SELECT  id,
               (select name from position where id = id_position) position_name,
               (select address from branch where id = id_branch) address,
               (select lat from branch where id = id_branch) lat,
               (select lon from branch where id = id_branch) lon,
               (select name from company where id = (select id_company from branch where id = id_branch)) company_name,
               (select logo from company where id = (select id_company from branch where id = id_branch)) company_logo,
               salary,
               count
               FROM vacancy
               WHERE count > 0
               AND id_position = %s
               ''', (id,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'position_name': result[1],
                  'address': result[2],
                  'lat': result[3],
                  'lon': result[4],
                  'company_name': result[5],
                  'company_logo': result[6],
                  'salary': result[7],
                  'count': result[8] }
       payload.append(content)
       content = {}
   cur.close()
   return jsonify(result=payload), 200, {'Content-Type': 'application/json; charset=utf-8'}


# Eding vacancy
@app.route("/api/edit/vacancy/<id>", methods = ['POST', 'GET'])
def editVacancy(id):
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "id_position" in request_data:
            id_position = request_data['id_position']
        else:
            return jsonify({"error": "Forgot something like id...",}), 403
        if "id_branch" in request_data:
            id_branch = request_data['id_branch']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403
        if "count" in request_data:
            count = request_data['count']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        if "salary" in request_data:
            salary = request_data['salary']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' UPDATE vacancy SET id_position = %s, id_branch = %s, count = %s, salary = %s WHERE id = %s ''',
                    (id_position, id_branch, count, salary, id))
        db.commit()
        cur.close()
        return f"Done"


