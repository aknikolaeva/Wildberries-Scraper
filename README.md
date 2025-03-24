
# Wildberries Parser

A Python script for scraping product data from Wildberries.ru e-commerce platform.

## Features

- Scrapes product information by search query
- Filters products by price range
- Optionally filters by discount percentage
- Saves results to Excel file
- Handles pagination (up to 50 pages)
- Includes retry mechanism for failed requests

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - pandas
  - openpyxl
  - retry

## Installation

1. Clone the repository or download the script
2. Install required packages:
   ```bash
   pip install requests pandas openpyxl retry
   ```

## Usage

### Command Line

```bash
python search_parser.py "search query" [--min_price MIN] [--max_price MAX] [--discount DISCOUNT]
```

#### Parameters:

- `search query` (required): The product search term
- `--min_price` (optional): Minimum price filter (default: 1)
- `--max_price` (optional): Maximum price filter (default: 1000000)
- `--discount` (optional): Minimum discount percentage (default: 0)

#### Examples:

1. Basic search:

   ```bash
   python wildberries_parser.py "Телефон Samsung"
   ```
2. Search with price range:

   ```bash
   python wildberries_parser.py "Телефон Samsung" --min_price 1000 --max_price 5000
   ```
3. Search with discount filter:

   ```bash
   python wildberries_parser.py "Телефон Samsung" --discount 10
   ```

### Output

The script generates an Excel file with the following naming convention:
`{search_query}_from_{min_price}_to_{max_price}.xlsx`

The Excel file contains the following product information:

- Product ID
- Name
- Price
- Sale price
- Discount percentage
- Brand
- Rating
- Supplier information
- Feedback count
- Review rating
- Promo texts
- Product link

## Notes

- The script includes a retry mechanism that will attempt failed requests up to 3 times
- Wildberries may block requests if too many are made in a short period
- Results are limited to 50 pages (approximately 2500 products)

## License

This project is open-source and available for use under the MIT License.
