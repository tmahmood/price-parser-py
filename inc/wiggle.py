import inc.parser as parser
import inc.util as util


class Wiggle(parser.Parser):

    XTITLE = "id('productTitle')"
    XPRICE = '//div[@class="bem-product-price__unit--pdp"]'
    XRATING = '//div[@class="bem-review-stars__wrapper"]'
    XDESC = '//div[@itemprop="description"]'
    XFEAT = '//div[@class="bem-content"]/dl[1]/dd'
    XIMG = '//a[@class="zoomable-image"]/img'
    XIMG2 = '//div[@id="mainImageWrapper"]/img'

    def get_review_url(self):
        """get review url

        :returns: @todo

        """
        return self.url + '#tabCustReviews'

    def get_title(self):
        """get product title

        :returns: @todo
        """
        return util.get_text(self.dom, Wiggle.XTITLE, 0)

    def get_price(self, rate):
        """parse price and calculate with the rate

        :rate: @todo
        :returns: @todo

        """
        price = float(util.get_text(self.dom, Wiggle.XPRICE, 0)[1:])
        return price * rate

    def get_rating(self):
        """get product rating

        :returns: @todo
        """
        rating = util.get_elm(self.dom, Wiggle.XRATING, 0)
        return rating.attrib['title'].strip().replace('Star review', '')

    def get_description(self):
        """get product description

        :returns: @todo
        """
        return util.get_text(self.dom, Wiggle.XDESC, 0)

    def get_features(self):
        """get product features


        """
        features = self.dom.xpath(Wiggle.XFEAT)
        txt = []
        for feature in features:
            txt.append(feature.text_content())
        return '\n»    '.join(txt).strip()

    def get_image(self):
        """get image url and download

        :returns: @todo
        """
        failed = False
        try:
            img = util.get_elm(self.dom, Wiggle.XIMG, 0).attrib['src']
        except Exception:
            failed = True
        if failed:
            try:
                img = util.get_elm(self.dom, Wiggle.XIMG2, 0).attrib['src']
            except Exception:
                print("Failed to download image")
                img = ''
        if img.startswith('//'):
            img = 'http:' + img
        if img != '':
            util.download_image(img)
        return img
