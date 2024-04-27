# from graph_db.connector import Neo4jConnection
# import os

# def create_price_nodes(drug_id, prices):
#     # Connect to the local Neo4j instance
#     uri = os.getenv("NEO4J_URI") 
#     user = os.getenv("NEO4J_USER") 
#     password = os.getenv("NEO4J_PASSWORD")  

#     # Create an instance of the Neo4jConnection class
#     conn = Neo4jConnection(uri, user, password)

#     # Cypher query to create price nodes and relationships
#     create_price_query = """

#     MATCH (d:Drug {drugbank_id: $drug_id})
#     UNWIND $prices as price
#     WITH d, price
#     WHERE price.description IS NOT NULL AND price.description <> ''
#     MERGE (p:Price {description: price.description, value: price.cost.value, currency: price.cost.currency, unit: price.unit})
#     MERGE (d)-[:HAS_PRICE]->(p)
#     RETURN d, p;

#     """

#     # Prepare the data for the query
#     data = {
#         'drug_id': drug_id,
#         'prices': prices
#     }

#     # Execute the query
#     result = conn.execute_query(create_price_query, data)

#     # Close the connection
#     conn.close()

#     return True
from graph_db.connector import Neo4jConnection
from neo4j import GraphDatabase
import os
from db_generator.modelling.utils import preprocess_drug_text
from dotenv import load_dotenv


load_dotenv()
def create_price_nodes(drug_id, prices):
    # Connect to the local Neo4j instance
    uri = os.getenv("NEO4J_URI") 
    username = os.getenv("NEO4J_USER")            
    password = os.getenv("NEO4J_PASSWORD")

    auth = (username, password)

    # Create an instance of the Neo4jConnection class
    conn = GraphDatabase.driver(uri, auth=auth)


    # Cypher query to create price nodes and relationships
    create_price_query = """
    MATCH (d:Drug {drugbank_id: $drug_id})
    UNWIND $prices as price
    WITH d, price
    WHERE price.description IS NOT NULL AND price.description <> ''
    MERGE (p:Price {
        description: price.description, 
        embed_text: price.embed_text, 
        value: price.cost.value, 
        currency: price.cost.currency, 
        unit: price.unit})
    MERGE (d)-[:HAS_PRICE]->(p)
    RETURN d, p;
    """

    # Prepare the data for the query
    preprocessed_prices = [{
        'description': price['description'],
        'embed_text': preprocess_drug_text(price['description'] + ' ' +price["cost"]["value"] +' '+ price["cost"]["currency"] + ' ' + price["unit"] ),  # Preprocess the description for embedding
        'cost': price['cost'],
        'unit': price['unit']
    } for price in prices]

    data = {
        'drug_id': drug_id,
        'prices': preprocessed_prices
    }

    # Execute the query
    result = conn.execute_query(create_price_query, data)

    # Close the connection
    conn.close()

    return True


# drug_id = 'BIOD00024'  
# prices = [
#     {
#         'description': 'Refludan 50 mg vial',
#         'cost': {
#             'value': '273.19',
#             'currency': 'USD'
#         },
#         'unit': 'vial'
#     }
# ]

# create_price_nodes(drug_id, prices)