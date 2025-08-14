import requests
import time
import json
from typing import Dict, List, Optional

class WikipediaAnimalScraper:
    def __init__(self, language='en'):
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/api/rest_v1"
        self.search_url = f"https://{language}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        # Vær høflig - identifikér dit projekt
        self.session.headers.update({
            'User-Agent': 'Zoo Animal Information Scraper - Educational Project'
        })
    
    def search_animal(self, animal_name: str, limit: int = 5) -> List[Dict]:
        """
        Søg efter artikler om et bestemt dyr
        """
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': animal_name,
            'srlimit': limit,
            'srnamespace': 0  # Kun hovednavnerum
        }
        
        try:
            response = self.session.get(self.search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'query' in data and 'search' in data['query']:
                return data['query']['search']
            return []
            
        except requests.RequestException as e:
            print(f"Fejl ved søgning efter {animal_name}: {e}")
            return []
    
    def get_article_summary(self, page_title: str) -> Optional[Dict]:
        """
        Hent artikel sammendrag
        """
        url = f"{self.base_url}/page/summary/{page_title}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            print(f"Fejl ved hentning af sammendrag for {page_title}: {e}")
            return None
    
    def get_article_content(self, page_title: str) -> Optional[Dict]:
        """
        Hent fuld artikel indhold
        """
        url = f"{self.base_url}/page/html/{page_title}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return {
                'title': page_title,
                'html': response.text,
                'content_type': response.headers.get('content-type')
            }
            
        except requests.RequestException as e:
            print(f"Fejl ved hentning af indhold for {page_title}: {e}")
            return None
    
    def get_article_images(self, page_title: str) -> List[Dict]:
        """
        Hent billeder fra artikel
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': page_title,
            'prop': 'images',
            'imlimit': 10
        }
        
        try:
            response = self.session.get(self.search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'images' in page_data:
                    return page_data['images']
            return []
            
        except requests.RequestException as e:
            print(f"Fejl ved hentning af billeder for {page_title}: {e}")
            return []
    
    def get_comprehensive_animal_info(self, animal_name: str) -> Dict:
        """
        Hent omfattende information om et dyr
        """
        print(f"Søger efter information om: {animal_name}")
        
        # Søg først efter artiklen
        search_results = self.search_animal(animal_name)
        
        if not search_results:
            return {
                'animal_name': animal_name,
                'found': False,
                'error': 'Ingen artikler fundet'
            }
        
        # Tag den første og mest relevante artikel
        best_match = search_results[0]
        page_title = best_match['title']
        
        print(f"Fandt artikel: {page_title}")
        
        # Hent sammendrag
        summary = self.get_article_summary(page_title)
        
        # Hent billeder
        images = self.get_article_images(page_title)
        
        # Vær høflig mod Wikipedia's servere
        time.sleep(0.5)
        
        animal_info = {
            'animal_name': animal_name,
            'found': True,
            'wikipedia_title': page_title,
            'search_snippet': best_match.get('snippet', ''),
            'summary': summary,
            'images': images,
            'wikipedia_url': f"https://{self.language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        }
        
        return animal_info
    
    def process_zoo_animal_list(self, animal_list: List[str]) -> List[Dict]:
        """
        Bearbejd en liste af dyr fra zoo
        """
        results = []
        
        for i, animal in enumerate(animal_list, 1):
            print(f"\nBehandler dyr {i}/{len(animal_list)}: {animal}")
            
            animal_info = self.get_comprehensive_animal_info(animal)
            results.append(animal_info)
            
            # Vær ekstra høflig - pause mellem hver forespørgsel
            if i < len(animal_list):
                time.sleep(1)
        
        return results
    
    def save_results(self, results: List[Dict], filename: str = 'zoo_animals_info.json'):
        """
        Gem resultaterne til en JSON fil
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\nResultater gemt i {filename}")
        except Exception as e:
            print(f"Fejl ved gemning af fil: {e}")

# Eksempel på brug
if __name__ == "__main__":
    # Initialiser scraper
    scraper = WikipediaAnimalScraper(language='en')  # Brug 'da' for dansk
    
    # Eksempel dyr fra zoo (disse kunne komme fra dit tidligere scraping)
    zoo_animals = [
        "Lion",
        "Elephant",
        "Giraffe",
        "Zebra",
        "Penguin"
    ]
    
    print("Wikipedia Zoo Animal Information Scraper")
    print("=" * 50)
    
    # Bearbejd alle dyr
    animal_results = scraper.process_zoo_animal_list(zoo_animals)
    
    # Gem resultater
    scraper.save_results(animal_results)
    
    # Vis nogle resultater
    print("\nRESULTATER:")
    print("=" * 50)
    
    for result in animal_results:
        if result['found']:
            summary = result['summary']
            if summary:
                print(f"\n{result['animal_name'].upper()}")
                print(f"Wikipedia titel: {result['wikipedia_title']}")
                print(f"Kort beskrivelse: {summary.get('extract', 'Ingen beskrivelse')[:200]}...")
                print(f"Link: {result['wikipedia_url']}")
                if result['images']:
                    print(f"Antal billeder: {len(result['images'])}")
            else:
                print(f"\n{result['animal_name']}: Fundet, men ingen sammendrag tilgængeligt")
        else:
            print(f"\n{result['animal_name']}: Ikke fundet på Wikipedia")