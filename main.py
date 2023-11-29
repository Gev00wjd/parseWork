import json

import requests
from bs4 import BeautifulSoup

def parse_product():
    pages = 1
    pages_count = 2
    all_products_data = []
    while pages <= pages_count:
        url = f'https://online.metro-cc.ru/category/avtotovary/avtokosmetika-aksessuary?in_stock=1&page={pages}'
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Section_id': '6315de530707d1df490306ea'
        }

        s = requests.Session()
        r = s.get(url, headers=Headers)

        soup = BeautifulSoup(r.text, 'lxml')

        pagesF = soup.find('nav', class_='subcategory-or-type__pagination').find_all('li')
        if len(pagesF) >= 5:
            previous_page_element = pagesF[-2]
            pages_count = int(previous_page_element.text)
        else:
            print("Недостаточно данных для определения предыдущего номера страницы.")

        All_product = soup.find('div', class_='subcategory-or-type__products').find_all('div',
                                                                                        class_='catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop')
        all_brends = soup.find('div', {'data-filter-group': 'Бренд'}).find_all('div',
                                                                               class_='catalog-checkbox catalog-checkbox-group__item')
        for i in All_product:
            p_id = i['data-sku']
            p_name = i.find('span', class_='product-card-name__text').text
            p_url = 'https://online.metro-cc.ru' + i.find('a', class_='product-card-name').get('href')
            p_price = i.find('span', class_='product-price__sum-rubles').text
            p_brand = ', '.join([j.text.strip() for j in all_brends if j.text.strip().lower() in p_name.lower()])
            product_data = {
                'ID товара': p_id,
                'Наименование': p_name.strip(),
                'URL': p_url,
                'Цена': ''.join(p_price.split()),
                'Brand': p_brand
            }
            # Добавляем словарь в список
            all_products_data.append(product_data)
        pages += 1
    with open('products_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_products_data, json_file, ensure_ascii=False, indent=4)


def main():
    parse_product()


if __name__ == '__main__':
    main()
