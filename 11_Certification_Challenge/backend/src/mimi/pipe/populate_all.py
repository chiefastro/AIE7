#!/usr/bin/env python3
"""
Script to populate vector database for all chunker types.
"""

import sys
import os
import traceback
from pathlib import Path

# Add the parent directory to the path so we can import mimi modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mimi.config.variants import ChunkerType, AgentType, RetrieverType, ExperimentConfig, variants
from mimi.pipe.pipe import pipe

def populate_for_chunker(chunker_type: ChunkerType):
    """Populate vector database for a specific chunker type"""
    print(f"\n🔄 Populating for chunker: {chunker_type.value}")
    print("=" * 50)
    
    # Create a config with the chunker type and default values for other fields
    config = ExperimentConfig(
        agent_type=AgentType.SUPERVISOR,  # Default value
        chunker_type=chunker_type,
        retriever_type=RetrieverType.COSINE  # Default value
    )
    
    # Initialize the global config
    print(f"Initializing config with: {config.to_dict()}")
    variants.initialize(config)
    
    try:
        # Verify config is initialized
        current_config = variants.get_config()
        print(f"Config initialized successfully: {current_config.to_dict()}")
        
        # Run the pipe function
        docs_path = Path("./data")
        result = pipe(docs_path)
        if result:
            print(f"✅ Successfully populated for {chunker_type.value}")
        else:
            print(f"⚠️  No vectorstore created for {chunker_type.value}")
    except Exception as e:
        print(f"❌ Failed to populate for {chunker_type.value}: {e}")
        print("Full traceback:")
        traceback.print_exc()
        raise
    finally:
        # Reset for next iteration
        print(f"Resetting config for {chunker_type.value}")
        variants.reset()

def main():
    """Populate vector database for all chunker types"""
    print("🚀 Starting population for all chunker types...")
    
    # Get all chunker types
    chunker_types = list(ChunkerType)
    print(f"Found {len(chunker_types)} chunker types: {[ct.value for ct in chunker_types]}")
    
    # Populate for each chunker type
    for chunker_type in chunker_types:
        try:
            populate_for_chunker(chunker_type)
        except Exception as e:
            print(f"❌ Failed to populate for {chunker_type.value}: {e}")
            print("Full traceback:")
            traceback.print_exc()
            # Continue with next chunker type instead of stopping
            continue
    
    print("\n🎉 Population completed for all chunker types!")

if __name__ == "__main__":
    main() 