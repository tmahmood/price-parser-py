#!/usr/bin/env python
# encoding: utf-8

import sys
import inc.wiggle as wiggle
import inc.chainreaction as chainreaction
import subprocess

TEMPLATE = """%(title)s
========================
Our Price: BDT %(total_price)s
Original Price: £%(original_price)s
==
Est. Weight
%(weight)s g
========================
Rating : %(rating)s
========================
Details: %(url)s
Review : %(review_url)s
========================
Description:
%(description)s
========================
Features:
» %(features)s
"""


def main():
    """Main"""
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
        print("unknown website")
        return
    data = parser.parse_page(rate, weight_charge)
    if len(sys.argv) >= 3:
        weight = int(sys.argv[2])
        data['weight'] = weight
        data['weight_charge'] = round((weight / 1000) * weight_charge, 2)
        data['total_price'] = round(data['weight_charge'] + data['price'])
    else:
        data['total_price'] = '%s taka BUT NO WEIGHT PROVIDED' % data['price']
    with open('post_content', 'w') as fp:
        txt = TEMPLATE % data
        fp.write(txt)
    cmd = "convert_img.jpg_-font_Ubuntu_-pointsize_24_-background_Orange_" +\
          "label:| Price: %s taka |_-gravity_Center_-append_imgtxt.jpg" % data['total_price']
    subprocess.check_output(cmd.split('_'))


if __name__ == '__main__':
    main()
