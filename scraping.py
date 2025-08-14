import csv
import pandas as pd
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


"""
    aqua silkeborg [mangler liste på hjemmeside]
    blå planet [vanskelig hjemmeside at scrape]
<ok>blåvand zoo [mangler liste på hjemmeside] **ufuldstændig liste lavet**
    danmarks fuglezoo [mangler liste på hjemmeside]
<OK>dyrehaven engholm (nemmest at taste ind manuelt)
    enghave naturpark (ved brørup) [ikke umiddelbart en liste over dyr]
<OK>givskud zoo
<OK>glad zoo (lintrup) [nemmest at taste ind manuelt]
<ok>jylland park zoo  [nemmest at taste ind manuelt]
<ok>klokkerholm dyrepark selvtast
<OK>Knuthenborg Safari (nemmest at taste ind manuelt)
<OK>Krokodillezoo se: https://zooniverse.dk/zooniversitetet/generalle%20artikler/Krokodillezoo ved ikke om komplet og up to date.
<OK>københavn Zoo  se: https://www.zoo.dk/om-zoo/dyrene-i-zoo/forvaltning-af-dyrebestanden - kan næsten direkte kopieres ind i csv-fil.
<ok>Munkholm Zoo se: https://munkholmzoo.dk/galleri/ nok ikke komplet, selvtast
<OK>nordisk dyrepark (hobro)
<OK>odense zoo
<OK>odsherred zoo rescue [ikke umiddelbart en liste over dyr]  **ufuldstændig liste lavet**
<OK>pangaea sjælland
<OK>pangaea falster https://pangeapark.dk/falster/vores-dyr/
<OK>randers regnskov
<OK>ree park
<OK>Skandinavisk Dyrepark (tastet ind)
<OK>skærup zoo
    Fjord og Bælt Kerteminde [ikke umiddelbart en liste over dyr]
<ok>terrariet vissenbjerg
<OK>zoopark sydsjælland (nemmest at taste ind manuelt)
<OK>aalborg zoo
    hillerød mini zoo [virkelig lidt info]
    flamingo naturpark vemb midlertidigt lukket
<ok>nordsøakvariet vorupør (dårlig info på hjemmeside) **ufuldstændig liste lavet**
<ok>nordsøen oceanarium hirtshals (HELT SIKKERT UFULDSTÆNDIG LISTE)
    øresundsakvariet Helsingør (ser ud til ikke at findes)
<ok>kattegatcenteret grenå [også skrevet ind manuelt]


SE EVT DYREPARKER I DANMARK PÅ WIKIPEDIA
"""

dklettersreplace = [('aae','åe'), ('ae','æ'), ('oe','ø'), ('aa','å'), ('Ae','Æ'), ('Oe','Ø'), ('Aa','Å'),  
                    ('Årdvark','Aardvark'), ('Børged','Boerged'), ('Gøldis Abe', 'Goeldis Abe')]


def get_skaerup():
    skaerup = 'https://skaerup-zoo.dk/dyrene-i-parken/laer-om-dyrene'
    ignore = ['Udforsk Zoosamarbejde', 'Ring til Skærup Zoo', 'Send mail til Skærup Zoo', 'Se kontrolrapport for Skærup Zoo']
    browser.get(skaerup)
    time.sleep(random.randint(10,20))
    animal_links = browser.find_elements(By.CSS_SELECTOR, "a[title]")
    animal_names = [link.get_attribute("title") for link in animal_links]
    animal_names_clean = set(animal_names)-set(ignore)
    return [('Skærup Zoo', name) for name in animal_names_clean]

def get_odense():
    odense = "https://www.odensezoo.dk/besoeg-zoo/havens-dyr/"
    ignore = ['Havens dyr', 'Overnat i Camp Kiwara', 'Prøv en fodring', 'Rundvisning', 'Børnefødselsdag', 'Dyrepasser for en dag', 'Smagninger',
              'Adopter et dyr', 'Dansk', 'ZOOskole']
    browser.get(odense)
    time.sleep(random.randint(10,20))
    animal_links = browser.find_elements(By.CSS_SELECTOR, "a[href*='dyr'][title], a[href*='dyr'][title]")
    animal_names = [link.get_attribute("title") for link in animal_links]
    animal_names_clean = set(animal_names)-set(ignore)
    return[('Odense Zoo', name) for name in animal_names_clean]

def get_randers():
    randers = "https://www.regnskoven.dk/laerbevar/viden/dyreleksikon/"
    randers_next = "https://www.regnskoven.dk/nc/laerbevar/viden/dyreleksikon/side/"
    next_no = 0
    max_no = 12

    browser.get(randers)
    time.sleep(random.randint(10,20))
    done = False
    animal_names = []
    while (not done):
        animal_links = browser.find_elements(By.CSS_SELECTOR, "figure a[href*='/dyr/']")
        for link in animal_links:
            href = link.get_attribute("href")
            if href and '/dyr/' in href:
                # Extract animal name from URL: "agatudse" from "/dyr/agatudse/"
                animal_name = href.split('/dyr/')[-1].rstrip('/')
                # Clean up the name: replace hyphens with spaces and capitalize
                clean_name = animal_name.replace('-', ' ').title()
              
                for rule in dklettersreplace:
                    clean_name = clean_name.replace(rule[0], rule[1])
                animal_names.append(clean_name)
        next_no += 1
        newurl = randers_next + str(next_no) + '/'
        print('try to open:')
        print(newurl)
        try:
            browser.get(newurl)
            time.sleep(random.randint(5,8))
        except:
            done = True
        if next_no >= max_no:
            done = True
    return [('Randers Regnskov', name) for name in animal_names]

def getkroko():
    animal_names = []
    with open('data\krokodillezoo.txt', mode='r', encoding='utf-8', newline='') as file:
        content = file.read().split('\r')
        for line in content:
            if '-' in line:
                animal_names.append((line.split('-')[1]).strip().title())
            if '–' in line:
                animal_names.append((line.split('–')[1]).strip().title())
    return [('Krokodillezoo', name) for name in animal_names]

def getpangeafalster():
    url = 'https://pangeapark.dk/falster/vores-dyr/'
    browser.get(url)
    animal_names = []
    ignore = {'mertz', 'lysholt_hansen_16x9', 'mindb', 'hangry', 'Gulborgsund_kloakservice', 'Vesterskoven', 'K bertelsen', 'koihulen', 'valdemar',
              'Brdr.-Pedersen', 'metalcoloursverigeab_logo', 'container', 'bjarne 12', 'M Karrebæk', 'skousen', 'H biler_', 'MWM_Byg', 'Anlægsgartner',
              'rask el',  'AJCONSULT', 'møllegård', 'kj', 'Vores sponsorer', 'Rema 1000', 'Marina villa', 'Revisit consent button', 'Loxam', 'marius',
              'Stark', 'PH_Anlægsgartner', 'tegnebræt 1 kopier 2', 'Priser', 'COlour_plus', 'Sonny vvs', 'Følg os', 'ronni steinfeldt', 'tegnebræt 1 kopier 3',
              'tegnebræt 1 kopier',  'Toxværd entreprise',  'bera', 'jyske bank1', 'steens plante', 'paw', 'solsø', 'Pangea Park Falster', 'Køleteknik',
              'GLarmester_', 'rosenhoved dværgpapegøje', 'Gullev Designs', 'Close', 'Primatag-logo', 
              'Bygma_Nykoebing_F_adr_cmyk_hvid_ramme-1-9374df31e37b15a5adf44f9bc37a418a', 'Besøg os', 'atriumfonder', 'profil 1', 'Idebyg', 'murermester',
              'maler thrane logo', 'erikfrederiksenseftf-logo', 'Marielyst el', 'kian 1', 'nyt patrick heintz logo', 'Løve Apoteket'}

    # Method 1: Images with alt text
    images = browser.find_elements(By.CSS_SELECTOR, "img[alt]")
    for img in images:
        alt_text = img.get_attribute("alt")
        if alt_text and alt_text.strip():
            animal_names.append(alt_text.strip())

    # Method 2: Heading titles
    headings = browser.find_elements(By.CSS_SELECTOR, "h2.elementor-heading-title, h3.elementor-heading-title")
    for heading in headings:
        if heading.text.strip():
            animal_names.append(heading.text.strip())

    # Remove duplicates
    animal_names = list(set(animal_names) - ignore)
    return [('Pangea Falster', name) for name in animal_names]

def getpangeasjaelland():
    url = 'https://pangeapark.dk/vores-dyr/'
    browser.get(url)
    animal_names = []
    ignore = {'TilPangea', 'Tegnebraet-2-1-e1688983606584', 'KoegeSkilteCenter-2', 'Pangea Park Sjælland', 'Noerbjerg-2', 'kb stubferæsning',
               'A2Vent-2', 'dIGI_Hvid', 'LT_Hvidt', 'Følg os', 'Besøg os', 'Vores sponsorer', 'Priser'}

    # Method 1: Images with alt text
    images = browser.find_elements(By.CSS_SELECTOR, "img[alt]")
    for img in images:
        alt_text = img.get_attribute("alt")
        if alt_text and alt_text.strip():
            animal_names.append(alt_text.strip())

    # Method 2: Heading titles
    headings = browser.find_elements(By.CSS_SELECTOR, "h2.elementor-heading-title, h3.elementor-heading-title")
    for heading in headings:
        if heading.text.strip():
            animal_names.append(heading.text.strip())

    # Remove duplicates
    animal_names = list(set(animal_names) - ignore)
    return [('Pangea Sjælland', name.title()) for name in animal_names]

def get_aalborg():
    url = 'https://aalborgzoo.dk/vores-dyr/'
    browser.get(url)
    # Target links within zoo-box containers specifically
    animal_links = browser.find_elements(By.CSS_SELECTOR, "#zoo-animals-container .zoo-box a[href]")
    animal_names = []

    for link in animal_links:
        href = link.get_attribute("href")
        if href and href != "#":  # Skip empty or placeholder links
            animal_name = href.strip('/').split('/')[-1]
            clean_name = animal_name.replace('-', ' ').title()
            for rule in dklettersreplace:
                clean_name = clean_name.replace(rule[0], rule[1])
            animal_names.append(clean_name)

    return [('Aalborg Zoo', name) for name in animal_names]

def get_nordiskdyrepark():
    base_url = 'https://nordiskdyrepark.dk/'
    suburls = ['pungdyr/', 'krybdyr-og-padder/', 'insekter-spindlere-bloeddyr-mm/', 'primater/', 'hovdyr/',
        'fugle/', 'gnavere-og-kaniner/', 'rovdyr/'
        ]
    animal_names = []

    for suburl in suburls:
        browser.get(base_url + suburl)
        time.sleep(random.randint(8,12))
        elements = browser.find_elements(By.CSS_SELECTOR, ".vc_gitem-animated-block")
        for element in elements:
            # Look for img tag within each animated block
            img_tags = element.find_elements(By.TAG_NAME, "img")
            for img in img_tags:
                alt_text = img.get_attribute("alt")
                if alt_text and alt_text.strip():
                    animal_names.append(alt_text.strip())
    return [('Nordisk Dyrepark', name) for name in animal_names]

def get_ree():
    browser.get('https://reepark.dk/dyreneireepark/')
    elements = browser.find_elements(By.CSS_SELECTOR,  ".animal h3")
    time.sleep(random.randint(4,8))
    animal_names = []
    for element in elements:
        name = element.text.title()
        if not name in animal_names:
            animal_names.append(name)
    return [('Ree Park', name) for name in animal_names]

def get_engholm():
    # Jeg er ikke i mål med denne funktion, 
    # har for nu bare tastet ind manuelt.
    browser.get('https://dyrehavenengholm.dk/')
    wait = WebDriverWait(browser, 5)
    # Click main menu
    dyrene_button = browser.find_element(By.LINK_TEXT, "Dyrene")
    dyrene_button.click()

    # Wait a moment for menu to appear
    wait = WebDriverWait(browser, 10)

    # Click subcategory
    landbrugsdyr_button = browser.find_element(By.LINK_TEXT, "Landbrugsdyr")
    landbrugsdyr_button.click()

    # Wait for submenu and get animal names
    # You'll need to inspect the HTML to find the right selector
    animal_elements = browser.find_elements(By.CSS_SELECTOR, "menu-link")

    # Extract text
    animal_names = [element.text for element in animal_elements]
    print(animal_names)

def get_givskud():
    browser.get('https://www.givskudzoo.dk/da/dyrene/laer-dyrene-at-kende/')
    time.sleep(random.randint(8,12))
    # Hent alle dyrenavne
    elements = browser.find_elements(By.CSS_SELECTOR, ".card-title a")

    animal_names = [element.text for element in elements]
    return [ ('Givskud Zoo', name) for name in animal_names ]

def get_terrariet():
    browser.get('https://terrariet.dk/dyr/')
    time.sleep(random.randint(8,12))

    animal_elements = browser.find_elements(By.CSS_SELECTOR, "h2.et_pb_module_header")
    animal_names = [element.text.title() for element in animal_elements]
    return [('Terrariet Vissenbjerg', name) for name in animal_names]


#### MAIN CODE #####

datafile = 'dyrizoo.csv'
column_names = ['Zoo', 'Dyr']

browser = webdriver.Firefox()
# husk at vælge mode='a' eller 'w' alt efter om du starter forfra eller hvad.
with open(datafile, mode='a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    #writer.writerow(column_names)
    #skaerupdata = get_skaerup()
    #writer.writerows(skaerupdata)
    #odensedata = get_odense()
    #writer.writerows(odensedata)
    #randersdata = get_randers()
    #writer.writerows(randersdata)
    #krokodata = getkroko()
    #writer.writerows(krokodata)
    #pangeasjdata = getpangeasjaelland()
    #writer.writerows(pangeasjdata)
    #pangeafdata = getpangeafalster()
    #writer.writerows(pangeafdata)
    #aalborgdata = get_aalborg()
    #writer.writerows(aalborgdata)
    #nordisk_data = get_nordiskdyrepark()
    #writer.writerows(nordisk_data)
    #ree_data = get_ree()
    #writer.writerows(ree_data)
    #givskud_data = get_givskud()
    #writer.writerows(givskud_data)
    terra_data = get_terrariet()
    writer.writerows(terra_data)
    
print('File created')