
# from dotenv import load_dotenv
# import os
# # Langchain
# from langchain_community.graphs.neo4j_graph import Neo4jGraph
# from langchain_community.vectorstores.neo4j_vector import Neo4jVector
# from langchain_openai import OpenAIEmbeddings
# # from langchain.chains.retrieval import RetrievalQAWithSourcesChain
# from langchain_openai import ChatOpenAI


# from db_generator.vector_indexes.node_indexes.drug_index import create_drug_indexes
# load_dotenv()


# NEO4J_URI = os.getenv("NEO4J_URI")
# NEO4J_USERNAME = os.getenv("NEO4J_USER")
# NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")



# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# OPENAI_ENDPOINT = os.getenv('OPENAI_BASE_URL') + '/embeddings'




# kg = Neo4jGraph(
#     url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
# )



# kg.query("""
#             CREATE VECTOR INDEX `drug_text_embedding` IF NOT EXISTS
#             FOR (d:Drug) ON (d.embed_text) 
#             OPTIONS { indexConfig: {
#             `vector.dimensions`: 1536,
#             `vector.similarity_function`: 'cosine'    
#             }}
         
#         """)



# create_drug_indexes(kg,OPENAI_API_KEY,OPENAI_API_KEY)