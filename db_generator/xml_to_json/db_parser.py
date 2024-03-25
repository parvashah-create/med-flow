import xml.etree.ElementTree as ET
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
        drug_prop_keys = ['drugbank-id', 'name', 'description', 'cas-number', 'unii', 'average-mass', 'monoisotopic-mass', 'state', 'synthesis-reference', 'indication', 'pharmacodynamics', 'mechanism-of-action', 'toxicity', 'metabolism', 'absorption', 'half-life', 'protein-binding', 'route-of-elimination', 'volume-of-distribution', 'clearance', 'fda-label', 'msds']
        drug_dict = {}

        # drug_element = self.root.find('.//{}drug'.format(self.NAMESPACE))

        drug_dict['drug_type'] = drug_element.get('type')
        drug_dict['created'] = drug_element.get('created')
        drug_dict['updated'] = drug_element.get('updated')

        for child in drug_element:
            tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
            if tag in drug_prop_keys:
                if tag == "drugbank-id" and child.attrib.get('primary') == 'true':
                    drug_dict[tag] = child.text
                elif child.text:
                    drug_dict[tag] = child.text

        return drug_dict
    
    
    # def parse_drug_prop(self, drug_element):
    #     drug_prop_keys = ['drugbank-id', 'name', 'description', 'cas-number', 'unii', 'average-mass', 'monoisotopic-mass', 'state', 'synthesis-reference', 'indication', 'pharmacodynamics', 'mechanism-of-action', 'toxicity', 'metabolism', 'absorption', 'half-life', 'protein-binding', 'route-of-elimination', 'volume-of-distribution', 'clearance', 'fda-label', 'msds']
    #     drug_dict = {
    #         'drug_type': drug_element.get('type'),
    #         'created': drug_element.get('created'),
    #         'updated': drug_element.get('updated')
    #     }

    #     for child in drug_element:
    #         tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
    #         if tag in drug_prop_keys:
    #             if tag == "drugbank-id" and child.attrib.get('primary', '') == 'true':
    #                 drug_dict[tag] = child.text
    #             elif child.text:
    #                 drug_dict[tag] = child.text

    #     return drug_dict

    def parse_sub_one(self, drug_element):
        drug_sub_one_keys = ['groups', 'synonyms', 'manufacturers', 'affected-organisms', 'food-interactions']
        drug_dict = {}

        # drug_element = self.root.find('.//{}drug'.format(self.NAMESPACE))

        for child in drug_element:
            tag = child.tag[len(self.NAMESPACE):]  # Removes namespace
            if tag in drug_sub_one_keys:
                if tag == "groups":
                    drug_dict[tag] = [group.text for group in child.findall('.//{}group'.format(self.NAMESPACE))]
                elif tag == "synonyms":
                    drug_dict[tag] = [synonym.text for synonym in child.findall('.//{}synonym'.format(self.NAMESPACE))]
                elif tag == "manufacturers":
                    manufacturer_list = [{
                        "name": manufacturer.text,
                        "generic": manufacturer.attrib.get('generic', ''),
                        "url": manufacturer.attrib.get('url', '')
                    } for manufacturer in child.findall('.//{}manufacturer'.format(self.NAMESPACE))]
                    drug_dict[tag] = manufacturer_list
                elif tag == "affected-organisms":
                    drug_dict[tag] = [org.text for org in child.findall('.//{}affected-organism'.format(self.NAMESPACE))]
                elif tag == "food-interactions":
                    drug_dict[tag] = [interaction.text for interaction in child.findall('.//{}food-interaction'.format(self.NAMESPACE))]

        return drug_dict
    
    def parse_general_references(self, drug_element):
        general_refs_element = drug_element.find('.//{}general-references'.format(self.NAMESPACE))
        if general_refs_element is None:
            return None

        general_references = {}

        for ref_type in ['articles', 'textbooks', 'links', 'attachments']:
            ref_elements = general_refs_element.find('.//{}{}'.format(self.NAMESPACE, ref_type))
            if ref_elements is not None:
                references = []
                for ref_element in ref_elements.findall('.//{}{}'.format(self.NAMESPACE, ref_type[:-1])):
                    ref_data = {}
                    for child in ref_element:
                        ref_data[child.tag.split('}')[1]] = child.text
                    references.append(ref_data)
                general_references[ref_type] = references

        return general_references
    
    def parse_classification(self, drug_element):
        classification_element = drug_element.find('.//{}classification'.format(self.NAMESPACE))
        if classification_element is None:
            return None

        classification_info = {
            'description': classification_element.find('{}description'.format(self.NAMESPACE)).text if classification_element.find('{}description'.format(self.NAMESPACE)) is not None else None,
            'direct_parent': classification_element.find('{}direct-parent'.format(self.NAMESPACE)).text if classification_element.find('{}direct-parent'.format(self.NAMESPACE)) is not None else None,
            'kingdom': classification_element.find('{}kingdom'.format(self.NAMESPACE)).text if classification_element.find('{}kingdom'.format(self.NAMESPACE)) is not None else None,
            'superclass': classification_element.find('{}superclass'.format(self.NAMESPACE)).text if classification_element.find('{}superclass'.format(self.NAMESPACE)) is not None else None,
            'class': classification_element.find('{}class'.format(self.NAMESPACE)).text if classification_element.find('{}class'.format(self.NAMESPACE)) is not None else None,
            'subclass': classification_element.find('{}subclass'.format(self.NAMESPACE)).text if classification_element.find('{}subclass'.format(self.NAMESPACE)) is not None else None,
            'alternative_parents': [elem.text for elem in classification_element.findall('{}alternative-parent'.format(self.NAMESPACE))],
            'substituents': [elem.text for elem in classification_element.findall('{}substituent'.format(self.NAMESPACE))]
        }
        return classification_info
    
    def parse_products(self, drug_element):
        products_element = drug_element.findall('.//{}product'.format(self.NAMESPACE))
        products = []

        for product_element in products_element:
            product_info = {
                'name': product_element.find('{}name'.format(self.NAMESPACE)).text if product_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
                'labeller': product_element.find('{}labeller'.format(self.NAMESPACE)).text if product_element.find('{}labeller'.format(self.NAMESPACE)) is not None else None,
                'started_marketing_on': product_element.find('{}started-marketing-on'.format(self.NAMESPACE)).text if product_element.find('{}started-marketing-on'.format(self.NAMESPACE)) is not None else None,
                'ended_marketing_on': product_element.find('{}ended-marketing-on'.format(self.NAMESPACE)).text if product_element.find('{}ended-marketing-on'.format(self.NAMESPACE)) is not None else None,
                'dosage_form': product_element.find('{}dosage-form'.format(self.NAMESPACE)).text if product_element.find('{}dosage-form'.format(self.NAMESPACE)) is not None else None,
                'strength': product_element.find('{}strength'.format(self.NAMESPACE)).text if product_element.find('{}strength'.format(self.NAMESPACE)) is not None else None,
                'route': product_element.find('{}route'.format(self.NAMESPACE)).text if product_element.find('{}route'.format(self.NAMESPACE)) is not None else None,
                'fda_application_number': product_element.find('{}fda-application-number'.format(self.NAMESPACE)).text if product_element.find('{}fda-application-number'.format(self.NAMESPACE)) is not None else None,
                'generic': product_element.find('{}generic'.format(self.NAMESPACE)).text if product_element.find('{}generic'.format(self.NAMESPACE)) is not None else None,
                'over_the_counter': product_element.find('{}over-the-counter'.format(self.NAMESPACE)).text if product_element.find('{}over-the-counter'.format(self.NAMESPACE)) is not None else None,
                'approved': product_element.find('{}approved'.format(self.NAMESPACE)).text if product_element.find('{}approved'.format(self.NAMESPACE)) is not None else None,
                'country': product_element.find('{}country'.format(self.NAMESPACE)).text if product_element.find('{}country'.format(self.NAMESPACE)) is not None else None,
                'source': product_element.find('{}source'.format(self.NAMESPACE)).text if product_element.find('{}source'.format(self.NAMESPACE)) is not None else None,
            }
            products.append(product_info)

        return products
    
    def parse_international_brands(self, drug_element):
        international_brands_element = drug_element.findall('.//{}international-brand'.format(self.NAMESPACE))
        international_brands = []

        for brand_element in international_brands_element:
            brand_info = {
                'name': brand_element.find('{}name'.format(self.NAMESPACE)).text if brand_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
                'company': brand_element.find('{}company'.format(self.NAMESPACE)).text if brand_element.find('{}company'.format(self.NAMESPACE)) is not None and brand_element.find('{}company'.format(self.NAMESPACE)).text.strip() != '' else None
            }
            international_brands.append(brand_info)

        return international_brands
    
    def parse_mixtures(self, drug_element):
        mixtures_element = drug_element.findall('.//{}mixture'.format(self.NAMESPACE))
        mixtures = []

        for mixture_element in mixtures_element:
            mixture_info = {
                'name': mixture_element.find('{}name'.format(self.NAMESPACE)).text if mixture_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
                'ingredients': mixture_element.find('{}ingredients'.format(self.NAMESPACE)).text if mixture_element.find('{}ingredients'.format(self.NAMESPACE)) is not None else None,
                'supplemental_ingredients': mixture_element.find('{}supplemental-ingredients'.format(self.NAMESPACE)).text if mixture_element.find('{}supplemental-ingredients'.format(self.NAMESPACE)) is not None else None
            }
            mixtures.append(mixture_info)

        return mixtures
    
    def parse_packagers(self, drug_element):
        packagers_element = drug_element.findall('.//{}packager'.format(self.NAMESPACE))
        packagers = []

        for packager_element in packagers_element:
            packager_info = {
                'name': packager_element.find('{}name'.format(self.NAMESPACE)).text if packager_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
                'url': packager_element.find('{}url'.format(self.NAMESPACE)).text if packager_element.find('{}url'.format(self.NAMESPACE)) is not None else None
            }
            packagers.append(packager_info)

        return packagers
    
    def parse_prices(self, drug_element):
        prices_element = drug_element.findall('.//{}price'.format(self.NAMESPACE))
        prices = []

        for price_element in prices_element:
            cost_element = price_element.find('{}cost'.format(self.NAMESPACE))
            price_info = {
                'description': price_element.find('{}description'.format(self.NAMESPACE)).text if price_element.find('{}description'.format(self.NAMESPACE)) is not None else None,
                'cost': {
                    'value': cost_element.text if cost_element is not None else None,
                    'currency': cost_element.get('currency') if cost_element is not None else None
                },
                'unit': price_element.find('{}unit'.format(self.NAMESPACE)).text if price_element.find('{}unit'.format(self.NAMESPACE)) is not None else None
            }
            prices.append(price_info)

        return prices
 
    def parse_categories(self, drug_element):
        # Finding all 'category' elements directly under the 'categories' parent element
        categories_element = drug_element.findall('.//{}categories/{}category'.format(self.NAMESPACE, self.NAMESPACE))
        categories = []

        for category_element in categories_element:
            # Extracting the text directly from the 'category' element
            category_text = category_element.find('.//{}category'.format(self.NAMESPACE)).text if category_element.find('.//{}category'.format(self.NAMESPACE)) is not None else None

            # Correctly handling mesh_id_element to prevent AttributeError
            mesh_id_element = category_element.find('.//{}mesh-id'.format(self.NAMESPACE))
            mesh_id_text = mesh_id_element.text.strip() if mesh_id_element is not None and mesh_id_element.text is not None else None

            category_info = {
                'category': category_text,
                'mesh_id': mesh_id_text
            }
            categories.append(category_info)

        return categories
    def parse_patents(self, drug_element):
        patents_element = drug_element.findall('.//{}patent'.format(self.NAMESPACE))
        patents = []

        for patent_element in patents_element:
            patent_info = {
                'number': patent_element.find('{}number'.format(self.NAMESPACE)).text if patent_element.find('{}number'.format(self.NAMESPACE)) is not None else None,
                'country': patent_element.find('{}country'.format(self.NAMESPACE)).text if patent_element.find('{}country'.format(self.NAMESPACE)) is not None else None,
                'approved': patent_element.find('{}approved'.format(self.NAMESPACE)).text if patent_element.find('{}approved'.format(self.NAMESPACE)) is not None else None,
                'expires': patent_element.find('{}expires'.format(self.NAMESPACE)).text if patent_element.find('{}expires'.format(self.NAMESPACE)) is not None else None,
                'pediatric_extension': patent_element.find('{}pediatric-extension'.format(self.NAMESPACE)).text if patent_element.find('{}pediatric-extension'.format(self.NAMESPACE)) is not None else None,
            }
            patents.append(patent_info)

        return patents
    
    def parse_drug_interactions(self, drug_element):
        drug_interactions_element = drug_element.findall('.//{}drug-interaction'.format(self.NAMESPACE))
        drug_interactions = []

        for interaction_element in drug_interactions_element:
            interaction_info = {
                'drugbank_id': interaction_element.find('{}drugbank-id'.format(self.NAMESPACE)).text if interaction_element.find('{}drugbank-id'.format(self.NAMESPACE)) is not None else None,
                'name': interaction_element.find('{}name'.format(self.NAMESPACE)).text if interaction_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
                'description': interaction_element.find('{}description'.format(self.NAMESPACE)).text if interaction_element.find('{}description'.format(self.NAMESPACE)) is not None else None,
            }
            drug_interactions.append(interaction_info)

        return drug_interactions
    
    def parse_pathways(self, drug_element):
        pathways_element = drug_element.findall('.//{}pathway'.format(self.NAMESPACE))
        pathways = []

        for pathway_element in pathways_element:
            pathway_info = {
                'smpdb_id': pathway_element.find('{}smpdb-id'.format(self.NAMESPACE)).text if pathway_element.find('{}smpdb-id'.format(self.NAMESPACE)) is not None else None,
                'name': pathway_element.find('{}name'.format(self.NAMESPACE)).text if pathway_element.find('{}name'.format(self.NAMESPACE)) is not None else None,
                'category': pathway_element.find('{}category'.format(self.NAMESPACE)).text if pathway_element.find('{}category'.format(self.NAMESPACE)) is not None else None,
                'drugs': [{
                    'drugbank_id': drug.find('{}drugbank-id'.format(self.NAMESPACE)).text if drug.find('{}drugbank-id'.format(self.NAMESPACE)) is not None else None,
                    'name': drug.find('{}name'.format(self.NAMESPACE)).text if drug.find('{}name'.format(self.NAMESPACE)) is not None else None
                } for drug in pathway_element.findall('.//{}drug'.format(self.NAMESPACE))]
            }
            pathways.append(pathway_info)

        return pathways
    
    def parse_all_drug_data(self,drug_element):
            # Parse individual components
            parse_drug_prop =  self.parse_drug_prop(drug_element)
            parse_sub_one = self.parse_sub_one(drug_element)
            parse_general_references = self.parse_general_references(drug_element)
            parse_classification = self.parse_classification(drug_element)
            parse_products = self.parse_products(drug_element)
            parse_international_brands = self.parse_international_brands(drug_element)
            parse_mixtures = self.parse_mixtures(drug_element)
            parse_packagers = self.parse_packagers(drug_element)
            parse_prices = self.parse_prices(drug_element)
            parse_categories = self.parse_categories(drug_element)
            parse_patents = self.parse_patents(drug_element)
            parse_drug_interactions = self.parse_drug_interactions(drug_element)
            parse_pathways = self.parse_pathways(drug_element)
            
            # Compile all data into a dictionary
            all_data = {
                "drug_properties": parse_drug_prop,
                "substance_information": parse_sub_one,
                "general_references": parse_general_references,
                "classification": parse_classification,
                "products": parse_products,
                "international_brands": parse_international_brands,
                "mixtures": parse_mixtures,
                "packagers": parse_packagers,
                "prices": parse_prices,
                "categories": parse_categories,
                "patents": parse_patents,
                "drug_interactions": parse_drug_interactions,
                "pathways": parse_pathways
            }
            
            return all_data
    


    def parse_all_drugs(self):
        # Find all 'drug' elements
        all_drug_elements = self.root.findall('.//{}drug'.format(self.NAMESPACE))
        drug_elements = []

        for element in all_drug_elements:
            # if element.get("type") or element.get('created') or element.get('updated'):
            if element.get('updated'):

                drug_elements.append(element)

        
    


        
        all_drug_props = [self.parse_all_drug_data(drug_element) for drug_element in drug_elements]
        # all_drug_props = len(drug_elements)

        return all_drug_props
    



            
            



# file_path = 'data/sample.xml'
# dbdb = drugbank_db(file_path)
# drug_dict = dbdb.parse_all_drugs()
# print(drug_dict)

# # Assuming drug_dict is your dictionary containing all the drugs information
# file_path = 'data/drug_dict.json'  # Define the path where you want to save the file
# with open(file_path, 'w') as json_file:
#     json.dump(drug_dict, json_file, indent=4)
