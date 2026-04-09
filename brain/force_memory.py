#!/usr/bin/env python3
"""
Force Memory Creation for AOS Brain
Directly injects memories to bootstrap the system
"""

import sys
import json
import time
sys.path.insert(0, '/root/.aos/aos/brain')

def force_memory_creation():
    """Force create memories in ChromaDB"""
    print("=" * 60)
    print("FORCE MEMORY CREATION")
    print("=" * 60)
    
    # Try to import and use ChromaDB directly
    try:
        import chromadb
        print("✅ ChromaDB imported")
        
        db_path = "/root/.aos/memory/vector"
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection(name="qmd_memory")
        
        current_count = collection.count()
        print(f"Current memory count: {current_count}")
        
        if current_count == 0:
            print("\n🔄 Injecting seed memories...")
            
            # Create seed memories
            seed_memories = [
                {
                    "id": "bootstrap_1",
                    "text": "AOS Brain is an autonomous cognitive system using OODA loops for decision making",
                    "metadata": {"timestamp": time.time(), "source": "bootstrap", "novelty": 0.9}
                },
                {
                    "id": "bootstrap_2", 
                    "text": "Seven regions process information: Thalamus routes, Brainstem monitors, PFC reasons, Hippocampus remembers",
                    "metadata": {"timestamp": time.time(), "source": "bootstrap", "novelty": 0.85}
                },
                {
                    "id": "bootstrap_3",
                    "text": "QMD compresses episodic memories into semantic representations using vector embeddings",
                    "metadata": {"timestamp": time.time(), "source": "bootstrap", "novelty": 0.8}
                },
                {
                    "id": "bootstrap_4",
                    "text": "GrowingNN dynamically expands network capacity based on novelty signals and prediction errors",
                    "metadata": {"timestamp": time.time(), "source": "bootstrap", "novelty": 0.9}
                },
                {
                    "id": "bootstrap_5",
                    "text": "Three consciousness layers: Conscious (PFC), Subconscious (Hippocampus), Unconscious (Limbic/Basal)",
                    "metadata": {"timestamp": time.time(), "source": "bootstrap", "novelty": 0.85}
                },
            ]
            
            for memory in seed_memories:
                collection.add(
                    documents=[memory["text"]],
                    metadatas=[memory["metadata"]],
                    ids=[memory["id"]]
                )
                print(f"  ✅ Added: {memory['id']}")
            
            new_count = collection.count()
            print(f"\n✅ Total memories: {new_count}")
            
            # Test query
            print("\n🧪 Testing query...")
            results = collection.query(
                query_texts=["neural networks"],
                n_results=2
            )
            print(f"  Found {len(results['documents'][0])} matches")
            
            return new_count
        else:
            print("✅ Memories already exist")
            return current_count
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 0

def update_brain_state():
    """Update brain state to reflect memories"""
    print("\n" + "=" * 60)
    print("UPDATING BRAIN STATE")
    print("=" * 60)
    
    state_path = "/root/.aos/brain/state/brain_state.json"
    
    try:
        with open(state_path, 'r') as f:
            state = json.load(f)
        
        # Update memory count
        state["memory_nn"]["clusters"] = 5
        state["memory_nn"]["novelty_current"] = 0.8
        state["memory_nn"]["novelty_avg"] = 0.75
        state["limbic"]["novelty"] = 0.8
        state["tick"] = state.get("tick", 0) + 1
        
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
        
        print("✅ Brain state updated")
        print(f"   Clusters: {state['memory_nn']['clusters']}")
        print(f"   Novelty: {state['limbic']['novelty']}")
        print(f"   Tick: {state['tick']}")
        
    except Exception as e:
        print(f"❌ State update failed: {e}")

if __name__ == "__main__":
    count = force_memory_creation()
    if count > 0:
        update_brain_state()
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
