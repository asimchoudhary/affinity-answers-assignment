import requests
import pandas as pd
from tabulate import tabulate
import time

def fetch_all_olx_results(search_query):
    """
    Fetch all search results from OLX API
    """
    base_url = "https://www.olx.in/api/relevance/v4/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-IN,en;q=0.9',
        'Referer': f'https://www.olx.in/items/q-{search_query.replace(" ", "-")}',
        'Origin': 'https://www.olx.in',
        'Connection': 'keep-alive',
    }
    
    all_items = []
    page = 1
    
    print(f"Fetching results for '{search_query}'...\n")
    
    while True:
        params = {
            'facet_limit': 1000,
            'lang': 'en-IN',
            'location': 1000001,
            'location_facet_limit': 40,
            'page': page,
            'platform': 'web-desktop',
            'pttEnabled': 'true',
            'query': search_query,
            'relaxedFilters': 'true',
            'size': 40,
            'spellcheck': 'true',
        }
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data:
                    items = data['data']
                    
                    # If no items, we've reached the end
                    if not items or len(items) == 0:
                        print(f"✓ Reached end of results at page {page}")
                        break
                    
                    all_items.extend(items)
                    print(f"Page {page}: Fetched {len(items)} items (Total: {len(all_items)})")
                    
                    page += 1
                    
                    # Added Delay to avoid rate limiting
                    time.sleep(1.5)
                else:
                    print("No 'data' field in response")
                    break
                    
            elif response.status_code == 403:
                print("Access forbidden - might be blocked by anti-bot")
                break
            else:
                print(f"Error: Status code {response.status_code}")
                break
                
        except Exception as e:
            print(f"Error on page {page}: {str(e)}")
            break
    
    return all_items

def extract_item_data(items):
    """
    Extract title, description, and price from items
    """
    extracted_data = []
    
    for item in items:
        title = item.get('title', 'N/A')
        

        description = item.get('description', item.get('shortDescription', 'N/A'))
        

        price_data = item.get('price', {})
        if isinstance(price_data, dict):
            price = price_data.get('value', {}).get('display', 'N/A')
        else:
            price = price_data if price_data else 'N/A'
        
 
        location = 'N/A'
        if 'locations_resolved' in item and item['locations_resolved']:
            location_data = item['locations_resolved']
            if isinstance(location_data, dict):
                location = location_data.get('ADMIN_LEVEL_3_name', 
                           location_data.get('ADMIN_LEVEL_1_name', 'N/A'))
        
 
        ad_id = item.get('id', '')
        ad_url = f"https://www.olx.in/item/{ad_id}" if ad_id else 'N/A'
        
        extracted_data.append({
            'Title': title,
            'Description': description[:100] + '...' if len(str(description)) > 100 else description,
            'Price': price,
            'Location': location,
            'URL': ad_url
        })
    
    return extracted_data


if __name__ == "__main__":
    search_query = "car cover"
    

    all_items = fetch_all_olx_results(search_query)
    
    print(f"\n{'='*60}")
    print(f"Total items fetched: {len(all_items)}")
    print(f"{'='*60}\n")
    
    if all_items:

        extracted_data = extract_item_data(all_items)
        
        # Create DataFrame
        df = pd.DataFrame(extracted_data)
        
        # Display in table format using tabulate
        print(tabulate(df.values.tolist(), headers=df.columns.tolist(), tablefmt='grid', showindex=False))
        
        # Save to CSV
        df.to_csv(f'olx_{search_query}_results.csv', index=False, encoding='utf-8')
        print(f"Results saved to 'olx_{search_query}_results.csv'")
    else:
        print("No items found!")
