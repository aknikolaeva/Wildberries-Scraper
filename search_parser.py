import requests
import pandas as pd
import argparse
from retry import retry

class WildberriesParser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "*/*",
        }

    @retry(Exception, tries=3, delay=1)
    def scrap_page(self, page: int, search_query: str, low_price: int, top_price: int, discount: int = None) -> dict:
        """Scrape data from a single page"""
        params = {
            "appType": "1",
            "curr": "rub",
            "dest": "-1255987",
            "page": str(page),
            "query": search_query,
            "resultset": "catalog",
            "sort": "popular",
            "spp": "30",
            "priceU": f"{low_price * 100};{top_price * 100}",
            "discount": str(discount)
        }
        
        response = requests.get(
            "https://search.wb.ru/exactmatch/ru/common/v9/search",
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def parse_products(self, products: list) -> list:
        """Parse product data from JSON response"""
        parsed_data = []
        
        for product in products:
            price_info = product.get('priceU', {})
            sale_price = product.get('salePriceU', price_info)
            
            parsed_data.append({
                'id': product.get('id'),
                'name': product.get('name'),
                'price': int(price_info / 100) if price_info else None,
                'salePriceU': int(sale_price / 100) if sale_price else None,
                'sale': round((1 - (sale_price / price_info)) * 100, 1) if price_info and sale_price else 0,
                'brand': product.get('brand'),
                'rating': product.get('rating'),
                'supplier': product.get('supplier'),
                'supplierRating': product.get('supplierRating'),
                'feedbacks': product.get('feedbacks'),
                'reviewRating': product.get('reviewRating'),
                'promoTextCard': product.get('promoTextCard'),
                'promoTextCat': product.get('promoTextCat'),
                'link': f"https://www.wildberries.ru/catalog/{product.get('id')}/detail.aspx",
            })
        return parsed_data

    def save_excel(self, data: list, filename: str):
        """Save results to Excel file"""
        df = pd.DataFrame(data)
        df.to_excel(f'{filename}.xlsx', index=False, engine='openpyxl')

    def parse_by_query(self, search_query: str, low_price: int = 1, top_price: int = 1000000, discount: int = 0):
        """Parse products by search query"""
        data_list = []
        for page in range(1, 51):
            try:
                data = self.scrap_page(
                    page=page,
                    search_query=search_query,
                    low_price=low_price,
                    top_price=top_price,
                    discount=discount
                )
                products = data.get('data', {}).get('products', [])
                if not products:
                    break
                
                data_list.extend(self.parse_products(products))
            except Exception:
                continue
        
        if data_list:
            # Save to Excel
            output_filename = f'{search_query}_from_{low_price}_to_{top_price}'
            self.save_excel(data_list, output_filename)
            return output_filename
        return None

def main():
    parser = argparse.ArgumentParser(description='Wildberries Parser')
    parser.add_argument('query', type=str, help='Search query')
    parser.add_argument('--min_price', type=int, default=1, help='Minimum price')
    parser.add_argument('--max_price', type=int, default=1000000, help='Maximum price')
    parser.add_argument('--discount', type=int, default=0, help='Minimum discount')

    args = parser.parse_args()

    wb_parser = WildberriesParser()

    result = wb_parser.parse_by_query(
        search_query=args.query,
        low_price=args.min_price,
        top_price=args.max_price,
        discount=args.discount
    )

    if result:
        print(f"Data successfully saved to {result}.xlsx")
    else:
        print("No data found with the specified parameters")

if __name__ == '__main__':
    main()