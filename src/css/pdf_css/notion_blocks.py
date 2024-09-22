notion_block_style = """
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}
.image-container {
    margin-bottom: 20px;
    text-align: center;
}
.image-container img {
    max-width: 37%;
    max-height: 320px;
    height: auto;
    display: block;
    margin: 0 auto;
}
.image-container img.full {
    width: 37%;
}
.image-container img.half {
    width: 35%;
    margin: 0 2.5%;
}
.image-container .text {
    width: 45%;
    margin: 0 2.5%;
    display: inline-block;
    vertical-align: middle;
}
p, h1, h2, h3 {
    text-align: justify;
}
.h1 {
    font-size: 22px;
    text-align: center;
}
.h2 {
    font-size: 28px;
}
.h3 {
    font-size: 13px;
}
.document-title {
    font-family: "Brush Script MT";
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 24px;
    text-decoration: underline;
}
.main-category-title {
    font-family: cursive;
    font-size: 28px;
    font-weight: bold;
    margin-top: 40px;
    text-align: center;
}
.category-title-small {
    text-align: left;
    position: absolute;
    top: -100px;
    left: -100px;
}
.page-number {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 12px;
    color: gray;
}
.page {
    position: relative;
}

.category-header {
    height:50px;
    width: 100%;
    background-color:#003135;
    border-radius: 15px;
    margin-bottom: 20px;
    display: flex;
    flex-direction: row;
    align-items:center;
    justify-content:center;
}

.category-header h1 {
    text-align:center;
    color: #fff;
}
"""

