import time
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from time import sleep
import random
import os
from get_proxy import check_ip

file_name = "minimaks_pars.xml"
url = 'https://www.minimaks.ru/catalog/'
cookies = {
    'BITRIX_SM_GUEST_ID': '46920283',
    'BITRIX_SM_USER_TYPE': '2',
    'BITRIX_SM_VIEW_BASKET': 'TABLE',
    'BITRIX_SM_SORT_CATALOG': 'CHASTOTA_PRODAZH',
    'BITRIX_SM_VIEW_FAVORITE': 'LIST',
    'BITRIX_SM_SECTIONS_FAVORITE': 'SHOW_SECTIONS',
    'BITRIX_SM_CATALOG_SETTING_MAIN_CITY': '606729',
    'rrpvid': '907119976026863',
    'rcuid': '653655de7d1ee741f0ef2dd6',
    '_userGUID': '0:lo2sxeqh:RPAUp~cF5_b8RBYLgkAKAKhqf1slEXUI',
    'digi_uc': 'W10=',
    'rraem': '',
    '_ym_uid': '169805974319312276',
    'tmr_lvid': '14a7da0ef9f6cd8982da9c6677b88c94',
    'tmr_lvidTS': '1698059743671',
    'BX_USER_ID': 'e43dbf14bd7886d7ac33f4a8b6f0c94f',
    'BITRIX_SM_MAIN_CITY5': '606729',
    'BITRIX_SM_COOKIE_AGREEMENT': '1',
    'BITRIX_SM_VIEW_CATALOG': 'TILE',
    'BITRIX_SM_CNT_CATALOG': '96',
    'PHPSESSID': '6cLAr6QW6nu7tULGk8xAWQJXYq1pwXHd',
    'dSesn': 'be5290de-7f55-7dd4-f0f3-3b3cae6b57eb',
    '_dvs': '0:lo4f7ycw:H9TAMoIo1qkra~wBwQn5~eygJBJTDZU8',
    'rrwpswu': 'true',
    '_gid': 'GA1.2.1390581771.1698157653',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A11%2C%22EXPIRE%22%3A1698181140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    '_ym_isad': '1',
    'BITRIX_SM_STORES_CATALOG': '[%22183%22%2C%22192%22%2C%22194%22%2C%22198%22%2C%22202%22%2C%22209%22%2C%22210%22%2C%22211%22%2C%22212%22%2C%22213%22%2C%22214%22%2C%22215%22%2C%22216%22%2C%22217%22%2C%22218%22%2C%22219%22%2C%22220%22%2C%22221%22%2C%22222%22%2C%22223%22%2C%22224%22%2C%22225%22%2C%22226%22%2C%22227%22%2C%22228%22%2C%22229%22%2C%22239%22%2C%22252%22%2C%22255%22%2C%22257%22%2C%22266%22%2C%22269%22%2C%22270%22%2C%22280%22%2C%22281%22%2C%22283%22%2C%22287%22%2C%22288%22%2C%22292%22%2C%22293%22%2C%22295%22%2C%22296%22%2C%22297%22%2C%22299%22%2C%22337%22%2C%22340%22%2C%22350%22]',
    'BITRIX_SM_FILTER_CATALOG': 'FILTER_CATALOG_TRUE',
    '_ga': 'GA1.2.653616618.1698059744',
    'tmr_detect': '1%7C1698157683513',
    '_ga_3YQ9CTX8JM': 'GS1.1.1698157652.2.1.1698157700.12.0.0',
    '_ym_d': '1698157724',
    'BITRIX_SM_LAST_VISIT': '24.10.2023%2017%3A28%3A44',
}
headers = {
    'authority': 'www.minimaks.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.minimaks.ru/catalog/strukturirovannye-kabelnye-sistemy-sks/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
proxy = check_ip()


# Получаем html файл
def get_html(url):
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies, proxies=proxy)
    except Exception as e:
        proxies = check_ip()
        response = requests.get(url=url, headers=headers, cookies=cookies, proxies=proxies)
        print("Нет доступа к странице", e)

    soup = BeautifulSoup(response.text, "lxml")
    return soup


# Создание нового xml файла
def new_file_xml(file_name):
    root = ET.Element('products')
    tree = ET.ElementTree(root)
    with open(file_name, 'wb') as file:
        tree.write(file)


# Получаем последний id
def current_id(file_name):
    existing_tree = ET.parse(file_name, parser=ET.XMLParser(encoding="utf-8"))
    root = existing_tree.getroot()

    id_elements = root.findall(".//id")

    last_id_element = id_elements[-1]
    last_id = int(last_id_element.text)

    print('=========')
    print('=========')
    print('=========')
    print("Последний элемент id:", last_id)
    print('=========')

    return last_id


# Получаем текущий раздел
def current_chapter(file_name):
    existing_tree = ET.parse(file_name, parser=ET.XMLParser(encoding="utf-8"))
    root = existing_tree.getroot()

    chapter_elements = root.findall(".//count_chapter")

    last_chapter_element = chapter_elements[-1]
    last_chapter = int(last_chapter_element.text)

    print('=========')
    print('=========')
    print('=========')
    print("Текущий раздел:", last_chapter)
    print('=========')

    return last_chapter


# Получаем ссылки на подпункты каталога
def get_chapter(url):
    soup = get_html(url)
    chapter_blocks = soup.find_all("div", class_="col-xs-12 col-sm-6 col-md-6 col-lg-6 catalog-block-item")

    # Два блока
    for chapter in chapter_blocks:
        chapter_elements = chapter.find_all("div", class_="catalog-item")

        # Девять элементов списка
        for el in chapter_elements:
            el_links = el.find_all("a")[1:]

            # Ссылки
            for link in el_links:
                link = "https://www.minimaks.ru/" + link.get("href")
                yield link


# Получаем последнюю страницу
def get_pagination(link):
    soup = get_html(link)
    if len(soup.find_all(class_="nothing-find")) > 0:
        return 0
    elif len(soup.find_all(class_="mobile-pagination")) > 0:
        get_max_page = soup.find(class_="mobile-pagination hidden-sm hidden-md hidden-lg").find_all(class_="mobile-pagination__contains")[1].find_all("a")[1].get("href")
        max_page = int(get_max_page.split("?PAGEN_1=")[-1].strip())
        return max_page
    else:
        return 1


# Парсим карточку товара
def get_product(full_card_link, id, count_chapter):
    soup_product = get_html(full_card_link)

    id = str(id)
    count_chapter = str(count_chapter)

    # Ищем заголовок
    try:
        title = soup_product.find("h1", id="page-header").text.strip()

    except Exception as e:
        print("Заголовок не найден:")
        title = ""

    # Ищем изображения
    try:
        gallery = []
        gallery_link = soup_product.find("div", class_="js-photo-slider").find_all("img")
        for photo_link in gallery_link:
            image = f"https://www.minimaks.ru{photo_link.get("src")}"
            gallery.append(image)

        if gallery[0] == "https://www.minimaks.ru/local/templates/main/images/no_photo.png" or len(gallery) <= 0:
            gallery = []
            img = ""
        else:
            img = gallery[0]

            if len(gallery) == 1:
                gallery = []
            else:
                gallery = gallery[1:]

    except Exception as e:
        print("Изображения не найдены:")
        gallery = []
        img = ""

    # Ищем описание
    try:
        description = soup_product.find("div", class_="js-description-text-small").get_text("<br>", strip=True).strip()

    except Exception as e:
        description = ""

    # Ищем цену
    try:
        price = soup_product.find(class_="price-block__pricePerCard").find(class_="price-style").get_text()
        price = price.replace("₽", "").strip()
    except Exception as e:
        print("Цена не найдена")
        price = ""

    # Ищем страну производитель
    try:
        country = soup_product.find(class_="madeIn__text").get_text().strip()

    except Exception as e:
        print("Страна производитель не найдена:")
        country = ""

    # Ищем характеристики
    try:
        characteristics = dict()
        characteristics_list = soup_product.find(class_="col-xs-12 all-specifications scroll").find_all("tr")

        for char in characteristics_list:
            key = char.find(class_="heading-text").text.strip()
            value = char.find(class_="specification-text").text.strip()
            characteristics[key] = value

    except Exception as e:
        print("Характеристики не найдены:")
        characteristics = dict()

    params = {
        "id": id,
        "count_chapter": count_chapter,
        "title": title,
        "gallery": gallery,
        "img": img,
        "description": description,
        "price": price,
        "country": country,
        "characteristics": characteristics
    }

    return params


# Запись в xml файл
def load_in_xml(params, file_name):
    existing_tree = ET.parse(file_name, parser=ET.XMLParser(encoding="utf-8"))
    root = existing_tree.getroot()

    product = ET.SubElement(root, 'product')

    id = ET.SubElement(product, 'id')
    id.text = params['id']

    count_chapter = ET.SubElement(product, 'count_chapter')
    count_chapter.text = params['count_chapter']

    title = ET.SubElement(product, 'title')
    title.text = params['title']

    gallery = ET.SubElement(product, "gallery")
    for picture in params['gallery']:
        gallery_element = ET.SubElement(gallery, "gallery_element")
        gallery_element.text = picture

    img = ET.SubElement(product, 'img')
    img.text = params['img']

    description = ET.SubElement(product, 'description')
    description.text = params['description']

    country = ET.SubElement(product, 'country')
    country.text = params['country']

    characteristics = ET.SubElement(product, "characteristics")
    for key, value in params['characteristics'].items():
        char_element = ET.SubElement(characteristics, "char")
        char_element.set('name', key)
        char_element.text = value

    existing_tree.write(file_name, encoding="utf-8", xml_declaration=True)


def main(url, file_name):
    count_product = 1
    count_chapter = 1

    if not os.path.isfile(file_name):
        new_file_xml(file_name)
        last_id = 0
        last_chapter = 0
    else:
        last_id = current_id(file_name)
        last_chapter = current_chapter(file_name)

    for link in get_chapter(url):
        if count_chapter < last_chapter:
            print(f"WARNING || Skip chapter {count_chapter}")
            count_chapter += 1
            continue

        max_page = get_pagination(link)

        if max_page == 0:
            continue

        print("===========")
        print(f"In chapter {max_page} pages...")
        print("===========")

        for page_number in range(1, max_page + 1):
            page_link = f"{link}?PAGEN_1={page_number}"

            print("-------")
            print(page_link)
            print("-------")

            soup_page = get_html(page_link)
            cards_links = soup_page.find_all("a", class_="title-list-item js-ga-detail-item-link")
            for card_link in cards_links:
                if count_product <= last_id:
                    print(f"Skip product number {count_product}")
                    count_product += 1
                    continue

                full_card_link = f"https://www.minimaks.ru{card_link.get('href')}"
                params = get_product(full_card_link, count_product, count_chapter)
                load_in_xml(params, file_name)

                print(f"Product number {count_product} save successful")
                count_product += 1

        count_chapter += 1


main(url, file_name)
