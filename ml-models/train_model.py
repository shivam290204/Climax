# [NEW FILE]: ml-models/train_model.py
"""Main training script that runs data pipeline first, then trains model."""
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from fetch_data import run_data_pipeline
    from train_random_forest import train
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required files are in the ml-models directory")
    sys.exit(1)

def main():
    """Run complete ML pipeline: data fetch -> training."""
    print("Starting ML Pipeline...")
    
    # Step 1: Fetch data
    print("\n=== Step 1: Running Data Pipeline ===")
    try:
        run_data_pipeline()
    except Exception as e:
        print(f"Error in data pipeline: {e}")
        print("Trying to train with existing data...")
    
    # Step 2: Train model
    print("\n=== Step 2: Training Model ===")
    try:
        model, metrics = train(save=True, do_cv=True)
        print("Model training completed successfully!")
        print(f"Final R² Score: {metrics.get('r2', 'N/A'):.3f}")
    except Exception as e:
        print(f"Error in model training: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()