from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()


# Connect to the local Neo4j instance
uri = os.getenv("NEO4J_URI") # Default URI for Neo4j
user = os.getenv("NEO4J_USER")            # Default user for Neo4j
password = os.getenv("NEO4J_PASSWORD")    # Replace 'your_password' with your actual Neo4j password

# Create a class to handle the database connection and operations
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.__uri = uri
        self.__user = user
        self.__password = password
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        except Exception as e:
            print(f"Failed to create the driver: {e}")

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def execute_query(self, query, parameters=None):
        with self.__driver.session() as session:
            result = session.execute_write(self.__execute_transaction, query, parameters)
            return result

    @staticmethod
    def __execute_transaction(tx, query, parameters):
        result = tx.run(query, parameters)
        return [record for record in result]




# # Create an instance of the Neo4jConnection class
# conn = Neo4jConnection(uri, user, password)

# # Test the connection and the environment by creating a simple node
# test_query = "CREATE (n:Test {message: 'Hello, World!'}) RETURN n.message AS message"
# result = conn.execute_query(test_query)
# print(result)  # Should print "Hello, World!"

# # Don't forget to close the connection when you're done
# conn.close()
