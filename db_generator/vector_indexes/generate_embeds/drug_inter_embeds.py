
from db_generator.vector_indexes.generate_embeds.create_embeds import get_clinicalbert_embeddings, get_clinicalbert_embeddings_parallel
from tqdm import tqdm



# def create_interaction_embeddings(session):
#     # This query matches all INTERACTS_WITH relationships that have a non-empty 'embed_text' property
#     # and then returns the relationship along with its ID and 'embed_text'
#     results = session.run( """
#         MATCH (d:Drug)-[r:INTERACTS_WITH]->(i:Drug)
#         WHERE r.embed_text IS NOT NULL AND r.embed_text <> "" AND r.embedding IS NULL
#         RETURN r AS relationship, r.embed_text AS embed_text, ID(r) AS relationshipId
#         """)
    

#     print(len(list(results)))

#     for result in tqdm(results):
#         relationship = result["relationship"]
#         embed_text = result["embed_text"]
#         relationship_id = result["relationshipId"]
        
#         # Generate the embedding for the 'embed_text'
#         vector = get_clinicalbert_embeddings(embed_text)
        
#         # Update the relationship with the generated embedding vector
#         update_query = session.run("""
#         MATCH ()-[r:INTERACTS_WITH]->()
#         WHERE ID(r) = $relationshipId
#         CALL db.create.setRelationshipVectorProperty(r, $property, $vector)
#         RETURN r
#         """, relationshipId=relationship_id, property="embedding", vector=vector)

     

#     print("Updated embeddings for INTERACTS_WITH relationships.")




# def create_interaction_embeddings(session):
#     # Fetch the results eagerly if the dataset is manageable in size.
#     results = session.run("""
#         MATCH (d:Drug)-[r:INTERACTS_WITH]->(i:Drug)
#         WHERE r.embed_text IS NOT NULL AND r.embed_text <> "" AND r.embedding IS NULL
#         RETURN r AS relationship, r.embed_text AS embed_text, ID(r) AS relationshipId
#         """)

#     for result in results:
#         print(result)
#         relationship = result["relationship"]
#         embed_text = result["embed_text"]
#         relationship_id = result["relationshipId"]
        
#         # Generate the embedding for the 'embed_text'
#         vector = get_clinicalbert_embeddings(embed_text)
        
#         # Update the relationship in the database
#         session.run("""
#             MATCH ()-[r:INTERACTS_WITH]->()
#             WHERE ID(r) = $relationshipId
#             CALL db.create.setRelationshipVectorProperty(r, $property, $vector)
#             RETURN r
#             """, relationshipId=relationship_id, property="embedding", vector=vector)

#     # print("Updated embeddings for INTERACTS_WITH relationships.")
        

def create_interaction_embeddings(session):
        relationships = session.run("""
                                    MATCH (d:Drug)-[r:INTERACTS_WITH]->(i:Drug)
                                    WHERE r.embed_text IS NOT NULL AND r.embed_text <> "" AND r.embedding IS NULL
                                    RETURN r AS relationship, r.embed_text AS embed_text, ID(r) AS relationshipId
                                    """)
                                    
        updates = []
        batch_size = 1000

        
        for rel in relationships:
            embed_text = rel["embed_text"]
            relationship_id = rel["relationshipId"]
            embedding = get_clinicalbert_embeddings(embed_text)
            updates.append({"id": relationship_id, "embed_text": embed_text, "embedding": embedding})
            
            # Update in batches
            if len(updates) >= batch_size:
                # embedding = get_clinicalbert_embeddings(embed_text)
                # updatd_embeds = get_clinicalbert_embeddings_parallel(updates,2)
                # updated_count = update_embeddings(updatd_embeds,session)

                updated_count = update_embeddings(updates,session)

                print(f"Updated {updated_count} embeddings.")
                updates = []

        # Update any remaining items
        if updates:
            # updatd_embeds = get_clinicalbert_embeddings_parallel(updates,2)
            # updated_count = update_embeddings(updatd_embeds,session)
            updated_count = update_embeddings(updates,session)
            print(f"Updated {updated_count} embeddings.")


def update_embeddings(updates, session):
    query = """
    UNWIND $updates AS update
    MATCH ()-[r:INTERACTS_WITH]->() WHERE ID(r) = update.id
    CALL db.create.setRelationshipVectorProperty(r, 'embedding', update.embedding)
    RETURN count(r) as updatedCount
    """
    result = session.run(query, updates=updates)
    return result.single()["updatedCount"]