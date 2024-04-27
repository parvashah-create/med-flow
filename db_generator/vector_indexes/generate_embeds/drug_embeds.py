
# from db_generator.vector_indexes.generate_embeds.create_embeds import get_clinicalbert_embeddings
from dotenv import load_dotenv
from tqdm import tqdm
import os
from openai import OpenAI
import re
import concurrent.futures
import json
load_dotenv()

# def create_drug_indexes(driver):

#     # Retrieve drugs and their embed_text
#     drugs_with_text = driver.run("""
#         MATCH (d:Drug)
#         WHERE d.embed_text IS NOT NULL AND d.embed_text <> ""
#         RETURN d AS drug, d.embed_text AS embed_text, ID(d) AS drugId
#     """)
    
    
#     for drug_data in drugs_with_text:
#         drug = drug_data['drug']
#         embed_text = drug_data['embed_text']
#         drug_id = drug_data['drugId']


#         print("Drug --------->",drug)
#         print("embed_text --------->",embed_text)
#         print("drug_id --------->",drug_id)

#         # Generate embedding for each drug's embed_text
#         vector = get_clinicalbert_embeddings(embed_text)

    

#         driver.run("""
#                 MATCH (d:Drug)
#                 WHERE ID(d) = $drugId
#                 CALL db.create.setNodeVectorProperty(d, 'embedding', $vector)
#                 RETURN d
#             """, drugId=drug_id, vector=vector)


#     driver.run("""
#         CREATE VECTOR INDEX drug_embedding IF NOT EXISTS
#         FOR (d:Drug) ON (d.drug_text_embedding) 
#         OPTIONS { indexConfig: {
#             `vector.dimensions`: 768,
#             `vector.similarity_function`: 'cosine'    
#         }}
#     """)
#     print("Complete")
        


        
def create_drug_related_embeddings(session):

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
    for node_type in related_node_types:
        results = session.run(f"""
            MATCH (n:{node_type["label"]})
            WHERE n.embed_text IS NOT NULL AND n.embed_text <> ""
            RETURN n AS node, n.embed_text AS embed_text, ID(n) AS nodeId
        """)
        
        for result in results:
            node = result['node']
            embed_text = result['embed_text']
            node_id = result['nodeId']
            
            # Assuming get_clinicalbert_embeddings is a function that generates the embedding
            vector = get_clinicalbert_embeddings(embed_text)
            
            session.run(f"""
                    MATCH (n:{node_type["label"]})
                    WHERE ID(n) = $nodeId
                    CALL db.create.setNodeVectorProperty(n, $property, $vector)
                    RETURN n
                """, nodeId=node_id, property="embedding", vector=vector)
                
    print("Updated embeddings for related nodes.")




def test_vector_query(session, sample_text, top_k):
    # Generate an embedding for the sample text
    query_vector = get_clinicalbert_embeddings(sample_text)
    
    
    query_results = session.run("""
        CALL db.index.vector.queryNodes("Absorption_embedding_index", $top_k, $embedding) 
        YIELD node, score
        RETURN node, score
        """, top_k=top_k, embedding=query_vector)
    

    # Print the results
    print("Nearest Drugs Based on Text Similarity:")
    for drug in query_results:
        # print(drug['node'])
        print(drug['node']['embed_text'])
        print(f"Drug: {drug['node']['embed_text']} - Score: {drug['score']}")


def test_ddi_vector_query(session, sample_text, top_k):
    # Generate an embedding for the sample text
    client = OpenAI()
    response = client.embeddings.create(
            input=sample_text,
            model="text-embedding-3-small"  
        )

    embedding = response.data[0].embedding
    
    query_results = session.run("""
        CALL db.index.vector.queryNodes("ddi_index", $top_k, $embedding) 
        YIELD node, score
        RETURN node, score
        """, top_k=top_k, embedding=embedding)
    

    # Print the results
    print("Nearest Drugs Based on Text Similarity:")
    for drug in query_results:
        # print(drug['node'])
        print(f"Drug: {drug['node']['title']} - Score: {drug['score']}")




def create_drug_openai_embeds(session):
    results = session.run("""
                            MATCH (d:Drug)
                            WHERE size(d.embed_text) <> 0 AND d.openai_embedding IS NULL
                            WITH collect(d) AS nodes,
                                count(*) AS total,
                                1000 AS batchSize
                            UNWIND range(0, total, batchSize) AS batchStart
                            CALL {
                                WITH nodes, batchStart, batchSize
                                WITH nodes, batchStart, [drug IN nodes[batchStart .. batchStart + batchSize] | drug.embed_text] AS batch
                                CALL genai.vector.encodeBatch(batch, "OpenAI", { token: $token }) YIELD index, vector
                                CALL db.create.setNodeVectorProperty(nodes[batchStart + index], "openai_embedding", vector)
                            } IN TRANSACTIONS OF 1 ROW
                            """, token=os.getenv("OPENAI_API_KEY"))
    

    print(results)


def create_ddi_embedding(session):
    client = OpenAI()
    ddi_nodes = session.run("""
                            MATCH (n:`drugbank_vocabulary:Drug-Drug-Interaction`)
                            WHERE apoc.meta.cypher.type(n.title) = 'STRING' AND size(n.title) <> 0 AND n.ddi_embedding IS NULL AND ID(n) = 353075
                            RETURN n
                            """) 

    nodes_list = list(ddi_nodes)
    batch_size = 10000

    for i in tqdm(range(0, len(nodes_list), batch_size)):
        batch = nodes_list[i:i + batch_size]

       

        for record in tqdm(batch):
            node = record["n"]
            text = node["title"]

            # Clean the text
            clean_text = re.sub(r'[^a-zA-Z0-9\s,.]', '', text)

            

            response = client.embeddings.create(
                input=clean_text,
                model="text-embedding-3-small"  
            )

            embedding = response.data[0].embedding

            update_query = """
                        MATCH (n:`drugbank_vocabulary:Drug-Drug-Interaction`)
                        WHERE ID(n) = $element_id
                        SET n.ddi_embedding = $embedding
                        """
            session.run(update_query, element_id=node.id, embedding=embedding)

           

    
    print("The embedding have been updated!")


# def process_batch(batch, client):
#     results = []
#     for record in batch:
#         node = record["n"]
#         text = node["title"]
#         clean_text = re.sub(r'[^a-zA-Z0-9\s,.]', '', text)
#         try:
#             response = client.embeddings.create(
#                 input=clean_text,
#                 model="text-embedding-3-small"
#             )
#             embedding = response.data[0].embedding
#             results.append({"id": node.id, "embedding": embedding})
#         except Exception as e:
#             print(f"Failed to process node {node.id} due to an error: {e}")
#     return results

# def create_ddi_embedding(session):
#     client = OpenAI()
#     ddi_nodes = session.run("""
#                             MATCH (n:`drugbank_vocabulary:Drug-Drug-Interaction`)
#                             WHERE apoc.meta.cypher.type(n.title) = 'STRING' AND size(n.title) <> 0 AND n.ddi_embedding IS NULL
#                             RETURN n
#                             """)
#     nodes_list = list(ddi_nodes)
#     batch_size = 10000
#     total_batches = [nodes_list[i:i + batch_size] for i in range(0, len(nodes_list), batch_size)]

#     with open("ddi_embeddings.json", "w") as json_file:
#         json_file.write('[')  # Start JSON array
#         first_record = True
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             results = list(tqdm(executor.map(lambda batch: process_batch(batch, client), total_batches), total=len(total_batches)))

#         for batch_results in results:
#             for data in batch_results:
#                 if not first_record:
#                     json_file.write(',')
#                 json_file.write(json.dumps(data))
#                 first_record = False

#         json_file.write(']')  # End JSON array

#     print("The embedding has been updated and stored in 'ddi_embeddings.json'!")
