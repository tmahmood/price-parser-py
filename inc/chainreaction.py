#!/usr/bin/env python
# encoding: utf-8

import inc.parser as parser
import inc.util as util


class ChainReaction(parser.Parser):

    """parse ChainReaction website"""
    def __init__(self, url):
        super(ChainReaction, self).__init__(url)
        self.XTITLE = '//li[@class="crcPDPTitle"]'
        self.XPRICE = '//span[@class="crcPDPPriceHidden"]'
        self.XRATING = '//li[@class="crcPDPRatingsReviewsStarsInfo"]'
        self.XDESC = 'id("crcPDPComponentDescription")'
        self.XFEAT = 'id("crcPDPComponentDescription")/ul/li'
        self.XIMG = '//li[@class="crcPDPImage"]//img'
        self.REVIEW_PREFIX = '#bazaarvoice_reviews_tab'

    def get_original_price(self):
        """parse for original price
        :returns: @todo

        """
        return float(util.get_text(self.dom, self.XPRICE, 0))

    def get_rating(self):
        """get product rating

        :returns: @todo
        """
        try:
            rating = util.get_elm(self.dom, self.XRATING, 0)
        except Exception:
            return 'N/A'
        return rating.text_content().strip()

    def get_description(self):
        """get product description

        :returns: @todo
        """
        desc = util.get_text(self.dom, self.XDESC, 0)
        return desc.split('Features:')[0]

    def get_features(self):
        """@todo: Docstring for function.

        :arg1: @todo
        :returns: @todo

        """
        feat = util.get_elm(self.dom, self.XFEAT)
        line = []
        if feat != None:
            for li in feat:
                line.append('» ' + li.text_content())
            return '\n'.join(line).strip('» ')
        desc = util.get_text(self.dom, self.XDESC, 0)
        try:
            lines = desc.split('Features:')[1].strip().split('\n')
        except Exception:
            return ''
        newline = []
        for l in lines:
            line = l.strip()
            if line != '':
                newline.append('» ' + line)
            else:
                newline.append('\n')
        return '\n'.join(newline).strip('»  ')

    def get_image(self):
        """get image url and download

        :returns: @todo
        """
        try:
            img = util.get_elm(self.dom, self.XIMG, 0).attrib['src']
        except Exception:
            print("Failed to download image")
            img = ''
        if img.startswith('//'):
            img = 'http:' + img
        if img != '':
            util.download_image(img)
        return img


