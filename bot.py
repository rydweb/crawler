import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from PIL import Image
import os
import xlwt


def Rempalcer(textString):
    cle = ['Comparer', '(voir tous les produits)', '(voir tous les articles)']
    for Q in cle:
        while Q in textString:
            textString = textString.replace(Q, '')
    return textString

productlist = []
def load_product(url,nume):
    valey = []
    page = requests.get(url)
    BS = BeautifulSoup(page.content, 'html.parser')
    getOver = BS.find('section', id='overview').find('table', id='sellers')
    K = getOver.find('tbody').find_all('tr')
    contImage = BS.find('section', class_='section-images').find_all("img")[-1]
    for e in K:
        Val = e.find('td', class_='table-value').text
        valey.append(Rempalcer(Val).strip())
    valey.append(contImage.get("src"))
    download_image(contImage.get("src"),"Aniwa_2021",str(nume+1))
    return valey


links = []
def load_url(link):
    page = requests.get(link)
    BS = BeautifulSoup(page.content, 'html.parser')
    contPage = BS.find('div', class_='products')
    elems = contPage.find_all('a', class_="title")
    keys = "imprimantes-3d"
    for el in elems:
        link = el.get("href")
        if keys in link:
            links.append(link)
    return(links)


def download_image(url, pathname,nume):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    data = "/wp-content/uploads/"
    if data in url:
        response = requests.get(url, stream=True)
        file_size = int(response.headers.get("Content-Length", 0))
        filename = os.path.join(pathname,nume+".jpg")
        progress = response.iter_content(1024)
        with open(filename, "wb") as f:
            for data in progress:
                f.write(data)
                #progress.update(len(data))

lx = load_url("your webside")
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Sheet Name", cell_overwrite_ok=True)
style = xlwt.easyxf('font: bold 1')

sheet.write(0, 0, 'Id', style)
sheet.write(0, 1, 'Modèle', style)
sheet.write(0, 2, 'Marque', style)
sheet.write(0, 3, 'Catégorie', style)
sheet.write(0, 4, 'Thématique', style)
sheet.write(0, 5, 'Technologie', style)
sheet.write(0, 6, 'Matériaux', style)
sheet.write(0, 7, 'Volume d\'impression', style)
sheet.write(0, 8, 'Date de sortie', style)
sheet.write(0, 9, 'Pays', style)
sheet.write(0, 10, 'Image', style)
workbook.save("AnCrawler.xls")

counter = 1
for l in range(len(lx)):
    lien = lx[l]
    charProd = load_product(lx[l],l+1)
    for z in range(len(charProd)):
        charProd[-1]= str(l+1)+".jpg"
        sheet.write(l + 1, 0, l+1)
        #print(z, " : ", charProd[z])
        sheet.write(l+1, z+1, charProd[z])
        workbook.save("Aniwa.xls")
    print("----Data Uploaded....", load_product(lx[l],l)[0])
    print("    [+]Dossier Image : AnCrawler_2021/",l+1,".jpg")
    counter += 1
