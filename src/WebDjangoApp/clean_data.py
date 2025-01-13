# Lire le fichier data.json et remplacer toutes les entités HTML par des caractères normaux (é, è, à, etc.)
# Enregistrer le fichier nettoyé dans un fichier cleaned_data.json
import html
import re

with open("data.json", "r", encoding="utf-8") as f:
    data = f.read()

# Supprimer toutes les balises HTML
data_no_tags = re.sub(r'<[^>]+>', '', data)

# Utiliser html.unescape() pour convertir les entités HTML
cleaned_data = html.unescape(data_no_tags)

# Écrire les données nettoyées dans un nouveau fichier
with open("cleaned_data.json", "w", encoding="utf-8") as f:
    f.write(cleaned_data)
