

def create_drug_indexes(kg,OPENAI_API_KEY,OPENAI_ENDPOINT):

    kg.query("""
                CREATE VECTOR INDEX `drug_text_embedding` IF NOT EXISTS
                FOR (d:Drug) ON (d.embed_text) 
                OPTIONS { indexConfig: {
                `vector.dimensions`: 1536,
                `vector.similarity_function`: 'cosine'    
                }}
            
            """)
    

    kg.query("""
    
        MATCH (d:Drug) WHERE d.embed_text IS NULL
        WITH d, genai.vector.encode(
        d.embed_text, 
        "OpenAI", 
        {
            token: $openAiApiKey, 
            endpoint: $openAiEndpoint
        }) AS vector
        CALL db.create.setNodeVectorProperty(d, "embed_text", vector)
        RETURN d
        """, 
        params={"openAiApiKey":OPENAI_API_KEY, "openAiEndpoint": OPENAI_ENDPOINT} )
    


