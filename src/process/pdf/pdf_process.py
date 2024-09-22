
import tempfile
import re

from src.process.custom.organizer import group_guidlines_by_category,categories,capitalize_category,get_data
from src.process.query.query import input_query
from src.process.query.query import query_info
from weasyprint import HTML
import os
from src.process.google_cloud.pdf_to_drive import upload_to_drive
from src.process.google_cloud.bucket_upload2 import upload_to_bucket, upload_image_to_bucket
from src.base_url import base_url
from src.process.pdf.notion_to_html import fetch_page_content,notion_blocks_to_html
from src.process.pdf.notion_process import get_notion_data

#Html
from src.process.pdf.includes.html_includes import html_boilerplate_start,colors_html
#CSS
from src.css.pdf_css.pdf_general_style import pdf_general_style
from src.css.pdf_css.notion_blocks import notion_block_style
import requests
import json


def pdf_page_one(data):
    
    #Defines
    branding_colors     = data.get('branding_colors')
    fName               = data.get('name')
    extra_information   = data.get('extra_information')  if data.get('extra_information') is not None else 'No Addtional Information'  
    file_format         = data.get('file_format')  if data.get('file_format') is not None else ' - ' 
    frame_rate          = data.get('frame_rate')
    pre_plug            = data.get('premiere_pro_plugins')
    af_ef_plug          = data.get('after_effects_plugins')
    ti_font             = data.get('title_font')
    ti_color            = data.get('title_color')
    cap_font            = data.get('caption_font')
    cap_color           = data.get('caption_color')
    reference           = data.get('reference')
    premiere_pro_plugins = None
    after_effects_plugins = None
    title_font = None
    caption_font = None
    inner_counter = 0
   

    if pre_plug != '':
        premiere_pro_plugins = query_info(None,pre_plug)
    if af_ef_plug != '':
        after_effects_plugins = query_info(None,af_ef_plug)
    if ti_font != '':
        title_font = query_info(None,ti_font)
    if cap_font != '':
        caption_font       =  query_info(None,cap_font)
    
    #INTRODUCTION
    all_html_content =  html_boilerplate_start(pdf_general_style)
    all_html_content += f'<h1 class="first_page_title">{fName}\'s Content Guidelines</h1>'
    all_html_content += f"""
    <div class="intro-page">
        <h3>Hi {fName}, these are your personalized editing guidelines made in our unique <u> Content editing style</u>.</h3>
        <p> Please make sure that you take the time to read everything attached, as we've spent a lot of time building this, and it is <u>crucial</u> these guides are followed. </p>
    </div>
    """

    #FILE FORMAT
    all_html_content += f'<div class="info1"><h4> File Format: <b>{file_format}</b></h4></div>'


    #Reference
    # all_html_content += f'<div class="info1"><h4> Reference:</h4><i><a href="{reference}">{reference}</i></a></div>'
    #FRAME RATE
    all_html_content += f'<div class="info1"><h4> Frame Rate: <b>{frame_rate}</b></h4></div>'

    #BRANDING COLOR
    
    all_html_content += '<div class="info1"><h4> Branding Color(s): </h4></div>'
    all_html_content += '<div class="branding-color-container">'
    all_html_content += colors_html(branding_colors)

    #PLUGINS REQUIRED
    all_html_content += '<div class="info1"> <h4 style="color:red;"> Plugins Required : </h4></div>'
    all_html_content += '<ul class="plugins">'
    if premiere_pro_plugins is not None:
        all_html_content += f"""<li><a href="{premiere_pro_plugins[2]}">{premiere_pro_plugins[1]}</a></li> """
    if after_effects_plugins is not None:
        all_html_content += f"""<li><a href="{after_effects_plugins[2]}">{after_effects_plugins[1]}</a></li> """
    all_html_content += '</ul>'

    #Title Font
    if isinstance(title_font,list):
        all_html_content += f'<div class="info1 fonts"><h4>Title Font: </h4><a href="{title_font[2]}">Download {title_font[1]}</a></div>'
    #Title Colors
        all_html_content += '<div class="info1"><h4> Title Color(s): </h4></div>'
        all_html_content += '<div class="branding-color-container">'
        all_html_content += colors_html(ti_color)

    #Captions
    if isinstance(caption_font,list):
        all_html_content += f'<div class="info1 fonts"><h4>Caption Font: </h4><a href="{caption_font[2]}">Download {caption_font[1]}</a></div>'
        all_html_content += '<div class="info1"><h4> Caption Color(s): </h4></div>'
        all_html_content += '<div class="branding-color-container">'
        all_html_content += colors_html(cap_color)
    #Extra Information
    all_html_content += f"""<div class="info1"><h4> Extra Information: </h4></div>
                                <p class="extra-information-text">{extra_information}</p>
                            """    

     #Reference
    all_html_content += f"""<div class="info1"><h4> Reference: </h4></div>
                                <p class="extra-information-text">For a complete reference to the video style these
                                guidelines refer to, please watch the video here: <i><a href="{reference}">{reference}</a></i></p> <br>
                            """    
    all_html_content += f"""<i><p style="color:red;">
                                WARNING: This is only a reference, and specific branding details may be different. 
                                Please make sure you go over all of the guidelines as well as the reference
                            <p></i>
                            """ 




    all_html_content += """
    
    <div class="page-break"> </div>
    """
    #CATEGORIES
    all_html_content += '<div class="info1" style="margin-top: 10px;"><h4>Categories: </h4></div>'
    all_html_content += '<div class="info1" style="margin-top: 5px; margin-left:10px"><i><p style="font-size: 15px;"> Glosarry: </p></i></div>'
    cats = categories(data)

     #Query Data from Database
    q_data              =  get_data(data)
    for_paging          = group_guidlines_by_category(q_data)
    
    all_html_content += '<ul class="categories">'

    for key_category, items in for_paging.items():
        caps = capitalize_category(key_category)
        all_html_content += f"""<li class="category_glossary"><span> {caps} </span></li> """
        
        for subcat,item in items.items():
            all_html_content += '<ul class="guideline_glossary">'
            all_html_content += f"""<li><span> {subcat} </span></li> """
            all_html_content += '</ul>'

            for row in item:
                docName         = row['data']["name"]
                key_cat         = row['data']["key_category"]
                paging          = row["paging"]

                all_html_content += '<ul class="docname_glossary">'
                all_html_content += f"""<li><span> {docName} </span><b>(Page {paging}</b>)</li> """
                all_html_content += '</ul>'
    
    all_html_content += '</ul>'
   
    all_html_content += """
    
    <div class="page-break"> </div>
    """
    

    return  all_html_content
   


def generate_pdf(data):
    inner_counter = 0
    fname               = data.get('name')
    #First Page
    all_html_content    = ''
    all_html_content    += pdf_page_one(data)
    
    disclaimer = f"""<i><p>Disclaimer : These are a general set of instructions to help guide editors
                    in making our content styles. Do not use these as a crutch. 
                    If the audio is low quality, if the video is low quality, do not use guidelines as an excuse. 
                    They are here to help you, not as something to 100{'%'} rely on. Use your intuition to solve problems when editing content
                    </p></i>
        """

    
    # Categories
    cats                = categories(data)
    cat_pages_created       = 1
    cat_total_pages     = len(cats)
    
    #Query Data from Database
    q_data              =  get_data(data)
    total_pages         = len(q_data)
    for row in cats:
        # Captalize Category Name
        caps = capitalize_category(row)
        
        #Category Header
        all_html_content += f'<div class="category-header">'
        all_html_content +=     f'<h1>{caps}</h1>'
        all_html_content += f'</div>'

        #Inner Loop Data
        for row1 in  q_data:

            #defining values
            link            = row1["link"]
            notion_id       = row1["notion_id"]
            docName         = row1["name"]
            category        = row1["category"]
            key_category    = row1["key_category"]

            
            #Condition if Equal to Category
            if(key_category == row):
                inner_counter += 1  # Increment the continuing counter
                

                #1. CREATING THE PAGE
                #page container
                all_html_content += f'<div class="page">'

#               #2. CREATING THE HEADER
                all_html_content += f"""
                    <div class="main_page-header">
                        <div class="disclaimer">
                            {disclaimer}
                        </div>
                        <div class="category_title">
                            {category}
                        </div> 
                        <div class="page_number"> 
                            Page {inner_counter} 
                        </div> 
                    </div> """

                all_html_content += f"""
                    <div class="document_title">
                        {docName  if isinstance(docName,str) else category} 
                    </div>
                """
             
                if notion_id is not None:
                    
                    #4. NOTION BLOCKS TO HTML  + BUCKET INFO

                    blocks_raw =  get_notion_data(notion_id, docName)
                    blocks = blocks_raw["results"]
                    all_html_content += notion_blocks_to_html(blocks)
                    print("passed notion blocks")
                   
                


                #5. closing the page div
                all_html_content += """</div>"""

                if inner_counter < total_pages:
                    all_html_content += """<div class="page-break"> </div>"""

                progress_data = {'pdf_prog' : inner_counter * 5 ,'pdf_message': f'Page {inner_counter} / {total_pages}'}
                try:
                    response = requests.post(base_url+'/update-pdf-progress', json=progress_data)
                    response.raise_for_status()
                    print(f"Progress update sent: {progress_data['pdf_message']}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to send progress update: {e}")


        cat_pages_created += 1

    all_html_content += """</div>"""
    all_html_content += """
    </body>
    </html>
    """


#     print(f"\n \n \n final html content compiled before creating pdf \n \n \n")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", dir="/tmp") as temp_html_file:
        temp_html_file_path = temp_html_file.name
        temp_html_file.write(all_html_content.encode('utf-8'))  # Ensure content is encoded properly

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir="/tmp") as temp_pdf_file:
        temp_pdf_file_path = temp_pdf_file.name
        HTML(string=all_html_content).write_pdf(temp_pdf_file_path)
        print("pdf temp file written")

    # Upload the generated PDF to Google Cloud Storage
    # with open(temp_pdf_file_path, 'rb') as pdf_file:
    #     file_content = pdf_file.read()
    # file_name = os.path.basename(temp_pdf_file_path)
    # upload_to_bucket(file_name, file_content, bucket_name)  # Correctly pass file_name
    # print(f"{file_name} written to bucket")

    #status
    progress_data = {'pdf_prog' : 90,'pdf_message': 'Uploading to Drive..'}
    try:
        response = requests.post(base_url+'/update-pdf-progress', json=progress_data)
        response.raise_for_status()
        print("Final progress update sent: drive%")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send final progress update: {e}")
    #  Upload the PDF to Google Drive
    # drive_folder_id = '164lbEWocPLZctVs3GXkdqWFF55yGDh5d'  # Your Google Drive folder ID
    # id = upload_to_drive(temp_pdf_file_path, f'Guidelines for {fname}.pdf', drive_folder_id)

    # os.remove(temp_html_file_path)
    # os.remove(temp_pdf_file_path)
    #  #Progress Complete
    # progress_data = {'pdf_prog' : 100,'pdf_message': 'Uploaded to Drive'}
    # try:
    #     response = requests.post(base_url+'/update-pdf-progress', json=progress_data)
    #     response.raise_for_status()
    #     print("Final progress update sent: 100%")
    # except requests.exceptions.RequestException as e:
    #     print(f"Failed to send final progress update: {e}")
    # return f"https://drive.google.com/file/d/{id}"

   
