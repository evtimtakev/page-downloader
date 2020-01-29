import requests
from bs4 import BeautifulSoup

FILE_NAME = 'INDEX'


def create_file(content, ext, name):
    name = '{0}.{1}'.format(name, ext)
    with open(name, "w", encoding='utf-8') as file:
        file.write(content)


def download_resources(soup, source):
    for link in soup.find_all('link', href=True):
        if 'css' in link['href']:
            css = requests.get(source + link['href'])
            css_str = css.text
            name_to = 'url({0}/img/'.format(source)
            name_to_b = "url('{0}/img/".format(source)
            css_replaced = css_str.replace('url(img/', name_to)
            css_replaced_dash = css_replaced.replace("url('img/", name_to_b)
            create_file(css_replaced_dash, '', link['href'])


def download_html(url, source):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    for link in soup.find_all('link', href=True):
        if 'css' in link['href']:
            link['href'] = './' + link['href']

    for link in soup.find_all('img', src=True):
        link['src'] = source + link['src']

    for link in soup.find_all('script', src=True):
        if 'js' in link['src']:
            link['src'] = source + link['src']

    for td in soup.find_all('td', background=True):
        td['background'] = source + td['background']

    create_file(str(soup), 'html', FILE_NAME)
    download_resources(soup, source)


if __name__ == '__main__':
    url = input("Enter url to scrap : ")
    source = input("enter source url : ")
    download_html(url, source)
