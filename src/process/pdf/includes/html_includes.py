from src.css.pdf_css.notion_blocks import notion_block_style

def html_boilerplate_start(pdf_general_style):
    boilerplate = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> MyTitle </title>
    <style>  
        
        {pdf_general_style} 
        {notion_block_style}
    </style>
    <link href="../pdf_css/notion_blocks.css" rel="stylesheet">    
    </head>
    <body>

    """
    return boilerplate


def colors_html(colors):
    all_html_content = ''
    if(len(colors)):
        for row in colors:
            all_html_content   += f"""<div style="branding-color-container-col">
                                            <span style="margin: 0px; padding: 0px; text-align:center;">#{row}</span>
                                            <div style="background-color: #{row}; width:80px;padding-bottom: 35px;margin: 5px;"></div>
                                        </div>"""
    all_html_content += '</div>'

    return all_html_content
    