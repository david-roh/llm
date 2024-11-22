import os
import time
import random
import logging
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from src.main import create_graph_database_connection, extract_graph_from_file_local_file
from src.entities.source_node import sourceNode
import asyncio
from neo4j import GraphDatabase
# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Load environment variables
load_dotenv()

# Test configurations
BATCH_SIZES = [1, 5, 10, 20]
MODELS = ['groq_llama3_70b']  # Can be expanded to test different models
PDF_DIR = 'testdocs/'  # Your test documents directory
MERGED_DIR = os.path.join(os.path.dirname(__file__), "merged_files")

# Set random seed for consistent document selection
random.seed(42)

def setup_test_files(num_files):
    """Setup test files by selecting and copying the specified number of documents"""
    # Get list of all PDF files
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith('.pdf')]
    
    # Consistently select the same files for each batch size
    selected_files = random.sample(pdf_files, num_files)
    
    test_files = []
    for i, filename in enumerate(selected_files):
        src_path = os.path.join(PDF_DIR, filename)
        new_filename = f'test_doc_{i}_{filename}'
        dest_path = os.path.join(MERGED_DIR, new_filename)
        
        if not os.path.exists(dest_path):
            with open(src_path, 'rb') as src:
                with open(dest_path, 'wb') as dst:
                    dst.write(src.read())
        test_files.append((new_filename, dest_path))
    
    return test_files

async def run_ingestion_benchmark():
    """Run the ingestion benchmark across different batch sizes"""
    results = []
    
    # Database connection
    uri = os.getenv('NEO4J_URI', '')
    username = os.getenv('NEO4J_USERNAME', '')
    password = os.getenv('NEO4J_PASSWORD', '')
    database = os.getenv('NEO4J_DATABASE', 'neo4j')
    
    # Create direct Neo4j driver connection instead of Neo4jGraph
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    for model in MODELS:
        for batch_size in BATCH_SIZES:
            logging.info(f"Testing batch size: {batch_size}")
            
            # Setup test files
            test_files = setup_test_files(batch_size)
            
            # Measure ingestion time
            start_time = time.time()
            
            total_nodes = 0
            total_relationships = 0
            
            for filename, filepath in test_files:
                try:
                    logging.info(f"Starting processing of {filename}")
                    
                    # Create source node
                    source_node = sourceNode()
                    source_node.file_name = filename
                    source_node.file_type = 'pdf'
                    source_node.model = model
                    
                    # Verify source node creation
                    logging.info(f"Created source node: {source_node.__dict__}")
                    
                    # Use the driver's session
                    with driver.session(database=database) as session:
                        result = session.run("""
                            MERGE (d:Document {filename: $filename})
                            SET d.status = 'processing'
                            RETURN d
                        """, filename=filename)
                        logging.info(f"Document node creation result: {result.single()}")
                    
                    result = await extract_graph_from_file_local_file(
                        uri, username, password, database,
                        model, filepath, filename, '', '',
                        None
                    )
                    
                    logging.info(f"Result from extraction: {result}")
                    
                    total_nodes += result.get('nodeCount', 0)
                    total_relationships += result.get('relationshipCount', 0)
                    
                except Exception as e:
                    logging.error(f"Error processing file {filename}: {str(e)}")
                    logging.error("Full error details:", exc_info=True)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Record results
            result = {
                'timestamp': datetime.now(),
                'model': model,
                'batch_size': batch_size,
                'total_processing_time': processing_time,
                'avg_time_per_doc': processing_time / batch_size,
                'total_nodes': total_nodes,
                'total_relationships': total_relationships
            }
            results.append(result)
            
            # Clean up test files
            for _, filepath in test_files:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(f'ingestion_benchmark_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', index=False)
    return results

if __name__ == "__main__":
    results = asyncio.run(run_ingestion_benchmark())
    
    # Print summary
    print("\nBenchmark Results:")
    print("================")
    for result in results:
        print(f"\nBatch Size: {result['batch_size']}")
        print(f"Total Processing Time: {result['total_processing_time']:.2f} seconds")
        print(f"Average Time per Document: {result['avg_time_per_doc']:.2f} seconds")
        print(f"Total Nodes Created: {result['total_nodes']}")
        print(f"Total Relationships Created: {result['total_relationships']}")
