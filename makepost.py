from lxml import html
import requests
import shutil
import sys


def download_image(url):
    """downloads an image

    :url: @todo
    :returns: @todo
    """
    response = requests.get(url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def get_elm(xpath, index=None):
    """returns element by xpath

    """
    elm = dom.xpath(xpath)
    if index != None:
        return elm[0]
    return elm


def get_text(xpath, index):
    """returns text of element by index

    """
    elm = get_elm(xpath, index)
    return elm.text_content().strip()

rate = 130

if len(sys.argv) < 2:
    sys.exit(1)
print(sys.argv)
url = sys.argv[1]
resp = requests.get(url)
dom = html.fromstring(resp.content)
data = {}

data['title'] = get_text("id('productTitle')", 0)
price = float(get_text('//div[@class="bem-product-price__unit--pdp"]', 0)[1:])
data['price'] = price * rate
rating = get_elm('//div[@class="bem-review-stars__wrapper"]', 0)
data['rating'] = rating.attrib['title'].strip()
data['description'] = get_text('//div[@itemprop="description"]', 0)
features = dom.xpath('//div[@class="bem-content"]/dl[1]/dd')
txt = []
for feature in features:
    txt.append(feature.text_content())
data['features'] = '\n»    '.join(txt).strip()
data['img'] = get_elm('//a[@class="zoomable-image"]/img', 0).attrib['src']
data['url'] = url
data['review_url'] = data['url'] + '/#tabCustReviews'

if data['img'].startswith('//'):
    data['img'] = 'http:' + data['img']

download_image(data['img'])

with open('post_content', 'w') as fp:
    tpl = """
%(title)s

Description:
%(description)s

Review:
%(rating)s

Features:
»    %(features)s

Price: %(price)d taka + [ ADD WEIGHT IN GRAM ] * 600

Details: %(url)s
Review: %(review_url)s

        """
    txt = tpl % data
    fp.write(txt)
    print (txt)
