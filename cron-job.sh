#!/bin/bash

cd ..
source scrapyenv/bin/activate
cd codeworkers
scrapy crawl computrabajo
scrapy crawl bumeran
scrapy crawl zonajobs 
scrapy crawl lawebdelprogramador
scrapy crawl stackoverflow

