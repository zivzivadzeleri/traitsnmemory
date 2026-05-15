from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'


QUESTIONS = [
    "ლაპარაკის მოყვარული",
    "სხვების დადანაშაულებაზე ორიენტირებული",
    "საქმის საფუძვლიანად მკეთებელი",
    "დეპრესიული და სევდიანი",
    "ორიგინალური (უჩნდება ახალი იდეები)",
    "გულჩათხრობილი",
    "არა ეგოისტი (ეხმარება სხვებს)",
    "დაუდევარი",
    "მშვიდი, სტრესთან გამკლავების უნარიანი",
    "ცნობისმოყვარე",
    "ენერგიით სავსე",
    "დამთმობი",
    "სანდო თანამშრომელი",
    "დაძაბული",
    "გონებამახვილი, ღრმად მოაზროვნე",
    "ენთუზიაზმით სავსე",
    "მიმტევებელი",
    "მოუწესრიგებელი",
    "მშფოთვარე, მღელვარე",
    "მდიდარი წარმოსახვის მქონე",
    "სიწყნარის მოყვარული",
    "მიმნდობი",
    "ზარმაცი",
    "ემოციურად სტაბილური (რთულია მისი გაბრაზება)",
    "ინოვატორი",
    "საკუთარ შესაძლებლობებში დარწმუნებული",
    "ცივი და გულგრილი",
    "საქმის ბოლომდე მიმყვანი",
    "ცვალებადი ხასიათის მქონე",
    "შემოქმედების, ესთეტიკის მოყვარული",
    "მორცხვი, თავშეკავებული",
    "თითქმის ყველას მიმართ გულისხმიერი და კეთილი",
    "დავალების მარჯვედ შემსრულებელი",
    "გაწონასწორებული",
    "რუტინული, ერთფეროვანი საქმის მოყვარული",
    "გახსნილი და კომუნიკაბელური",
    "ზოგჯერ უხეში გარშემომყოფების მიმართ",
    "წინასწარ შედგენილი გეგმის შესაბამისად მოქმედი",
    "ადვილად გაღიზიანებადი",
    "იდეების გამომხატველი, აზრებით თამაშის მოყვარული",
    "ხელოვნებით ნაკლებად დაინტერესებული",
    "თანამშრომლობის მოყვარული",
    "საქმეზე ფოკუსირებული",
    "ხელოვნებაში, ლიტერატურასა და მუსიკაში გარკვეული"
]


@app.route('/consent', methods=['GET', 'POST'])
def consent():

    if request.method == 'POST':

        choice = request.form['consent']

        if choice == 'agree':
            return render_template('index.html')

        else:
            return render_template('declined.html')

    return render_template('consent.html')


@app.route('/')
def index():

    return redirect('/consent')


@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():

    if request.method == 'GET':

        return render_template(
            'questionnaire.html',
            questions=QUESTIONS
        )

    participant_id = f"P-{random.randint(10000, 99999)}"

    age = request.form['age']
    gender = request.form['gender']
    marital_status = request.form['marital_status']
    education = request.form['education']
    employment = request.form['employment']

    answers = []

    for i in range(1, 45):

        answers.append(int(request.form[f'q{i}']))

    extraversion = round(sum(answers[0:8]) / 8, 2)

    agreeableness = round(sum(answers[8:17]) / 9, 2)

    conscientiousness = round(sum(answers[17:26]) / 9, 2)

    neuroticism = round(sum(answers[26:35]) / 9, 2)

    openness = round(sum(answers[35:44]) / 9, 2)

    traits = {

        'ექსტრავერსია': extraversion,

        'თანხმობისკენ მიდრეკილება': agreeableness,

        'კეთილსინდისიერება': conscientiousness,

        'ნევროტიზმი': neuroticism,

        'ღიაობა გამოცდილებისადმი': openness
    }

    highest_trait = max(traits, key=traits.get)

    lowest_trait = min(traits, key=traits.get)

    session['participant_id'] = participant_id

    session['highest_trait'] = highest_trait

    session['lowest_trait'] = lowest_trait

    conn = sqlite3.connect(
        r'C:\Users\PC_LION\Desktop\bfi_app\database.db'
    )

    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO participants (

        participant_id,
        age,
        gender,
        marital_status,
        education,
        employment,

        q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,
        q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,
        q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,
        q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,
        q41,q42,q43,q44,

        extraversion,
        agreeableness,
        conscientiousness,
        neuroticism,
        openness,

        highest_task_total_rt,
        lowest_task_total_rt
    )

    VALUES (

        ?, ?, ?, ?, ?, ?,

        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?,

        ?, ?, ?, ?, ?,

        ?, ?
    )
    ''', (

        participant_id,
        age,
        gender,
        marital_status,
        education,
        employment,

        *answers,

        extraversion,
        agreeableness,
        conscientiousness,
        neuroticism,
        openness,

        0,
        0
    ))

    conn.commit()

    conn.close()

    return redirect('/task_intro/highest')


@app.route('/task_intro/<task_type>')
def task_intro(task_type):

    if task_type == 'highest':

        trait = session['highest_trait']

        next_url = '/task/highest'

    else:

        trait = session['lowest_trait']

        next_url = '/task/lowest'

    return render_template(
        'task_intro.html',
        trait=trait,
        next_url=next_url
    )


@app.route('/task/<task_type>')
def task(task_type):

    if task_type == 'highest':

        trait = session['highest_trait']

        order = 1

    else:

        trait = session['lowest_trait']

        order = 2

    trait_to_template = {

        'ექსტრავერსია': 'tasks/extraversion.html',

        'თანხმობისკენ მიდრეკილება': 'tasks/agreeableness.html',

        'კეთილსინდისიერება': 'tasks/conscientiousness.html',

        'ნევროტიზმი': 'tasks/neuroticism.html',

        'ღიაობა გამოცდილებისადმი': 'tasks/openness.html'
    }

    return render_template(
        trait_to_template[trait],
        participant_id=session['participant_id'],
        task_order=order,
        trait=trait
    )


@app.route('/save_task', methods=['POST'])
def save_task():

    data = request.get_json()

    participant_id = session['participant_id']

    responses = data['responses']

    task_order = int(data['task_order'])

    if task_order == 1:

        task_label = "დომინანტური ნიშნის დავალება"

    else:

        task_label = "მეორეხარისხოვანი ნიშნის დავალება"

    conn = sqlite3.connect(
        r'C:\Users\PC_LION\Desktop\bfi_app\database.db'
    )

    cursor = conn.cursor()

    for item in responses:

        cursor.execute('''
        INSERT INTO task_results (

            participant_id,
            task_trait,
            task_order,
            shown_word,
            stem,
            participant_response,
            accuracy,
            reaction_time

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        ''', (

            participant_id,
            task_label,
            task_order,
            item['shown_word'],
            item['stem'],
            item['response'],

            1 if item['response'].strip().lower()
            ==
            item['shown_word'].strip().lower()
            else 0,

            item['rt']

        ))

    total_rt = sum(item['rt'] for item in responses)

    if task_order == 1:

        cursor.execute('''
        UPDATE participants
        SET highest_task_total_rt = ?
        WHERE participant_id = ?
        ''', (

            total_rt,
            participant_id
        ))

    else:

        cursor.execute('''
        UPDATE participants
        SET lowest_task_total_rt = ?
        WHERE participant_id = ?
        ''', (

            total_rt,
            participant_id
        ))

    conn.commit()

    conn.close()

    if task_order == 1:

        return {
            "next_task": "/task_intro/lowest"
        }

    else:

        return {
            "next_task": "/final_results"
        }


@app.route('/final_results')
def final_results():

    participant_id = session['participant_id']

    conn = sqlite3.connect(
        r'C:\Users\PC_LION\Desktop\bfi_app\database.db'
    )

    cursor = conn.cursor()

    cursor.execute('''
    SELECT

        extraversion,
        agreeableness,
        conscientiousness,
        neuroticism,
        openness,

        highest_task_total_rt,
        lowest_task_total_rt

    FROM participants

    WHERE participant_id = ?
    ''', (

        participant_id,
    ))

    personality = cursor.fetchone()

    cursor.execute('''
    SELECT

        task_trait,
        SUM(reaction_time),
        SUM(accuracy)

    FROM task_results

    WHERE participant_id = ?

    GROUP BY task_trait
    ''', (

        participant_id,
    ))

    task_results = cursor.fetchall()

    conn.close()

    return render_template(

        'final_results.html',

        personality=personality,

        task_results=task_results,

        participant_id=participant_id
    )


@app.route('/admin')
def admin():

    conn = sqlite3.connect(
        r'C:\Users\PC_LION\Desktop\bfi_app\database.db'
    )

    cursor = conn.cursor()

    cursor.execute('''
    SELECT

        p.*,

        (
            SELECT SUM(accuracy)

            FROM task_results

            WHERE participant_id = p.participant_id

            AND task_order = 1
        ) as dominant_accuracy,

        (
            SELECT SUM(accuracy)

            FROM task_results

            WHERE participant_id = p.participant_id

            AND task_order = 2
        ) as secondary_accuracy

    FROM participants p

    ORDER BY p.created_at DESC
    ''')

    participants = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        participants=participants
    )


if __name__ == '__main__':

    app.run(debug=True)