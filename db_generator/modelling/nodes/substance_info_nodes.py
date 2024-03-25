from graph_db.connector import Neo4jConnection
from db_generator.modelling.utils import preprocess_drug_text

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


def create_substance_info_nodes(drugbank_id, substance_dict):

    substance_dict["drugbank_id"] = drugbank_id

    substance_dict['food_interactions'] = [{'advice': food_interaction, 
                                'embed_text': preprocess_drug_text(food_interaction)} 
                                for food_interaction in substance_dict.get('food_interactions', [])]



    uri = os.getenv("NEO4J_URI") 
    username = os.getenv("NEO4J_USER")            
    password = os.getenv("NEO4J_PASSWORD")

    auth = (username, password)

    # Create an instance of the Neo4jConnection class
    conn = GraphDatabase.driver(uri, auth=auth)

    # Cypher query to create the DrugNode with the given attributes
    create_drug_node_query = """
        // Assuming you have created or merged the drug node previously and it's identified by 'drugbank_id'
        MATCH (d:Drug {drugbank_id: $drugbank_id})
        // Groups
        WITH d
        UNWIND CASE WHEN size($groups) > 0 THEN $groups ELSE [null] END AS group
        FOREACH (ignoreMe IN CASE WHEN group IS NOT NULL THEN [1] ELSE [] END |
            MERGE (g:Group {name: group})
            MERGE (d)-[:BELONGS_TO_GROUP]->(g)
        )
        // Synonyms
        WITH d
        UNWIND CASE WHEN size($synonyms) > 0 THEN $synonyms ELSE [null] END AS synonym
        FOREACH (ignoreMe IN CASE WHEN synonym IS NOT NULL THEN [1] ELSE [] END |
            MERGE (s:Synonym {name: synonym})
            MERGE (d)-[:HAS_SYNONYM]->(s)
        )
        // Manufacturers
        WITH d
        UNWIND CASE WHEN size($manufacturers) > 0 THEN $manufacturers ELSE [null] END AS manufacturer
        FOREACH (ignoreMe IN CASE WHEN manufacturer IS NOT NULL THEN [1] ELSE [] END |
            MERGE (m:Manufacturer {name: manufacturer.name, generic: manufacturer.generic, url: manufacturer.url})
            MERGE (d)-[:MANUFACTURED_BY]->(m)
        )
        // Food Interactions
        WITH d
        UNWIND CASE WHEN size($food_interactions) > 0 THEN $food_interactions ELSE [null] END AS food_interaction
        FOREACH (ignoreMe IN CASE WHEN food_interaction IS NOT NULL THEN [1] ELSE [] END |
            MERGE (f:FoodInteraction {advice: food_interaction.advice})
            ON CREATE SET f.embed_text = food_interaction.embed_text
            MERGE (d)-[:HAS_FOOD_INTERACTION]->(f)
        )
        RETURN d;
    """

    # Execute the query
    result = conn.execute_query(create_drug_node_query, substance_dict)

    # Close the connection
    conn.close()


    return True


# create_substance_info_nodes(substance_dict)
