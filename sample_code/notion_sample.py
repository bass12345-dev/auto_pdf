import requests
import os
import json
import time
import re
from src.credentials.cred import notion_headers,bucket_name
from src.process.pdf.notion_process import get_notion_data


# Fetch children of the collapsible block
def get_block_children(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=notion_headers)
    
    if response.status_code == 200:
        children_data = response.json()
        return children_data
    else:
        print(f"Error fetching block children: {response.status_code}")
        return None

# Get the collapsed content inside the block
# children = get_block_children('8e9ec26e-62b8-485c-8169-cf87cc6d80e4')

# if children:
#     print(json.dumps(children, indent=4))  # Nicely formatted output
# else:
#     print("No children found or an error occurred.")


def get_notion():
    blocks_raw =  fetch_page_content('3b0bd3f27a844a8fb5b3612dbd27145b')
    blocks = blocks_raw["results"]

    for i, block in enumerate(blocks) :
       block_type = block.get("type", "unsupported")
       if block_type == "heading_1":
            toggle = block.get("heading_1")
            if toggle:
            #    print(toggle.get("is_toggleable"))
               
                children = get_block_children(block.get('id'))["results"]
                json_object     = json.dumps(children, indent = 4) 
                print(json_object)


def fetch_page_content(notion_id):
    try:
        url = f"https://api.notion.com/v1/blocks/{notion_id}/children"
        response = requests.get(url, headers=notion_headers)
        response.raise_for_status()
        print(f"Fetched content for page ID {notion_id}")
        return response.json()
    except Exception as e:
        print(f"Error fetching page content for page ID {notion_id}: {e}")
        return {"results": []}
    
if __name__ == '__main__':
    get_notion()
