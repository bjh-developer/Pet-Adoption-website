from flask import Flask, render_template, redirect, request, url_for
import sqlite3, base64

app = Flask(__name__)

@app.route("/")
def reroute():
    return redirect('/home')

@app.route("/home")
def homePage():
    return render_template("/home.html")

@app.route("/aboutus")
def aboutusPage():
    return render_template("/aboutus.html")

@app.route("/profile", methods=['GET', 'POST'])
def profilePage():
    global records, email, password
    if request.method == 'POST':
        email_interested = request.form.get('email_interested')
        id = request.form.get('id')
        sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
        cursor = sqliteConnection.execute("UPDATE Animal SET AdoptedBy=?, OwnedBy=?, InterestedBy=? WHERE Id=?", (email_interested, None, None, id))
        sqliteConnection.commit()
        records = cursor.fetchall()
        cursor.close()

    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    for row in records:
        email = row[0]
        password = row[1]
    cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE OwnedBy = ?", (email,))
    records = cursor.fetchall()
    idList_petsForAdoption = []
    nameList_petsForAdoption = []
    photoList_petsForAdoption = []
    genderList_petsForAdoption = []
    ageList_petsForAdoption = []
    feeList_petsForAdoption = []
    writeUpList_petsForAdoption = []
    interestedbyList_petsForAdoption = []
    for row in records:
        idList_petsForAdoption.append(row[0])
        nameList_petsForAdoption.append(row[1])
        genderList_petsForAdoption.append(row[2])
        photoList_petsForAdoption.append(row[3])
        ageList_petsForAdoption.append(row[4])
        feeList_petsForAdoption.append(row[5])
        writeUpList_petsForAdoption.append(row[6])
        interestedbyList_petsForAdoption.append(row[10])
    for photo in photoList_petsForAdoption:
        photoList_petsForAdoption[photoList_petsForAdoption.index(photo)] = (base64.b64encode(photo)).decode('ascii')

    cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE InterestedBy = ?", (email,))
    records = cursor.fetchall()
    idList_interested = []
    nameList_interested = []
    photoList_interested = []
    genderList_interested = []
    ageList_interested = []
    feeList_interested = []
    writeUpList_interested = []
    ownedbyList_interested = []
    for row in records:
        idList_interested.append(row[0])
        nameList_interested.append(row[1])
        genderList_interested.append(row[2])
        photoList_interested.append(row[3])
        ageList_interested.append(row[4])
        feeList_interested.append(row[5])
        writeUpList_interested.append(row[6])
        ownedbyList_interested.append(row[8])
    for photo in photoList_interested:
        photoList_interested[photoList_interested.index(photo)] = (base64.b64encode(photo)).decode('ascii')
    cursor.close()

    cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE AdoptedBy = ?", (email,))
    records = cursor.fetchall()
    idList_adopted = []
    nameList_adopted = []
    photoList_adopted = []
    genderList_adopted = []
    ageList_adopted = []
    feeList_adopted = []
    writeUpList_adopted = []
    adoptedbyList_adopted = []
    for row in records:
        idList_adopted.append(row[0])
        nameList_adopted.append(row[1])
        genderList_adopted.append(row[2])
        photoList_adopted.append(row[3])
        ageList_adopted.append(row[4])
        feeList_adopted.append(row[5])
        writeUpList_adopted.append(row[6])
        adoptedbyList_adopted.append(row[9])
    for photo in photoList_adopted:
        photoList_adopted[photoList_adopted.index(photo)] = (base64.b64encode(photo)).decode('ascii')
    cursor.close()

    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE OwnedBy=?", (email,))
    records = cursor.fetchall()
    idList_edit = []
    nameList_edit = []
    for row in records:
        idList_edit.append(row[0])
        nameList_edit.append(row[1])
    cursor.close()
    return render_template('/profile.html', email=email, password=password, nameList_interested=nameList_interested,
                        genderList_interested=genderList_interested, photoList_interested=photoList_interested, ageList_interested=ageList_interested,
                        feeList_interested=feeList_interested, writeUpList_interested=writeUpList_interested, ownedbyList_interested=ownedbyList_interested,
                        nameList_petsForAdoption=nameList_petsForAdoption, genderList_petsForAdoption=genderList_petsForAdoption, photoList_petsForAdoption=photoList_petsForAdoption,
                        ageList_petsForAdoption=ageList_petsForAdoption, feeList_petsForAdoption=feeList_petsForAdoption, writeUpList_petsForAdoption=writeUpList_petsForAdoption,
                        interestedbyList_petsForAdoption=interestedbyList_petsForAdoption, idList_petsForAdoption=idList_petsForAdoption, idList_interested=idList_interested,
                        idList_adopted=idList_adopted, nameList_adopted=nameList_adopted, photoList_adopted=photoList_adopted,
                        genderList_adopted=genderList_adopted, ageList_adopted=ageList_adopted, feeList_adopted=feeList_adopted,
                        writeUpList_adopted=writeUpList_adopted, adoptedbyList_adopted=adoptedbyList_adopted, idList_edit=idList_edit, nameList_edit=nameList_edit)




@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    global records, email
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        return render_template("/login.html")
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = sqliteConnection.execute('SELECT * FROM Users WHERE email=? AND password=?', (email, password))
        sqliteConnection.commit()
        records = cursor.fetchall()
        if not records:
            cursor.close()
            return render_template('/login.html')
        else:
            cursor.close()
            return redirect("/profile")
            
        

@app.route("/petsforadoption")
def petsforadoptionPage():
    return render_template("/petsforadoption.html")

@app.route("/dogs", methods=['GET', 'POST'])
def dogsPage():
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE type='dog' AND OwnedBy IS NOT NULL")
        records = cursor.fetchall()
        idList_petsForAdoption = []
        nameList_petsForAdoption = []
        photoList_petsForAdoption = []
        genderList_petsForAdoption = []
        ageList_petsForAdoption = []
        feeList_petsForAdoption = []
        writeUpList_petsForAdoption = []
        ownedbyList_petsForAdoption = []
        for row in records:
            idList_petsForAdoption.append(row[0])
            nameList_petsForAdoption.append(row[1])
            genderList_petsForAdoption.append(row[2])
            photoList_petsForAdoption.append(row[3])
            ageList_petsForAdoption.append(row[4])
            feeList_petsForAdoption.append(row[5])
            writeUpList_petsForAdoption.append(row[6])
            ownedbyList_petsForAdoption.append(row[8])
        for photo in photoList_petsForAdoption:
            photoList_petsForAdoption[photoList_petsForAdoption.index(photo)] = (base64.b64encode(photo)).decode('ascii')
        cursor.close()
        return render_template("/dogs.html", idList_petsForAdoption=idList_petsForAdoption, nameList_petsForAdoption=nameList_petsForAdoption, genderList_petsForAdoption=genderList_petsForAdoption, photoList_petsForAdoption=photoList_petsForAdoption, ageList_petsForAdoption=ageList_petsForAdoption, feeList_petsForAdoption=feeList_petsForAdoption, writeUpList_petsForAdoption=writeUpList_petsForAdoption, ownedbyList_petsForAdoption=ownedbyList_petsForAdoption)
    else:
        email = request.form.get('email')
        id = request.form.get('id')
        cursor = sqliteConnection.execute("UPDATE Animal SET InterestedBy=? WHERE Id=?", (email, id,))
        sqliteConnection.commit()
        cursor.close()
        return redirect("/login")

@app.route("/cats", methods=['GET', 'POST'])
def catsPage():
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE type='cat' AND OwnedBy IS NOT NULL")
        records = cursor.fetchall()
        idList_petsForAdoption = []
        nameList_petsForAdoption = []
        photoList_petsForAdoption = []
        genderList_petsForAdoption = []
        ageList_petsForAdoption = []
        feeList_petsForAdoption = []
        writeUpList_petsForAdoption = []
        ownedbyList_petsForAdoption = []
        for row in records:
            idList_petsForAdoption.append(row[0])
            nameList_petsForAdoption.append(row[1])
            genderList_petsForAdoption.append(row[2])
            photoList_petsForAdoption.append(row[3])
            ageList_petsForAdoption.append(row[4])
            feeList_petsForAdoption.append(row[5])
            writeUpList_petsForAdoption.append(row[6])
            ownedbyList_petsForAdoption.append(row[8])
        for photo in photoList_petsForAdoption:
            photoList_petsForAdoption[photoList_petsForAdoption.index(photo)] = (base64.b64encode(photo)).decode('ascii')
        cursor.close()
        return render_template("/cats.html", idList_petsForAdoption=idList_petsForAdoption, nameList_petsForAdoption=nameList_petsForAdoption, genderList_petsForAdoption=genderList_petsForAdoption, photoList_petsForAdoption=photoList_petsForAdoption, ageList_petsForAdoption=ageList_petsForAdoption, feeList_petsForAdoption=feeList_petsForAdoption, writeUpList_petsForAdoption=writeUpList_petsForAdoption, ownedbyList_petsForAdoption=ownedbyList_petsForAdoption)
    else:
        email = request.form.get('email')
        id = request.form.get('id')
        cursor = sqliteConnection.execute("UPDATE Animal SET InterestedBy=? WHERE Id=?", (email, id,))
        sqliteConnection.commit()
        cursor.close()
        return redirect("/login")

@app.route("/addpet", methods=['GET', 'POST'])
def addpetPage():
    global records, email
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        return render_template("/addpet.html")
    else:
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        fee = request.form.get('fee')
        writeup = request.form.get('writeup')
        type = request.form.get('type')
        image1 = request.files['image1']
        image2 = request.files['image2']
        image3 = request.files['image3']
        image1 = image1.read()
        image2 = image2.read()
        image3 = image3.read()
        cursor = sqliteConnection.execute("INSERT INTO Animal (name, gender, photos, age, fee, writeUp, type, OwnedBy, AdoptedBy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, gender, image1, age, fee, writeup, type, email, None))
        sqliteConnection.commit()
        records = cursor.fetchall()
        cursor.close()
        return redirect("/profile")
    
@app.route("/selectpettoedit", methods=["GET", 'POST'])
def selectpettoedit():
    global records, email, id
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        cursor = sqliteConnection.execute("SELECT Id, name FROM Animal WHERE OwnedBy=?", (email,))
        records = cursor.fetchall()
        idList_edit = []
        nameList_edit = []
        for row in records:
            idList_edit.append(row[0])
            nameList_edit.append(row[1])
        cursor.close()
        return render_template("/selectpettoedit.html", idList_edit=idList_edit, nameList_edit=nameList_edit)
    else:
        id = request.form.get('pet_name_choice')
        return redirect('/editpet')

@app.route("/editpet", methods=['GET', 'POST'])
def editpetPage():
    global records, email, id
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        cursor = sqliteConnection.execute("SELECT * FROM Animal WHERE Id=?", (id,))
        sqliteConnection.commit()
        records = cursor.fetchall()
        idList_edit = []
        nameList_edit = []
        photoList_edit = []
        genderList_edit = []
        ageList_edit = []
        feeList_edit = []
        writeUpList_edit = []
        typeList_edit = []
        for row in records:
            idList_edit.append(row[0])
            nameList_edit.append(row[1])
            genderList_edit.append(row[2])
            photoList_edit.append(row[3])
            ageList_edit.append(row[4])
            feeList_edit.append(row[5])
            writeUpList_edit.append(row[6])
            typeList_edit.append(row[7])
        return render_template("/editpet.html", idList_edit=idList_edit, nameList_edit=nameList_edit, genderList_edit=genderList_edit,
                               photoList_edit=photoList_edit, ageList_edit=ageList_edit, feeList_edit=feeList_edit,
                               writeUpList_edit=writeUpList_edit, typeList_edit=typeList_edit)
    else:
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        fee = request.form.get('fee')
        writeup = request.form.get('writeup')
        type = request.form.get('type')
        image1 = request.files['image1']
        image2 = request.files['image2']
        image3 = request.files['image3']
        image1 = image1.read()
        image2 = image2.read()
        image3 = image3.read()
        cursor = sqliteConnection.execute("UPDATE Animal SET name=?, gender=?, photos=?, age=?, fee=?, writeUp=?, type=? WHERE Id=?",
                                          (name, gender, image1, age, fee, writeup, type, id,))
        sqliteConnection.commit()
        records = cursor.fetchall()
        cursor.close()
        return redirect("/profile")

@app.route('/deletepet', methods=['GET', 'POST'])
def deletepetPage():
    global records, email
    sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
    if request.method == 'GET':
        cursor = sqliteConnection.execute("SELECT Id, name FROM Animal WHERE OwnedBy=?", (email,))
        sqliteConnection.commit()
        records = cursor.fetchall()
        idList_edit = []
        nameList_edit = []
        for row in records:
            idList_edit.append(row[0])
            nameList_edit.append(row[1])
        cursor.close()
        return render_template("/deletepet.html", idList_edit=idList_edit, nameList_edit=nameList_edit)
    else:
        id = request.form.get('pet_name_choice')
        cursor = sqliteConnection.execute("DELETE FROM Animal WHERE Id=?", (id,))
        sqliteConnection.commit()
        records = cursor.fetchall()
        cursor.close()
        return redirect("/profile")

@app.route('/adduser', methods=['GET', 'POST'])
def adduserPage():
    if request.method == 'GET':
        return render_template('/adduser.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        sqliteConnection = sqlite3.connect('Web Application/Pet Adoption website/LovingPaws.db')
        cursor = sqliteConnection.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, password,))
        sqliteConnection.commit()
        cursor.close()
        return redirect("/login")

if __name__ == '__main__':
    app.run()