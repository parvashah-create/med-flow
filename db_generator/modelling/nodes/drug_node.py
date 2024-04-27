from graph_db.connector import Neo4jConnection
from neo4j import GraphDatabase
from db_generator.modelling.utils import preprocess_drug_text
import os
from dotenv import load_dotenv


load_dotenv()

def create_drug_and_related_nodes(drugbank_id, drug_properties):


    uri = os.getenv("NEO4J_URI") 
    username = os.getenv("NEO4J_USER")            
    password = os.getenv("NEO4J_PASSWORD")

    auth = (username, password)

    print(uri)
    # Create an instance of the Neo4jConnection class
    conn = GraphDatabase.driver(uri, auth=auth)

    print(conn)

    # Cypher query to create the DrugNode and related nodes
    create_nodes_query = """
    MERGE (d:Drug {drugbank_id: $drugbank_id, name: $name, drug_type: $drug_type, state: $state, description: $description, embed_text:$drug_embed_text})
    // Indication
    FOREACH (ignoreMe IN CASE WHEN $indication IS NOT NULL AND $indication <> '' THEN [1] ELSE [] END |
        MERGE (ind:Indication {description: $indication, embed_text:$indication_embed_text})
        MERGE (d)-[:HAS_INDICATION]->(ind)
    )
    // Pharmacodynamics
    FOREACH (ignoreMe IN CASE WHEN $pharmacodynamics IS NOT NULL AND $pharmacodynamics <> '' THEN [1] ELSE [] END |
        MERGE (pd:Pharmacodynamics {description: $pharmacodynamics, embed_text:$pd_embed_text})
        MERGE (d)-[:HAS_PHARMACODYNAMICS]->(pd)
    )
    // Mechanism of Action
    FOREACH (ignoreMe IN CASE WHEN $mechanism_of_action IS NOT NULL AND $mechanism_of_action <> '' THEN [1] ELSE [] END |
        MERGE (moa:MechanismOfAction {description: $mechanism_of_action, embed_text:$moa_embed_text})
        MERGE (d)-[:HAS_MECHANISM]->(moa)
    )
    // Metabolism
    FOREACH (ignoreMe IN CASE WHEN $metabolism IS NOT NULL AND $metabolism <> '' THEN [1] ELSE [] END |
        MERGE (met:Metabolism {description: $metabolism, embed_text:$met_embed_text})
        MERGE (d)-[:HAS_METABOLISM]->(met)
    )
    // Absorption
    FOREACH (ignoreMe IN CASE WHEN $absorption IS NOT NULL AND $absorption <> '' THEN [1] ELSE [] END |
        MERGE (abs:Absorption {description: $absorption, embed_text:$abs_embed_text})
        MERGE (d)-[:HAS_ABSORPTION]->(abs)
    )
    // Toxicity
    FOREACH (ignoreMe IN CASE WHEN $toxicity IS NOT NULL AND $toxicity <> '' THEN [1] ELSE [] END |
        MERGE (tox:Toxicity {description: $toxicity, embed_text:$tox_embed_text})
        MERGE (d)-[:HAS_TOXICITY]->(tox)
    )
    // Half Life
    FOREACH (ignoreMe IN CASE WHEN $half_life IS NOT NULL AND $half_life <> '' THEN [1] ELSE [] END |
        MERGE (hl:HalfLife {description: $half_life, embed_text:$hl_embed_text})
        MERGE (d)-[:HAS_HALFLIFE]->(hl)
    )
    // Protein Binding
    FOREACH (ignoreMe IN CASE WHEN $protein_binding IS NOT NULL AND $protein_binding <> '' THEN [1] ELSE [] END |
        MERGE (pb:ProteinBinding {description: $protein_binding, embed_text:$prb_embed_text})
        MERGE (d)-[:HAS_PROTEINBINDING]->(pb)
    )
    // Route of Elimination
    FOREACH (ignoreMe IN CASE WHEN $route_of_elimination IS NOT NULL AND $route_of_elimination <> '' THEN [1] ELSE [] END |
        MERGE (roe:RouteOfElimination {description: $route_of_elimination, embed_text:$roe_embed_text})
        MERGE (d)-[:HAS_ROUTE_OF_ELIMINATION]->(roe)
    )
    // Volume of Distribution
    FOREACH (ignoreMe IN CASE WHEN $volume_of_distribution IS NOT NULL AND $volume_of_distribution <> '' THEN [1] ELSE [] END |
        MERGE (vod:VolumeOfDistribution {description: $volume_of_distribution, embed_text:$vod_embed_text})
        MERGE (d)-[:HAS_VOLUME_OF_DISTRIBUTION]->(vod)
    )
    // Clearance
    FOREACH (ignoreMe IN CASE WHEN $clearance IS NOT NULL AND $clearance <> '' THEN [1] ELSE [] END |
        MERGE (clr:Clearance {description: $clearance, embed_text:$clr_embed_text})
        MERGE (d)-[:HAS_CLEARANCE]->(clr)
    )
    RETURN d;
    """

    # Prepare the drug attributes
    drug_attributes = {
        'drugbank_id': drugbank_id,
        'name': drug_properties.get('name', ''),
        'drug_type': drug_properties.get('drug_type', ''),
        'state': drug_properties.get('state', ''),
        'description': drug_properties.get('description', ''),
        'indication': drug_properties.get('indication', ''),
        'pharmacodynamics': drug_properties.get('pharmacodynamics', ''),
        'mechanism_of_action': drug_properties.get('mechanism_of_action', ''),
        'metabolism': drug_properties.get('metabolism', ''),
        'absorption': drug_properties.get('absorption', ''),
        'toxicity': drug_properties.get('toxicity', ''),
        'half_life': drug_properties.get('half_life', ''),
        'protein_binding': drug_properties.get('protein_binding', ''),
        'route_of_elimination': drug_properties.get('route_of_elimination', ''),
        'volume_of_distribution': drug_properties.get('volume_of_distribution', ''),
        'clearance': drug_properties.get('clearance', ''),
            # Generate embeddings
        'drug_embed_text': preprocess_drug_text(drug_properties.get('description', '')),
        'indication_embed_text': preprocess_drug_text(drug_properties.get('indication', '')),
        'pd_embed_text': preprocess_drug_text(drug_properties.get('pharmacodynamics', '')),
        'moa_embed_text': preprocess_drug_text(drug_properties.get('mechanism_of_action', '')),
        'met_embed_text': preprocess_drug_text(drug_properties.get('metabolism', '')),
        'abs_embed_text': preprocess_drug_text(drug_properties.get('absorption', '')),
        'tox_embed_text': preprocess_drug_text(drug_properties.get('toxicity', '')),
        'hl_embed_text': preprocess_drug_text(drug_properties.get('half_life', '')),
        'prb_embed_text': preprocess_drug_text(drug_properties.get('protein_binding', '')),
        'roe_embed_text': preprocess_drug_text(drug_properties.get('route_of_elimination', '')),
        'vod_embed_text': preprocess_drug_text(drug_properties.get('volume_of_distribution', '')),
        'clr_embed_text': preprocess_drug_text(drug_properties.get('clearance', ''))
    }



    # Execute the query
    result = conn.execute_query(create_nodes_query, drug_attributes)

    # Close the connection
    conn.close()

    return True






# create_drug_and_related_nodes('BIOD00024', drug_properties)
