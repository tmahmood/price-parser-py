#!/usr/bin/env python
# encoding: utf-8

import inc.parser as parser
import inc.util as util


class Wiggle(parser.Parser):
    """Parses wiggle"""

    def __init__(self, url):
        super(Wiggle, self).__init__(url)
        self.XTITLE = "id('productTitle')"
        self.XPRICE = '//div[@class="bem-product-price__unit--pdp"]'
        self.XRATING = '//div[@class="bem-review-stars__wrapper"]'
        self.XDESC = '//div[@itemprop="description"]'
        self.XFEAT = '//div[@class="bem-content"]/dl[1]/dd'
        self.XIMG = '//a[@class="zoomable-image"]/img'
        self.XIMG2 = '//div[@id="mainImageWrapper"]/img'
        self.REVIEW_PREFIX = '#tabCustReviews'

    def get_original_price(self):
        """get original price
        :returns: @todo

        """
        return float(util.get_text(self.dom, self.XPRICE, 0)[1:])

    def get_rating(self):
        """get product rating

        :returns: @todo
        """
        rating = util.get_elm(self.dom, self.XRATING, 0)
        return rating.attrib['title'].strip().replace('Star review', '')

    def get_description(self):
        """get product description

        :returns: @todo
        """
        return util.get_text(self.dom, self.XDESC, 0)

    def get_features(self):
        """get product features


        """
        features = self.dom.xpath(self.XFEAT)
        txt = []
        for feature in features:
            txt.append(feature.text_content())
        s = "\n»    "
        return s.join(txt).strip()

    def get_image(self):
        """get image url and download

        :returns: @todo
        """
        failed = False
        try:
            img = util.get_elm(self.dom, self.XIMG, 0).attrib['src']
        except Exception:
            failed = True
        if failed:
            try:
                img = util.get_elm(self.dom, self.XIMG2, 0).attrib['src']
            except Exception:
                print("Failed to download image")
                img = ''
        if img.startswith('//'):
            img = 'http:' + img
        if img != '':
            util.download_image(img)
        return img
