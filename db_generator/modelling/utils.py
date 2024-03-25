import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_drug_text(text):
    # Convert to lowercase
    text = text.lower()
    # Handle specific drug data cases (e.g., replace slashes with spaces, keep decimal points)
    text = text.replace('/', ' ')
    text = re.sub(r'(?<!\d)\.|\.(?!\d)', ' ', text)  # Remove periods that are not part of a decimal number
    # Remove other special characters, but keep the chemical components like '-' in compounds
    text = re.sub(r'[^a-z0-9-. ]', ' ', text)
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words and perform lemmatization with medical adjustments
    stop_words = set(stopwords.words('english')) 
    lemmatizer = WordNetLemmatizer()
    preprocessed_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 1]  # Remove single characters
    # Join tokens back into a string
    preprocessed_text = ' '.join(preprocessed_tokens)
    return preprocessed_text




# processed_text = preprocess_drug_text("Lepirudin is a recombinant hirudin formed by 65 amino acids that acts as a highly specific and direct thrombin inhibitor.[L41539,L41569] Natural hirudin is an endogenous anticoagulant found in _Hirudo medicinalis_ leeches.[L41539] Lepirudin is produced in yeast cells and is identical to natural hirudin except for the absence of sulfate on the tyrosine residue at position 63 and the substitution of leucine for isoleucine at position 1 (N-terminal end).[A246609] Lepirudin is used as an anticoagulant in patients with heparin-induced thrombocytopenia (HIT), an immune reaction associated with a high risk of thromboembolic complications.[A3, L41539] HIT is caused by the expression of immunoglobulin G (IgG) antibodies that bind to the complex formed by heparin and platelet factor 4. This activates endothelial cells and platelets and enhances the formation of thrombi.[A246609] Bayer ceased the production of lepirudin (Refludan) effective May 31, 2012.[L41574]")

# print(processed_text)