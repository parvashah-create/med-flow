
from dotenv import load_dotenv
import os
# Langchain
from neo4j import GraphDatabase
from langchain.graphs.neo4j_graph import Neo4jGraph
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain_openai import OpenAIEmbeddings
# from langchain.chains.retrieval import RetrievalQAWithSourcesChain
from langchain_openai import ChatOpenAI



# from db_generator.vector_indexes.generate_embeds.drug_embeds import test_vector_query, create_drug_related_embeddings, create_drug_openai_embeds, create_ddi_embedding
from db_generator.vector_indexes.generate_embeds.drug_embeds import create_ddi_embedding, test_ddi_vector_query

# from db_generator.vector_indexes.generate_embeds.price_embeds import create_price_embeddings
# from db_generator.vector_indexes.generate_embeds.sub_info_embeds import create_sub_info_embeddings
# from db_generator.vector_indexes.generate_embeds.drug_inter_embeds import create_interaction_embeddings



load_dotenv()


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")



OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = os.getenv('OPENAI_BASE_URL') + '/embeddings'




# kg = Neo4jGraph(
#     url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
# )



# with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:


    # driver.verify_connectivity()

    # print(driver.execute_query("SHOW INDEXES"))

    # create_drug_indexes(kg)



related_node_types = [
        {"label": "Drug", "property": "drug_text_embedding"},
        {"label": "Indication", "property": "indication_text_embedding"},
        {"label": "Pharmacodynamics", "property": "pd_text_embedding"},
        {"label": "MechanismOfAction", "property": "moa_text_embedding"},
        {"label": "Metabolism", "property": "met_text_embedding"},
        {"label": "Absorption", "property": "abs_text_embedding"},
        {"label": "Toxicity", "property": "tox_text_embedding"},
        {"label": "HalfLife", "property": "hl_text_embedding"},
        {"label": "ProteinBinding", "property": "prb_text_embedding"},
        {"label": "RouteOfElimination", "property": "roe_text_embedding"},
        {"label": "VolumeOfDistribution", "property": "vod_text_embedding"},
        {"label": "Clearance", "property": "clr_text_embedding"}
    ]

related_node_types = [
        {"label": "Drug", "property": "drug_text_embedding"},
    ]
def create_node_indexes(session):


    for label in related_node_types:

        node_index = label["label"] + "_embedding_index"
        print(node_index)

        query = """
            CREATE VECTOR INDEX {node_index} IF NOT EXISTS
            FOR (n:{node_label}) ON (n.embedding)
            OPTIONS {index_config}
            """.format(node_index=node_index, node_label=label["label"], index_config="{indexConfig:{`vector.dimensions`: 768,`vector.similarity_function`: 'cosine'}}")
        
        print(query)
        session.run(query)
            
    
    print("Complete")


def create_openai_indexes(session):


    query = """
        CREATE VECTOR INDEX {node_index} IF NOT EXISTS
        FOR (n:{node_label}) ON (n.openai_embedding)
        OPTIONS {index_config}
        """.format(node_index="openai_embedding_index", node_label="Drug", index_config="{indexConfig:{`vector.dimensions`: 1536,`vector.similarity_function`: 'cosine'}}")
    
    print(query)
    session.run(query)
    print("Complete")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
session = driver.session()



# create_node_indexes(session)
# create_drug_related_embeddings(session)


# create_price_embeddings(session)
# create_sub_info_embeddings(session)
# create_interaction_embeddings(session)

# create_drug_openai_embeds(session)

# create_openai_indexes(session)
create_ddi_embedding(session)

# test_ddi_vector_query(session,"Etanercept and Nicotine",5)

# test_vector_query(session,"Drug Interaction",3)



# """
# CREATE VECTOR INDEX ddi_index IF NOT EXISTS
# FOR (n:`drugbank_vocabulary:Drug-Drug-Interaction`) ON (n.ddi_embedding)
# OPTIONS {indexConfig:{`vector.dimensions`: 1536,`vector.similarity_function`: 'cosine'}}
# """


# """
# MATCH (n:`drugbank_vocabulary:Drug-Drug-Interaction`)
# WHERE size(n.title) <> 0 AND n.embedding IS NULL
# WITH collect(n) AS nodes, count(*) AS total, 1000 AS batchSize
# UNWIND range(0, total, batchSize) AS batchStart
# CALL {
#     WITH nodes, batchStart, batchSize
#     WITH nodes, batchStart, [node IN nodes[batchStart .. batchStart + batchSize] | apoc.text.join(node.title, " ")] AS batchTexts
#     CALL genai.vector.encodeBatch(batchTexts, "OpenAI", { token: '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' }) YIELD index, vector
#     CALL db.create.setNodeVectorProperty(nodes[batchStart + index], "embedding", vector)
# } IN TRANSACTIONS OF 1 ROW
# RETURN count(*)
# """

# """
# :auto
# MATCH (n:`drugbank_vocabulary:Drug-Drug-Interaction`)
# WHERE size(n.title) <> 0 AND n.ddi_embedding IS NULL
# WITH collect(n) AS nodes,
#      count(*) AS total,
#      1000 AS batchSize
# UNWIND range(0, total, batchSize) AS batchStart
# CALL {
#     WITH nodes, batchStart, batchSize
#     WITH nodes, batchStart, [node IN nodes[batchStart .. batchStart + batchSize] | node.title] AS batch
#     CALL genai.vector.encodeBatch(batch, "OpenAI", { token:'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',model:"text-embedding-3-small" }) YIELD index, vector
#     CALL db.create.setNodeVectorProperty(nodes[batchStart + index], "ddi_embedding", vector)
# } IN TRANSACTIONS OF 1 ROW

# """

# """
# CALL n10s.graphconfig.init({handleVocabUris:"IGNORE",handleMultival:"OVERWRITE"});
# CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
# CALL n10s.rdf.import.fetch("file:///Users/parvashah/Documents/bio2rdf/data/rdf/drugbank.nq","N-Quads",{verifyUriSyntax:false});
# """

# """
# CALL n10s.graphconfig.init({handleMultival:"OVERWRITE"});

# """