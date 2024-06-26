from urllib.request import urlopen, Request
import re
import json
import asyncio
import os

async def get_name_heros():

        # URL you want to make the request to
    url = 'https://epic7x.com/characters/'

    # Making the request using urllib
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(request)

    # Checking if the request was successful (response code 200)
    if response.getcode() == 200:
        # Reading the content of the response
        html = response.read().decode('utf-8')
        # print(html_read)
    else:
        raise Exception('Error in the request:', response.getcode())

    # Finding the script that contains the necessary information
    start_index = html.find('var CHARACTERS = ')
    end_index = html.find('jQuery("body").on("click", ".glossary-button"')
    script_content = html[start_index + 16:end_index]

    # Removing semicolon at the end if exists
    script_content = re.sub(r';\s*$', '', script_content)

    # Converting the script content to a Python object
    characters = json.loads(script_content)

    names = [ch["name"] for ch in characters]

    return names

async def get_urls():

    names = await get_name_heros();
    start_url = 'https://epic7x.com/characters/'
    urls = []

    for n in names:
        formatted_name = n.replace(' ', '-').lower()
        url = start_url + formatted_name + '/'
        urls.append(url)
    #print(urls)
    return (urls)


async def get_link_img_heros():
    
    urls = await get_urls();
    not_img = []
    char_links = []
    for url in urls:
        # Making the request using urllib
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(request)

        # Checking if the request was successful (response code 200)
        if response.getcode() == 200:
            # Reading the content of the response
            html = response.read().decode('utf-8')

        else:
            raise Exception('Error in the request:', response.getcode())

        # Finding the script that contains the necessary information
        start_index = html.find('var SELECTED_SKIN =')
        end_index = html.find('console.log(SKINS);')
        script_content = html[start_index + 21:end_index]
        
        if len(script_content) > 400:
            not_img_char = url.split('/')[-2].capitalize()
            not_img.append(not_img_char)
            continue
        
        # Removing semicolon at the end if exists
        script_content = re.sub(r"';\s*$", '', script_content)

        formatted_data = (url.split('/')[-2].capitalize(), script_content)
        char_links.append(formatted_data)

    return char_links, not_img

async def create_dir(name):

    path_script = os.path.dirname(os.path.abspath(__file__))  # Script path
    folder_name = name.replace("-", " ").title()
    content_folder = 'data'
    directory = os.path.join(path_script, content_folder, folder_name)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        return directory
    return directory

async def download_image():

    links, without_image = await get_link_img_heros();

    for l in links:
        name = l[0]
        url = l[1]
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(request)
        img = response.read()

        directory = await create_dir(name)
        
        with open(f'{directory}/{name}.webp', 'wb') as f: f.write(img) # Save the image in the indicated directory
        
    
    print(without_image)
    

asyncio.run(download_image())
