import scrapy


class ReviewSpider(scrapy.Spider):
    name = "review"
    # allowed_domains = ['amazon.com']

    flag = 1

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
    }

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }

    def start_requests(self):

        for url in self.urls:

            url = url.replace('dp', 'product-reviews')

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers
            )

    def parse(self, response):

        complete_list = response.xpath('//*[@id="cm_cr-review_list"]/div')

        reviews = complete_list[:-1]

        if reviews:
            for review in reviews:

                reviewTitle = review.xpath(
                    './/div[@class="a-row"]/a[@data-hook="review-title"]/span/text()').extract()
                star = review.xpath(
                    './/i[@data-hook="review-star-rating"]/span/text()').extract_first()
                date = review.xpath(
                    './/span[@data-hook="review-date"]/text()').extract_first()
                body = review.xpath(
                    './/span[@data-hook="review-body"]/span/text()').extract()

                print(f"Extracted : {self.flag}", end="\r")
                self.flag += 1

                yield {
                    'review': reviewTitle,
                    'stars': star,
                    'date': date,
                    'body': body
                }

            newurl = complete_list[-1].xpath(
                './/ul/li[2]/a/@href').extract_first()

            # print(f'new url : {response.urljoin(newurl)}')

            yield scrapy.Request(
                url=response.urljoin(newurl),
                callback=self.parse,
                headers=self.headers
            )
