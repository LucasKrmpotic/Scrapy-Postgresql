#!/bin/bash

cd ..
source scrapyenv/bin/activate
cd codeworkers
scrapy crawl computrabajo -s CLOSESPIDER_ITEMCOUNT=50
scrapy crawl bumeran -s CLOSESPIDER_ITEMCOUNT=50
scrapy crawl zonajobs -s CLOSESPIDER_ITEMCOUNT=50
scrapy crawl lawebdelprogramador -s CLOSESPIDER_ITEMCOUNT=50
scrapy crawl stackoverflow -s CLOSESPIDER_ITEMCOUNT=50

