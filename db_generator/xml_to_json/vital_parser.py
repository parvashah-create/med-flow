# import xml.etree.ElementTree as ET
# import json
# from tqdm import tqdm

# class drugbank_db:
#     NAMESPACE = '{http://www.drugbank.ca}'

#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.root = self.parse_xml()

#     def parse_xml(self):
#         tree = ET.parse(self.file_path)
#         return tree.getroot()
    
#     def parse_drug_prop(self, drug_element):
#         drug_prop_keys = ['drugbank-id', 'name', 'description','state', 'indication', 'pharmacodynamics', 'mechanism-of-action', 'toxicity', 'metabolism', 'absorption', 'half-life', 'protein-binding', 'route-of-elimination', 'volume-of-distribution', 'clearance']
#         drug_dict = {}

#         # drug_element = self.root.find('.//{}drug'.format(self.NAMESPACE))

#         drug_dict['drug_type'] = drug_element.get('type')
#         drug_dict['created'] = drug_element.get('created')
#         drug_dict['updated'] = drug_element.get('updated')

#         for child in drug_element:
#             tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
#             if tag in drug_prop_keys:
#                 if tag == "drugbank-id" and child.attrib.get('primary') == 'true':
#                     drug_dict[tag] = child.text
#                 elif child.text:
#                     drug_dict[tag] = child.text

#         return drug_dict
    

#     def parse_sub_one(self, drug_element):
#         drug_sub_one_keys = ['groups', 'synonyms', 'manufacturers', 'food-interactions']
#         drug_dict = {}

#         # drug_element = self.root.find('.//{}drug'.format(self.NAMESPACE))

#         for child in drug_element:
#             tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
#             if tag in drug_sub_one_keys:
#                 if tag == "groups":
#                     drug_dict[tag] = [group.text for group in child.findall('.//{}group'.format(self.NAMESPACE))]
#                 elif tag == "synonyms":
#                     drug_dict[tag] = [synonym.text for synonym in child.findall('.//{}synonym'.format(self.NAMESPACE))]
#                 elif tag == "manufacturers":
#                     manufacturer_list = [{
#                         "name": manufacturer.text,
#                         "generic": manufacturer.attrib.get('generic', ''),
#                         "url": manufacturer.attrib.get('url', '')
#                     } for manufacturer in child.findall('.//{}manufacturer'.format(self.NAMESPACE))]
#                     drug_dict[tag] = manufacturer_list
#                 elif tag == "affected-organisms":
#                     drug_dict[tag] = [org.text for org in child.findall('.//{}affected-organism'.format(self.NAMESPACE))]
#                 elif tag == "food-interactions":
#                     drug_dict[tag] = [interaction.text for interaction in child.findall('.//{}food-interaction'.format(self.NAMESPACE))]

#         return drug_dict
    

    

    
#     def parse_prices(self, drug_element):
#         prices_element = drug_element.findall('.//{}price'.format(self.NAMESPACE))
#         prices = []

#         for price_element in prices_element:
#             cost_element = price_element.find('{}cost'.format(self.NAMESPACE))
#             price_info = {
#                 'description': price_element.find('{}description'.format(self.NAMESPACE)).text if price_element.find('{}description'.format(self.NAMESPACE)) is not None else None,
#                 'cost': {
#                     'value': cost_element.text if cost_element is not None else None,
#                     'currency': cost_element.get('currency') if cost_element is not None else None
#                 },
#                 'unit': price_element.find('{}unit'.format(self.NAMESPACE)).text if price_element.find('{}unit'.format(self.NAMESPACE)) is not None else None
#             }
#             prices.append(price_info)

#         return prices
 
    
#     def parse_drug_interactions(self, drug_element):
#         drug_interactions_element = drug_element.findall('.//{}drug-interaction'.format(self.NAMESPACE))
#         drug_interactions = []

#         for interaction_element in drug_interactions_element:
#             interaction_info = {
#                 'drugbank_id': interaction_element.find('{}drugbank-id'.format(self.NAMESPACE)).text if interaction_element.find('{}drugbank-id'.format(self.NAMESPACE)) is not None else None,
#                 'name': interaction_element.find('{}name'.format(self.NAMESPACE)).text if interaction_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
#                 'description': interaction_element.find('{}description'.format(self.NAMESPACE)).text if interaction_element.find('{}description'.format(self.NAMESPACE)) is not None else None,
#             }
#             drug_interactions.append(interaction_info)

#         return drug_interactions
    
#     def parse_all_drug_data(self,drug_element):
#             # Parse individual components
#             parse_drug_prop =  self.parse_drug_prop(drug_element)
#             parse_sub_one = self.parse_sub_one(drug_element)
#             parse_prices = self.parse_prices(drug_element)
#             parse_drug_interactions = self.parse_drug_interactions(drug_element)
            
#             # Compile all data into a dictionary
#             all_data = {
#                 "drug_properties": parse_drug_prop,
#                 "substance_information": parse_sub_one,
#                 "prices": parse_prices,
#                 "drug_interactions": parse_drug_interactions,
#             }
            
#             return all_data
    


#     def parse_all_drugs(self):
#         # Find all 'drug' elements
#         all_drug_elements = self.root.findall('.//{}drug'.format(self.NAMESPACE))
#         drug_elements = []

#         for element in tqdm(all_drug_elements):
#             # if element.get("type") or element.get('created') or element.get('updated'):
#             if element.get('updated'):

#                 drug_elements.append(element)

#         all_drug_props = []
#         error_list = []

#         for drug_element in tqdm(drug_elements):
#             try:
#                 # Attempt to parse each drug's data
#                 drug_data = self.parse_all_drug_data(drug_element)
#                 all_drug_props.append(drug_data)
#             except Exception as e:
#                 error_list.append(str(e))

#                 continue

#         return all_drug_props



            
            
import xml.etree.ElementTree as ET
from tqdm import tqdm
import json

class drugbank_db:
    NAMESPACE = '{http://www.drugbank.ca}'

    def __init__(self, file_path):
        self.file_path = file_path
        self.root = self.parse_xml()

    def parse_xml(self):
        tree = ET.parse(self.file_path)
        return tree.getroot()

    def parse_drug_prop(self, drug_element):
        drug_prop_keys = ['drugbank-id', 'name', 'description', 'state', 'indication', 'pharmacodynamics', 'mechanism-of-action', 'toxicity', 'metabolism', 'absorption', 'half-life', 'protein-binding', 'route-of-elimination', 'volume-of-distribution', 'clearance']
        drug_dict = {}

        drug_dict['drug_type'] = drug_element.get('type', '')
        drug_dict['created'] = drug_element.get('created', '')
        drug_dict['updated'] = drug_element.get('updated', '')

        
        for child in drug_element:
            tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
            if tag in drug_prop_keys:
                if tag == "drugbank-id" and child.attrib.get('primary') == 'true':
                    drug_dict[tag] = child.text
                elif child.text:
                    drug_dict[tag] = child.text

        return drug_dict
    

    

    def parse_sub_one(self, drug_element):
        drug_sub_one_keys = ['groups', 'synonyms', 'manufacturers', 'food-interactions']
        drug_dict = {}

        for child in drug_element:
            tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
            if tag in drug_sub_one_keys:
                elements = child.findall('.//{}{}'.format(self.NAMESPACE, tag[:-1]))  # Find all elements of the current tag
                if tag in ['groups', 'synonyms', 'food-interactions']:
                    drug_dict[tag] = [elem.text if elem.text is not None else '' for elem in elements]
                elif tag == "manufacturers":
                    drug_dict[tag] = [
                        {
                            "name": manufacturer.text if manufacturer.text is not None else '',
                            "generic": manufacturer.attrib.get('generic', ''),
                            "url": manufacturer.attrib.get('url', '')
                        } for manufacturer in elements
                    ]

        return drug_dict

    def parse_prices(self, drug_element):
        prices_element = drug_element.findall('.//{}price'.format(self.NAMESPACE))
        prices = []

        for price_element in prices_element:
            price_info = {
                'description': (price_element.find('{}description'.format(self.NAMESPACE)).text if price_element.find('{}description'.format(self.NAMESPACE)) is not None else ''),
                'cost': {
                    'value': (price_element.find('{}cost'.format(self.NAMESPACE)).text if price_element.find('{}cost'.format(self.NAMESPACE)) is not None else ''),
                    'currency': (price_element.find('{}cost'.format(self.NAMESPACE)).get('currency') if price_element.find('{}cost'.format(self.NAMESPACE)) is not None else '')
                },
                'unit': (price_element.find('{}unit'.format(self.NAMESPACE)).text if price_element.find('{}unit'.format(self.NAMESPACE)) is not None else '')
            }
            prices.append(price_info)

        return prices

    def parse_drug_interactions(self, drug_element):
        drug_interactions_element = drug_element.findall('.//{}drug-interaction'.format(self.NAMESPACE))
        drug_interactions = []

        for interaction_element in drug_interactions_element:
            interaction_info = {
                'drugbank_id': (interaction_element.find('{}drugbank-id'.format(self.NAMESPACE)).text if interaction_element.find('{}drugbank-id'.format(self.NAMESPACE)) is not None else ''),
                'name': (interaction_element.find('{}name'.format(self.NAMESPACE)).text if interaction_element.find('{}name'.format(self.NAMESPACE)) is not None else ''),
                'description': (interaction_element.find('{}description'.format(self.NAMESPACE)).text if interaction_element.find('{}description'.format(self.NAMESPACE)) is not None else ''),
            }
            drug_interactions.append(interaction_info)

        return drug_interactions
    
    def parse_all_drug_data(self, drug_element):
        # Parse individual components
        drug_prop = self.parse_drug_prop(drug_element)
        sub_one = self.parse_sub_one(drug_element)
        prices = self.parse_prices(drug_element)
        drug_interactions = self.parse_drug_interactions(drug_element)

        # Compile all data into a dictionary
        all_data = {
            "drug_properties": drug_prop,
            "substance_information": sub_one,
            "prices": prices,
            "drug_interactions": drug_interactions,
        }

        return all_data

    def parse_all_drugs(self):
        # Find all 'drug' elements
   
        # all_drug_elements = self.root.findall('.//{}drug'.format(self.NAMESPACE))
        all_drug_elements = self.root.findall('{}drug'.format(self.NAMESPACE))
        all_drug_props = []
        error_list = []
        
        for drug_element in tqdm(all_drug_elements[:100], desc="Parsing drugs"):
        # for drug_element in tqdm(all_drug_elements, desc="Parsing drugs"):
            
            try:
                # Attempt to parse each drug's data
                drug_data = self.parse_all_drug_data(drug_element)
                all_drug_props.append(drug_data)
            except Exception as e:
                # If there's an error, add it to the error_list
                error_list.append({'error': str(e), 'drug': drug_element.find(f'{self.NAMESPACE}name').text if drug_element.find(f'{self.NAMESPACE}name') is not None else 'Unknown'})

        return all_drug_props, error_list





def replace_keys(obj):
    """Recursively go through the dictionary obj and replace keys containing '-' with '_'."""
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = key.replace('-', '_')  # Replace '-' with '_'
            new_obj[new_key] = replace_keys(value)  # Recursively replace keys
        return new_obj
    elif isinstance(obj, list):
        return [replace_keys(item) for item in obj]  # Recursively replace keys in list
    else:
        return obj
    
# file_path = 'data/full_database.xml'
# dbdb = drugbank_db(file_path)
# drug_dict, error_list = dbdb.parse_all_drugs()


# file_path = 'data/sample_drug_dict.json'
# mod_drug_dict = replace_keys(drug_dict)
# with open(file_path, 'w') as json_file:
#     json.dump(mod_drug_dict, json_file, indent=4)

    