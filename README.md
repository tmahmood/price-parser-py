# price-parser-py

A small script that downloads a product page and parse details of the product. Uses `LXML` to parse websites

Two parsers are already included in `inc` folder for chainreaction and wiggle. New parsers can be added by extending `Parser` class  and defining selectors.

The script also takes the product image and imposes price on that image, using imagemagick.
