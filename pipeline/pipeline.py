import process_training
import grobid
import correction


def pipeline():
    # Retrieve training documents
    process_training.process_training()
    # Create training set
    grobid_core = grobid.GrobidCore('...')
    grobid_core.createTraining('...')
    # Validate training set
    correction.correction()
    # Train model
    grobid_trainer = grobid.GrobidTrainer()
    grobid_trainer.TrainRunner()

if __name__ == "__main__":
    pipeline()
