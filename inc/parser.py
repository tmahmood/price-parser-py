import inc.util as util


class Parser(object):

    """parse wiggle website"""
    def __init__(self, url):
        super(Parser, self).__init__()
        self.url = url
        self.dom = util.get_dom(self.url)
        self.XTITLE = None
        self.XPRICE = None
        self.XRATING = None
        self.XDESC = None
        self.XFEAT = None
        self.XIMG = None
        self.REVIEW_PREFIX = None

    def get_title(self):
        """get product title

        :returns: @todo
        """
        return util.get_text(self.dom, self.XTITLE, 0).replace('\n', ' ')

    def get_price(self, rate):
        """parse price and calculate with the rate

        :rate: @todo
        :returns: @todo

        """
        return self.get_original_price() * rate

    def get_original_price(self):
        """get original price
        :returns: @todo

        """
        return float(util.get_text(self.dom, self.XPRICE, 0)[1:])

    def get_review_url(self):
        """get review url

        :returns: @todo

        """
        return self.url + self.REVIEW_PREFIX

    def get_rating(self):
        """return rating"""
        raise NotImplementedError()

    def get_description(self):
        """return description"""
        raise NotImplementedError()

    def get_features(self):
        """get features"""
        raise NotImplementedError()

    def get_image(self):
        """get_image"""
        raise NotImplementedError()

    def parse_page(self, rate, weight_charge):
        """parsed the page for product data

        :returns: @todo
        """
        data = {}
        data['title'] = self.get_title()
        data['original_price'] = self.get_original_price()
        data['price'] = self.get_price(rate)
        data['rating'] = self.get_rating()
        data['description'] = self.get_description()
        data['features'] = self.get_features()
        data['url'] = self.url
        data['review_url'] = self.get_review_url()
        data['img'] = self.get_image()
        return data
