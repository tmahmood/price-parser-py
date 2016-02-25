#!/usr/bin/env python
# encoding: utf-8

from lxml import html
import requests
import shutil
import sys

XTITLE = "id('productTitle')"
XPRICE = '//div[@class="bem-product-price__unit--pdp"]'
XRATING = '//div[@class="bem-review-stars__wrapper"]'
XDESC = '//div[@itemprop="description"]'
XFEAT = '//div[@class="bem-content"]/dl[1]/dd'
XIMG = '//a[@class="zoomable-image"]/img'
XIMG2 = '//div[@id="mainImageWrapper"]/img'


def get_dom():
    """
    get dom from html
    """
    if len(sys.argv) < 2:
        print("missing url to parse")
        sys.exit(1)
    url = sys.argv[1]
    resp = requests.get(url)
    return url, html.fromstring(resp.content)


def download_image(url):
    """downloads an image

    :url: @todo
    :returns: @todo
    """
    response = requests.get(url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def get_elm(dom, xpath, index=None):
    """returns element by xpath

    """
    elm = dom.xpath(xpath)
    if index != None:
        return elm[0]
    return elm


def get_text(dom, xpath, index):
    """returns text of element by index

    """
    elm = get_elm(dom, xpath, index)
    return elm.text_content().strip()


def main():
    """
    Main
    """
    rate = 130
    weight_charge = 600
    url, dom = get_dom()
    data = {}
    data['title'] = get_text(dom, XTITLE, 0)
    price = float(get_text(dom, XPRICE, 0)[1:])
    data['price'] = price * rate
    rating = get_elm(dom, XRATING, 0)
    data['rating'] = rating.attrib['title'].strip().replace('Star review', '')
    data['description'] = get_text(dom, XDESC, 0)
    features = dom.xpath(XFEAT)
    txt = []
    for feature in features:
        txt.append(feature.text_content())
    data['features'] = '\n»    '.join(txt).strip()
    data['url'] = url
    data['review_url'] = data['url'] + '#tabCustReviews'
    failed = False
    try:
        data['img'] = get_elm(dom, XIMG, 0).attrib['src']
    except:
        failed = True
    if failed:
        try:
            data['img'] = get_elm(dom, XIMG2, 0).attrib['src']
        except:
            print("Failed to download image")
            data['img'] = ''
    if data['img'].startswith('//'):
        data['img'] = 'http:' + data['img']
    if data['img'] != '':
        download_image(data['img'])
    if len(sys.argv) >= 3:
        weight = int(sys.argv[2])
        data['weight'] = weight
        data['weight_charge'] = (weight / 1000) * weight_charge
        data['total_price'] = data['weight_charge'] + data['price']
    else:
        data['total_price'] = '%s taka BUT NO WEIGHT PROVIDED' % data['price']
    with open('post_content', 'w') as fp:
        template = """%(title)s

--------------------------------------------
Price
%(price)s
--
Est. Weight
%(weight)s g
--
Price inc. weight charge
%(total_price)s
--------------------------------------------
Rating : %(rating)s
--------------------------------------------
Details: %(url)s
Review : %(review_url)s
--------------------------------------------
Description:
%(description)s
--------------------------------------------
Features:
»    %(features)s
        """
        txt = template % data
        fp.write(txt)
        print(txt)


if __name__ == '__main__':
    main()
