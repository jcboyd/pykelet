import grobid
import correction

def pipeline():
        # Create training set
            grobid_core = grobid.GrobidCore('...')
                grobid_core.createTraining('...')
                    # Validate training set
                        correction.correction()
                            # Train model
                                grobid_trainer = grobid.GrobidTrainer(...)
                                    grobid_trainer.TrainRunner()
