#!/usr/bin/env python
# encoding: utf-8

import sys
import inc.wiggle as wiggle
import inc.chainreaction as chainreaction

TEMPLATE = """%(title)s
============================================
Price inc. weight charge
%(total_price)s
==
Est. Weight
%(weight)s g
============================================
Rating : %(rating)s
============================================
Details: %(url)s
Review : %(review_url)s
============================================
Description:
%(description)s
============================================
Features:
» %(features)s
        """


def main():
    """Main

    """
    rate = 130
    weight_charge = 600

    if len(sys.argv) < 2:
        print("missing url to parse")
        sys.exit(1)
    url = sys.argv[1]
    parser = None
    if url.find('wiggle.co.uk') >= 0:
        parser = wiggle.Wiggle(url)
    elif url.find('chainreaction') >= 0:
        parser = chainreaction.ChainReaction(url)
    else:
        print("unknown website\n")
        return

    data = parser.parse_page(rate, weight_charge)

    if len(sys.argv) >= 3:
        weight = int(sys.argv[2])
        data['weight'] = weight
        data['weight_charge'] = (weight / 1000) * weight_charge
        data['total_price'] = data['weight_charge'] + data['price']
    else:
        data['total_price'] = '%s taka BUT NO WEIGHT PROVIDED' % data['price']
    with open('post_content', 'w') as fp:
        txt = TEMPLATE % data
        fp.write(txt)
        print(txt)


if __name__ == '__main__':
    main()
