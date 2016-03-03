import inc.parser as parser
import inc.util as util


class ChainReaction(parser.Parser):

    XTITLE = '//li[@class="crcPDPTitle"]'
    XPRICE = '//span[@class="crcPDPPriceHidden"]'
    XRATING = '//li[@class="crcPDPRatingsReviewsStarsInfo"]'
    XDESC = 'id("crcPDPComponentDescription")'
    XFEAT = ''
    XIMG = '//li[@class="crcPDPImage"]//img'

    def get_title(self):
        """get product title

        :returns: @todo
        """
        return util.get_text(self.dom, ChainReaction.XTITLE, 0)

    def get_price(self, rate):
        """parse price and calculate with the rate

        :rate: @todo
        :returns: @todo

        """
        price = float(util.get_text(self.dom, ChainReaction.XPRICE, 0))
        return price * rate

    def get_rating(self):
        """get product rating

        :returns: @todo
        """
        rating = util.get_elm(self.dom, ChainReaction.XRATING, 0)
        return rating.text_content().strip()

    def get_description(self):
        """get product description

        :returns: @todo
        """
        return util.get_text(self.dom, ChainReaction.XDESC, 0)

    def get_features(self):
        """@todo: Docstring for function.

        :arg1: @todo
        :returns: @todo

        """
        return ''

    def get_image(self):
        """get image url and download

        :returns: @todo
        """
        try:
            img = util.get_elm(self.dom, ChainReaction.XIMG, 0).attrib['src']
        except Exception:
            print("Failed to download image")
            img = ''
        if img.startswith('//'):
            img = 'http:' + img
        if img != '':
            util.download_image(img)
        return img


