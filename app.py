# app.pyhttps://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingModuleSource
from flask import Flask, request, jsonify, render_template,url_for,redirect,session
import os
from src.process.query.query import input_query
from src.process.custom.interpret_sql import interpret_headers, interpret_rows
from src.process.custom.organize_pdf import json_to_py
from src.process.custom.pdf_compiler import pdf_ready
from src.process.custom.pdf_create_sql import pdf_create_main
from src.process.pdf.form_info import form_process
from src.process.pdf.pdf_process import generate_pdf
from src.process.auth.login_process import verify_process
from src.process.guideline_table.display_func import main_headers,rows_display

import time
import json

app = Flask(__name__,template_folder='src/templates')
app.secret_key = 'e^6n>C(fsT%`Ku`p9Tjs0na/U{o%T7;#ecK,X{fa?jjO5$6k~lEND]D8/)U#4;!'

#Define Display Loaders
pdf_prog = 1 
pdf_message = 'Processing'



@app.route('/')
def index():
    if session.get('email') is None:
        return redirect(url_for('login'))
    return redirect('/pdf-generator')

# AUTHENTICATION
@app.route("/login", methods=['GET'])
def login():
    if session.get('email') is None:
        title = 'Login'
        return render_template("pages/auth/login.html",title=title)
    return redirect('/pdf-generator')

#VERIFY
@app.route("/verify", methods=['POST'])
def verify():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        response = verify_process(email,password)
        print("Session data:", session)
        return jsonify(response)
      
    except Exception as e:
        return jsonify({'status': 'error','message': str(e)}), 500

#LOGOUT
@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    print(session)
    return redirect('/')


# PDF GENERATOR VIEW
@app.route('/pdf-generator', methods=['GET'])
def pdf_generator():
    print(session)
    if session.get('email') is None:
        return redirect('/')
   
    res             = form_process()
    file_formats    = ['MP4','MOV','AVI','WMV','WebM','FLV','AVCHD']
    # visuals         = ['pop-ups','fade ins','slide ins']
    text_display    = ["Processing...", "Please Wait...", "Creating PDF Guidelines..", "Info : The more you select Guidelines....The more it will takes too long to generate"]
    branding_colors = ['#000000','#FFFFFF','#9cf542','#42d4f5']
    frame_rate      = ['23.976 fps','Same as Source Footage']
    title           = 'Amora Auto PDF'
    name            = session.get('name')
    json_object     = json.dumps(res, indent = 4) 
    # print(json_object)
    return render_template("pages/generate_form/generate_form.html",res=res,text_display=text_display ,file_formats=file_formats,branding_colors=branding_colors,frame_rate=frame_rate,title=title,name=name)

#AUTO PDF PROCESS
@app.route('/pdf-generator-process', methods=['POST'])
def pdf_generator_process():
    try:
        data = request.json
        try:
            res = generate_pdf(data)
            return jsonify(res)
        except Exception as e:
            return jsonify({'status': 'error','message': str(e)}), 500
    except Exception as e:
        return jsonify({'status': 'error','message': str(e)}), 500

#AUTO PDF PROGRESS

@app.route('/update-pdf-progress', methods=['POST'])
def update_pdf_progress():
    global pdf_prog
    global pdf_message
    data = request.get_json()
    pdf_prog = data.get('pdf_prog') 
    pdf_message = data.get('pdf_message')
    return jsonify({"status": "success", "pdf_prog": pdf_prog ,'pdf_message' : pdf_message})



@app.route('/pdf-progress', methods=['GET'])
def pdf_progress():
    global pdf_prog
    global pdf_message
    return jsonify({"progress": pdf_prog,"message" : pdf_message})





                        #ALL GUIDELINES
#->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->


@app.route('/all-guidelines', methods=['GET'])
def all_guidelines():
    try:
            # all columns headers = "show columns from guidelines"
        headers = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'guidelines' AND COLUMN_NAME IN ('g_id', 'g_name', 'g_link', 'g_category', 'mandatory');"
        headers_result = main_headers(headers)
        rows = "select g_id ,g_name, g_link, g_category, mandatory from guidelines"
        rows_result = rows_display(rows)
    except Exception as e:
        result = f"Submit a query to get results. Error: {e}"
        headers_result = ""
        rows_result = ""
    return render_template("pages/guideline_table/index.html", headers=headers_result, rows=rows_result)  




@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.json.get('data')  # Retrieve the data from the JSON payload
        fName = request.json.get('fName')
        style = request.json.get('style')

        if data is None:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        # Convert each guide ID in the list to uppercase
        
        guides_full = json_to_py(data)
        guides_ready = pdf_ready(guides_full)
        
        useful_columns = pdf_create_main(guides_ready)

        from src.process.guideline_pdf.pdf_html import create_pdf_from_pages

        print(fName)

        pdf_confirmation = create_pdf_from_pages(useful_columns, fName, style)
        

        #print(f'it should have been confirmed from {pdf_confirmation}')
        print(pdf_confirmation)

        return jsonify(pdf_confirmation)


    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/processQa', methods=['POST'])
def process_data_qa():
        try:
            from src.process.guideline_pdf import qa_pdf

            data = request.json.get('data')
            fName = request.json.get('fName')
            style = request.json.get('style')
            if data is None:
                return jsonify({'status': 'error', 'message': 'No Data Provided..'})


            guides_full = json_to_py(data)
            guides_ready = pdf_ready(guides_full)
            print(guides_ready)
            useful_columns = pdf_create_main(guides_ready)
            print("hello")
            pdf_confirmation = qa_pdf(useful_columns, fName, style)
            return jsonify(pdf_confirmation)

        except Exception as e:
            return jsonify(({'status': 'error', 'message': str(e)}))


progress = "0%"  # Store the progress here

@app.route('/update_progress', methods=['POST'])
def update_progress():
    global progress
    data = request.get_json()
    progress = data.get('amount', '0%')
    return jsonify({"status": "success", "amount": progress})


@app.route('/get_progress', methods=['GET'])
def get_progress():
    global progress
    return jsonify({"progress": progress})

if __name__ == '__main__':
    app.run(debug=True)
