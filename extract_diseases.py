import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# Only for tensorflow supported python env
# from transformers import TFAutoModelForTokenClassification, BertTokenizer, pipeline

import os
import pandas as pd
import logging

print(torch.__version__)
print(torch.cuda.is_available())


# logging.set_verbosity_info()   # uncomment for verbose and set an integer 20 for info level

class extract_diseases:
    def __init__(self, dataset, model_name, tokenizer_name, pipeline_name):
        self.dataset = dataset
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.pipeline_name = pipeline_name
        self.model_results = None
        if not isinstance(pipeline_name, str):
                raise TypeError(f"'pipeline' should be of type 'str', but got {type(pipeline_name).__name__}")
        
        self.ner_pipeline = pipeline(str(self.pipeline_name), model=self.model_name, tokenizer=self.tokenizer_name)
        
    def run_pipeline(self):
        final_diseases = {}   # dict to store all results from the NER model
        df = self.dataset
        for x in df.index:
            index_num = df['ID'].loc[x]
            text_sentence = df['merged'].loc[x]
            # print(text_sentence)
            
            result = self.ner_pipeline(text_sentence)
            # print(result)
            
            final_diseases.update({x: result})
        self.model_results = final_diseases
        return self.model_results
        
    def extract_name(self):
        disease_names = {}
        for n, m in self.model_results.items():
            diseases = []
            for entity in m:
                if entity["entity"] == "Disease":
                    diseases.append(entity["word"])
                elif entity["entity"] == "Disease Continuation" and diseases:
                    diseases[-1] += f" {entity['word']}"
            # print(f"Diseases: {', '.join(diseases)}")
            disease_names.update({n: ', '.join(diseases)})
        return disease_names

def main():
    try:
        # Load pre-trained BioBERT or other NER model
        tokenizer = AutoTokenizer.from_pretrained("ugaray96/biobert_ncbi_disease_ner")
        model = AutoModelForTokenClassification.from_pretrained(
            "ugaray96/biobert_ncbi_disease_ner"
        )
        
        ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)
        conditions = extract_diseases(incl_data[['ID', 'merged']], model, tokenizer, 'ner')
        diseases_dict = conditions.run_pipeline()
        disease_names = disease_conditions.extract_name()
        pd.Series(disease_names).to_csv(os.path.join(os.getcwd(), 'disease_names.csv'))
        
        # In case of tensorflow:
        # # Load the pre-trained BioBERT or other NER model for TensorFlow
        # tokenizer = BertTokenizer.from_pretrained("ugaray96/biobert_ncbi_disease_ner")
        
        # # Load the model with TensorFlow (avoid using torch)
        # model = TFAutoModelForTokenClassification.from_pretrained("ugaray96/biobert_ncbi_disease_ner")
        
        # # Create the NER pipeline using TensorFlow model
        # ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

    except Exception as e:
        print(f"Error: {e}")


# Check if the script is being run directly
if __name__ == "__main__":
    main()
    

