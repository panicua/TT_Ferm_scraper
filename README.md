# TT_Ferm_scraper
Test task solution for **FERM**.
Data scraper.

## Main Technologies:
- Python
- Pandas
- BeautifulSoup
- aiohttp
- asyncio
- requests

## Prerequisites:
- Python 3.11+

## Local Installation and Usage:
1. **Clone the repository:**

   ```sh
   git clone https://github.com/panicua/TT_Ferm_scraper.git
   cd TT_Ferm_scraper
   ```
   
2. Create and activate **venv**:

   (bash)
   ```sh
   python -m venv venv
   source venv/Scripts/activate
   ```
   
   Windows (Command Prompt)
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
   
   Mac / Linux (Unix like systems)
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   
   ```sh
   pip install -r requirements.txt
   ```

4. Run the script:
   ```sh
   python -m agroplant.main
   ```
   
## DEMO:
You can see detailed info in `results` folder.
![scrape_data_result.png](demo_images%2Fscrape_data_result.png)

## Notes:
- Feel free to change files/settings in the `agroplant/fungicide_scrapers/settings.py` module.
- On my pc script takes about 1 minute to scrape 600+ urls.
