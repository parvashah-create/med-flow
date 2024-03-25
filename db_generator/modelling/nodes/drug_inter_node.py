from graph_db.connector import Neo4jConnection
from neo4j import GraphDatabase
import os
from db_generator.modelling.utils import preprocess_drug_text
from dotenv import load_dotenv



load_dotenv()
# def create_drug_interaction_nodes(drug_id, drug_interactions):
#     # Connect to the local Neo4j instance
#     uri = os.getenv("NEO4J_URI")  # Default URI for Neo4j
#     user = os.getenv("NEO4J_USER")  # Default user for Neo4j
#     password = os.getenv("NEO4J_PASSWORD")  # Your actual Neo4j password

#     # Create an instance of the Neo4jConnection class
#     conn = Neo4jConnection(uri, user, password)

#     create_interaction_query = """

#     MERGE (d:Drug {drugbank_id: $drug_id})
#     WITH d  
#     UNWIND $interactions as interaction
#     MERGE (i:Drug {drugbank_id: interaction.drugbank_id})
#     ON CREATE SET i.name = interaction.name
#     MERGE (d)-[r:INTERACTS_WITH]->(i)
#     ON CREATE SET r.description = interaction.description
#     ON MATCH SET r.description = interaction.description
#     RETURN d, i, r;

#     """



#     # Prepare the data for the query
#     data = {
#         'drug_id': drug_id,
#         'interactions': drug_interactions
#     }

#     # Execute the query
#     result = conn.execute_query(create_interaction_query, data)

#     # Close the connection
#     conn.close()

#     return True



def create_drug_interaction_nodes(drug_id, drug_interactions):
    uri = os.getenv("NEO4J_URI") 
    username = os.getenv("NEO4J_USER")            
    password = os.getenv("NEO4J_PASSWORD")

    auth = (username, password)

    # Create an instance of the Neo4jConnection class
    conn = GraphDatabase.driver(uri, auth=auth)


    # Cypher query to create Drug nodes and their INTERACTS_WITH relationships
    create_interaction_query = """
    MERGE (d:Drug {drugbank_id: $drug_id})
    WITH d  
    UNWIND $interactions as interaction
    MERGE (i:Drug {drugbank_id: interaction.drugbank_id})
    ON CREATE SET i.name = interaction.name
    MERGE (d)-[r:INTERACTS_WITH]->(i)
    ON CREATE SET r.description = interaction.description, r.embed_text = interaction.embed_text
    ON MATCH SET r.description = interaction.description, r.embed_text = interaction.embed_text
    RETURN d, i, r;
    """

    # Prepare the data for the query
    preprocessed_interactions = [{
        'drugbank_id': interaction['drugbank_id'],
        'name': interaction['name'],
        'description': interaction['description'],
        'embed_text': preprocess_drug_text(interaction['description']) 
    } for interaction in drug_interactions]

    data = {
        'drug_id': drug_id,
        'interactions': preprocessed_interactions
    }

    # Execute the query
    result = conn.execute_query(create_interaction_query, data)

    # Close the connection
    conn.close()

    return True