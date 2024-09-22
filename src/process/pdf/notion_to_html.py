from src.credentials.cred import notion_headers,bucket_name
import requests

def fetch_page_content(notion_id):
    try:
        url = f"https://api.notion.com/v1/blocks/{notion_id}/children"
        response = requests.get(url, headers=notion_headers)
        response.raise_for_status()
        print(f"Fetched content for page ID {notion_id}")
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Error fetching page content for page ID {notion_id}: {e}")
        return {"results": []}
    
def rich_text_to_html(rich_text):
        html_content = ""
        for text in rich_text:
            if text['type'] == 'text':
                if 'link' in text['text'] and text['text']['link']:
                    url = text['text']['link']['url']
                    html_content += f'<a href="{url}">{text["text"]["content"]}</a>'
                else:
                    html_content += str(text['text']['content'])
        return html_content

def fetch_block_children(block_id):
        try:
            url = f"https://api.notion.com/v1/blocks/{block_id}/children"
            response = requests.get(url, headers=notion_headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching block children for block ID {block_id}: {e}")
            return {"results": []}


def notion_blocks_to_html(blocks):
    
    html_content = ""
    inside_image_container = False
    
    for i, block in enumerate(blocks):
        block_type = block.get("type", "unsupported")
        if block_type == "paragraph":
            if inside_image_container:
                html_content += "</div>"
                inside_image_container = False
            if block['paragraph']['rich_text']:
                html_content += f"<p>{rich_text_to_html(block['paragraph']['rich_text'])}</p>"
            else:
                html_content += "<p></p>"
        elif block_type in ["heading_1", "heading_2", "heading_3"]:
            if inside_image_container:
                html_content += "</div>"
                inside_image_container = False
            level = block_type[-1]
            rich_text = block[block_type].get('rich_text', [])
            if rich_text:
                html_content += f"<h{level} class='h{level}'>{rich_text_to_html(rich_text)}</h{level}>"  
            
            toggle_heading = block.get('heading_1', [])
            if toggle_heading:
               if toggle_heading.get("is_toggleable"):
                    child_blocks = fetch_block_children(block.get('id'))["results"]
                    html_content += notion_blocks_to_html(child_blocks)
                 
        
        elif block_type == "image":
            if not inside_image_container:
                html_content += '<div class="image-container">'
                inside_image_container = True

            image_data = block.get("image", {})
            image_url = image_data.get("file", {}).get("url", "")
            if not image_url:
                continue  # Skip this block if no URL is found

            # Upload the image to Google Cloud Storage and get public URL
            
            # public_url = upload_image_to_bucket(image_url, bucket_name)

            next_block_type = blocks[i + 1].get("type", "unsupported") if i + 1 < len(blocks) else None
            if next_block_type == "image":
                html_content += f'<img src="{image_url}" alt="Image" class="half">'
            else:
                html_content += f'<img src="{image_url}" alt="Image" class="full">'
                if i + 1 < len(blocks) and blocks[i + 1].get("type", "unsupported") == "paragraph":
                    html_content += '<div class="text">'
                    html_content += f"<p>{rich_text_to_html(blocks[i + 1]['paragraph']['rich_text'])}</p>"
                    html_content += '</div>'


        elif block_type == "video":
            if inside_image_container:
                html_content += "</div>"
                inside_image_container = False
            video_url = block["video"].get("external", {}).get("url")
            if not video_url:
                video_url = block["video"].get("file", {}).get("url")
            if video_url:
                html_content += f'<p><a href="{video_url}">Watch Video</a></p>'
        
        
        
        elif block_type == "file":
            if inside_image_container:
                html_content += "</div>"
                inside_image_container = False
            file_url = block["file"].get("external", {}).get("url")
            if not file_url:
                file_url = block["file"].get("file", {}).get("url")
            if file_url:
                html_content += f'<p><a href="{file_url}">Download File</a></p>'
        
        
        
        elif block_type in ["column_list", "column", "toggle", "bulleted_list_item", "numbered_list_item"]:
            if inside_image_container:
                html_content += "</div>"
                inside_image_container = False
            if block['has_children']:
                child_blocks = fetch_block_children(block['id'])["results"]
                html_content += notion_blocks_to_html(child_blocks)
        
      
        
        else:
            print(f"Unsupported block type: {block_type}")

    
    if inside_image_container:
        html_content += "</div>"

    html_content += """
    </body>
    </html>
    """


    return html_content
