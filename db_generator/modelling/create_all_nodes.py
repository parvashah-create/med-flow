import os
import json
from db_generator.modelling.nodes.drug_inter_node import create_drug_interaction_nodes
from db_generator.modelling.nodes.drug_node import create_drug_and_related_nodes
from db_generator.modelling.nodes.prices_node import create_price_nodes
from db_generator.modelling.nodes.substance_info_nodes import create_substance_info_nodes


from tqdm import tqdm

def create_all_nodes_and_relationships_for_drug(all_data):

    for drug_data in tqdm(all_data):

        
        drug_id = drug_data['drug_properties'].get('drugbank_id')
  
        if not drug_id:
            continue 

        # Create nodes for drug properties
        create_drug_and_related_nodes(drug_id, drug_data['drug_properties'])

        # Create nodes for prices
        create_price_nodes(drug_id, drug_data['prices'])

        # Create nodes for drug interactions
        create_drug_interaction_nodes(drug_id, drug_data['drug_interactions'])

        # Create nodes for substance information
        create_substance_info_nodes(drug_id, drug_data['substance_information'])




# Load data from a JSON file
# def load_data_from_json(filename):
#     with open(filename, 'r') as file:
#         data = json.load(file)
#     return data

# # Specify the path to your JSON file
# json_file_path = 'data/sample_drug_dict.json'

# # Load the data
# all_data = load_data_from_json(json_file_path)

# # Create all nodes and relationships for each drug
# create_all_nodes_and_relationships_for_drug(all_data)