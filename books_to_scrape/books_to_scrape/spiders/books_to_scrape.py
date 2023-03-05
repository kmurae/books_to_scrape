import scrapy, os, urllib
from books_to_scrape.items import BooksToScrapeItem


class BooksToScrapeSpider(scrapy.Spider):
    name = 'books_to_scrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']
    dest_dir = './out/images' # ダウンロード先ディレクトリ
    base_url = 'https://books.toscrape.com/'

    def parse(self, response):
        for book in response.css('section .row li'):
            item = BooksToScrapeItem()
            link = response.urljoin(book.css('h3 > a::attr(href)').get())
            yield scrapy.Request(link,callback=self.parse_detail, meta={'item':item}
            )

        next_page = response.css('.next a::attr(href)')
        next_page = response.urljoin(next_page.get())
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['title'] = response.css('h1::text').get()
        item['product_description'] = response.css('#product_description + p::text').get()
        item['url'] = response.url

        # 画像ダウンロード
        image_url = response.css('.thumbnail img::attr(src)').get().strip()
        image_full_url = response.urljoin(image_url)
        print('image_full_url', image_full_url)
        file_name = image_url[image_url.rfind('/') + 1:]
        print('file_name', file_name)
        image_path = image_full_url.replace(self.base_url, '')
        print('image_path', image_path)
        dest_dir = self.dest_dir + '/' + image_path
        print('dest_dir', dest_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        urllib.request.urlretrieve(image_full_url, os.path.join(dest_dir, file_name))

        yield item
