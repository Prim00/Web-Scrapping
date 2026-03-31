import requests
from bs4 import BeautifulSoup

# Fonction pour nettoyer et convertir un texte de prix en float.
def clean_price(price_text):
    """
    Nettoie et convertit un texte de prix en float.
    """
    try:
        return float(
            price_text.replace('TND', '')  # Supprime la devise tunisienne.
                      .replace('DT', '')   # Supprime une autre variante de la devise.
                      .replace(',', '')    # Supprime les virgules (ex. séparateurs de milliers).
                      .replace('\u202f', '')  # Supprime les espaces fines insécables.
                      .replace('\xa0', '')  # Supprime les espaces insécables.
                      .strip()  # Supprime les espaces en début et fin de chaîne.
        )
    except ValueError:
        # Retourne None si la conversion échoue.
        return None

# Fonction pour récupérer le prix d'un article depuis le site MyTek.
def fetch_price_from_mytek(article):
    try:
        # URL de recherche pour l'article sur MyTek.
        url = f"https://www.mytek.tn/catalogsearch/result/?q={article.replace(' ', '+')}"
        response = requests.get(url, timeout=10)  # Requête HTTP avec un délai d'attente.
        
        soup = BeautifulSoup(response.text, 'html.parser')  # Analyse du HTML avec BeautifulSoup.
        price_tag = soup.find('span', class_='price')  # Recherche de l'élément contenant le prix.
        if price_tag:
            price_text = price_tag.text.strip()  # Extrait et nettoie le texte du prix.
            print(f"Prix brut récupéré sur MyTek : {price_text}")  # Affichage pour débogage.
            return clean_price(price_text)  # Nettoie et convertit le prix.
        print("Aucun prix trouvé pour cet article sur mytek.")
        return None  # Retourne None si aucun prix n'est trouvé.
    except Exception as e:
        # Capture et affiche les erreurs éventuelles.
        print(f"Erreur lors de la récupération du prix sur MyTek : {e}")
        return None

# Fonction pour récupérer le prix depuis Technopro.
def fetch_price_from_technopro(article):
    try:
        url = f"https://www.technopro-online.com/recherche?controller=search&s={article.replace(' ', '+')}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Identifier la balise et la classe contenant le prix
        price_tag = soup.find('span', class_='product-price')  # Adaptez selon la structure HTML du site.
        
        if price_tag:
            price_text = price_tag.text.strip()
            print(f"Prix brut récupéré sur Technopro : {price_text}")
            return clean_price(price_text)
        
        # Si aucun prix n'est trouvé, afficher un message.
        print("Aucun prix trouvé pour cet article sur Technopro.")
        return None

    except Exception as e:
        print(f"Erreur lors de la récupération du prix sur Technopro : {e}")
        return None

# Fonction pour récupérer le prix depuis Spacenet.
def fetch_price_from_spacenet(article):
    try:
        url = f"https://spacenet.tn/recherche?controller=search&s={article.replace(' ', '+')}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_tag = soup.find('span', class_='price')
        if price_tag:
            price_text = price_tag.text.strip()
            print(f"Prix brut récupéré sur Spacenet : {price_text}")
            return clean_price(price_text)
        print("Aucun prix trouvé pour cet article sur Spacenet.")
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération du prix sur Spacenet : {e}")
        return None

# Fonction pour trouver le prix le plus bas parmi les sites.
def find_lowest_price(article):
    # Récupère les prix depuis les différents sites.
    prices = {
        "MyTek": fetch_price_from_mytek(article),
        "Technopro": fetch_price_from_technopro(article),
        "Spacenet": fetch_price_from_spacenet(article),
    }

    # Filtre les prix valides (non None).
    valid_prices = {site: price for site, price in prices.items() if price is not None}
    
    if not valid_prices:
        # Affiche un message si aucun prix valide n'est trouvé.
        print("Aucun prix valide trouvé pour cet article.")
        return

    # Trouve le site avec le prix le plus bas.
    lowest_site = min(valid_prices, key=valid_prices.get)
    print("\n")
    print(f"Le prix le plus bas est sur {lowest_site} : {valid_prices[lowest_site]:.3f} TND")

# Exemple d'utilisation de la fonction.
article = input("Donner un article : ")
find_lowest_price(article)
