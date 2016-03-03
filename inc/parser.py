import inc.util as util


class Parser(object):

    """parse wiggle website"""
    def __init__(self, url):
        super(Parser, self).__init__()
        self.url = url
        self.dom = util.get_dom(self.url)

    def parse_page(self, rate, weight_charge):
        """parsed the page for product data

        :returns: @todo
        """
        data = {}
        data['title'] = self.get_title()
        data['price'] = self.get_price(rate)
        print(data)
        data['rating'] = self.get_rating()
        data['description'] = self.get_description()
        data['features'] = self.get_features()
        data['url'] = self.url
        data['review_url'] = self.get_review_url()
        data['img'] = self.get_image()
        return data
