
from db_generator.vector_indexes.generate_embeds.create_embeds import get_clinicalbert_embeddings


def create_sub_info_embeddings(session):

    related_node_types = [
        {"label": "FoodInteraction", "property": "drug_text_embedding"},
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
                
    print("Updated embeddings for food interaction nodes.")

