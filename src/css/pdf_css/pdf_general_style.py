pdf_general_style = """

@page {
            size: 8.5in 14in;  /* Legal page size */
            margin: 20px;      /* Margins around the page */
        }

h1.first_page_title{
    text-align: center !important;
}

.intro-page h2 {
    font-size: 25px;
    margin-bottom: 10px;
}
.intro-page p {
    font-size: 18px;
    margin-bottom: 10px;
}

.info1 {
    margin-bottom:7px;
}

.info1  h3,h4{
    margin:0 !important;
    padding: 0 !important;
}

.plugins li{
    margin: 7px;
}

.fonts{
    display : flex;
    flex-direction: row;
    
}

.fonts a{
    margin-left: 8px;
}



.guideline_glossary{
    list-style-type: circle;
    margin-left: 10px;
    margin-top: 10px
}

.docname_glossary{
    list-style-type: square;
    margin-left: 40px;
    margin-top: 10px
}



.categories .category_title{
   
    margin: 5px;
}

.categories .category_glossary span{
    font-size: 15px;
    font-weight: 600;
}

.extra-information-text {
    margin-top:0;
    margin-bottom:0;
    margin-left: 40px;
    padding:0;
}



.color-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.color-box {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 200px;
    height: 50px;
    margin: 10px;
    text-align: center;
    line-height: 50px;
    font-family: Arial, sans-serif;
    padding: 20px;
    color: #fff;
}
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}



.image-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
}
.image-container img {
    max-width: 50%;
    max-height: 300px;
    height: auto;
    display: block;
    margin: 0 auto;                
}
.image-container img.full {
    flex: 1 1 100%;
}
.image-container img.half {
    display: inline-block;
    width: 48%;
    margin: 1%;
    vertical-align: top;    }

    

p, h1, h2, h3 {
    text-align: justify;
}


.h1 {
    text-align: center;
    font-style: oblique;

    font-family: "Lucida Console"
    font-size: 25px;
}
.h2 {
    font-size: 20px;
}
.h3 {
    font-size: 15px;
}

.document_title {
    font-family: "Verdana";
    font-style: italic;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 24px;
}
.main-category-title {
    font-family: "URW Chancery", cursive;
    font-size: 28px;
    font-weight: bold;
    margin-top: 40px;
    text-align: center;
}

.extra-information{
   
    margin:0 !important;
    padding:0 !important;
    margin-top:20px !important;
}

.extra-information .extra-information-title {
    font-size:18px !important;
    font-weight:500 !important;
}
.extra-information p {
    margin-left:40px;
}





.image-container .text {
    width: 45%;
    margin: 0 2.5%;
    display: inline-block;
    vertical-align: middle;
}




.category_title {
    display: block;

    font-size: 20px;
    font-weight: 400;
    font-style: italic;
    margin: 0 auto;
}

.page-number {
    display: relative;
    position: absolute;
    right: 100px;
    top: 100px

}


.page-break {
    page-break-before: always;
}



.list {
    justify-content: space-between
    align-items: center;
}

.category_title_checklist {
    width: 100%;
    font-size: 30px;
    font: arial;
    font-style: oblique;
    padding-bottom: 10px;

}

.document_title_checklist {
    display: inline-block;
}


.qa_link {
    display: inline-block;
    margin-left: auto;
    text-align: right;
    width: 40px;

}

.branding-color-container{
    display:flex;
    flex-direction:row;
    row-gap:10px;
    margin-left: 40px; 
   
}

.branding-color-container-col{
    display:flex;
    flex-direction:column;
    column-gap:5px;
    row-gap:10px;
   
}

.disclaimer {
    text-align: center;
}

"""
