import re
import os
import pandas as pd
import json

class clindata_parser:
    def __init__(self, data_struct, schema, comb_studies, field_dict = None):
        self.data_struct = data_struct
        self.comb_studies = comb_studies
        self.target_schema = schema
        self.relevant_fields_df = None
        
        # Use the provided field_dict or set a default empty dictionary
        self.field_dict = field_dict if field_dict is not None else {}
        
        self.super_dict = None
        
        
    def xpath(self, a: str) -> str:
        '''function to modify XPath strings.'''
        if '/' in a:
            b = a.replace('/', '.')
            if 'Study' in b:
                return b.replace('.Study.', '')
        else:
            return a

    def map_datastruct(self):
        relevant_fields = {}        # relevant fields that look like keys in example schema 
        for field in self.target_schema.keys():
        #     print(field)
            if field == 'trialId':
                print(field)
                field_original = field
                field = 'id'
                result = [y for y in self.data_struct['Piece Name'] if re.search(f"{field}", str(y), re.IGNORECASE)]
                print(result)
        #         print(self.data_struct[self.data_struct['Piece Name'].isin(result)][['Piece Name', 'Classic XPath']])
                relevant_fields.update({field_original: self.data_struct[self.data_struct['Piece Name'].isin(result)][['Piece Name', 'Classic XPath']]})

            elif field == 'endDate':
                print(field)
                field_original = field
                field = 'CompletionDate'
                result = [y for y in self.data_struct['Piece Name'] if re.search(f"{field}", str(y), re.IGNORECASE)]
                print(result)
                relevant_fields.update({field_original: self.data_struct[self.data_struct['Piece Name'].isin(result)][['Piece Name', 'Classic XPath']]})

            elif field == 'principalInvestigator':
                print(field)
                field_original = field
                field = 'Investigator'
                result = [y for y in self.data_struct['Piece Name'] if re.search(f"{field}", str(y), re.IGNORECASE)]
                print(result)
                relevant_fields.update({field_original: self.data_struct[self.data_struct['Piece Name'].isin(result)][['Piece Name', 'Classic XPath']]})
    
    
            else:
                print(field)
                result = [y for y in self.data_struct['Piece Name'] if re.search(f"{field}", str(y), re.IGNORECASE)]
                print(result)
                relevant_fields.update({field: self.data_struct[self.data_struct['Piece Name'].isin(result)][['Piece Name', 'Classic XPath']]})
            print()
    
        relevant_fields_df = pd.concat(relevant_fields.values())
        self.relevant_fields_df = relevant_fields_df
        #     relevant_fields_df[relevant_fields_df['Piece Name'] == 'completionDateStruct']
        return self.relevant_fields_df


    def flatten_json(self, y, parent_key='', sep='.'):
        """
        Flattens a nested JSON object into a single level.
        Keys will be in the form 'parent.child.grandchild'.
        """
        items = []
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                # Recursive call with self.flatten_json
                items.extend(self.flatten_json(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    # Handle lists properly
                    items.extend(self.flatten_json({f"{k}[{i}]": item}, parent_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    
    def map_schema(self):
        super_dict = {}
        for n, x in enumerate(self.comb_studies):
        #     print(n)
            mapped_data = {}
            flat_json_1 = flatten_json(self.comb_studies[n])
        #     print(flat_json_1.keys())
            for item in self.field_dict:
                i = self.field_dict[item]
        #         print(item, i, '__________________')

                if isinstance(i, list):
        #             print(i)
                    try:
                        investigater = {}
                        for f in i:
                            col_a = self.xpath(self.relevant_fields_df[self.relevant_fields_df['Piece Name'] == f]['Classic XPath'].values[0])
        #                     print(col_a)
                            try:
                                investigater.update({f: flat_json_1[col_a]})
                            except:
                                pass
                        mapped_data.update({item : investigater})
                    except:
                        pass

                else:
                    if item == 'locations':
                        col_a = self.xpath(self.relevant_fields_df[self.relevant_fields_df['Piece Name'] == i]['Classic XPath'].values[0])
        #                 print(col_a)

                        try:
                            location = [a for a in flat_json_1.keys() if a.startswith(str(col_a))]
                            if len(location) == 1:
                                mapped_data.update({item : flat_json_1[col_a]})
                            else:
                #             print(location)
                                location_data = pd.Series({v: flat_json_1[v] for v in location})
                    #             print(location_data)
                                location_df = pd.DataFrame([range(1, len(location_data.index)+1), location_data, location_data.index]).T

                                location_df['keyid'] = [re.findall(r'\d+', string)[0] for string in location_df[2]]
                                location_df['subfield'] = [string.split('].')[1] for string in location_df[2]]
                                loc = {}
                    #             print(location_df)
                                for num, (g, h) in enumerate(location_df.groupby(by='keyid')):
                                    loc.update({num: {key: val for key, val in zip(h['subfield'], h[1])}})
                #                     print()
            #                     print(loc)
                                mapped_data.update({item : loc})
                        except:
                            pass

                    elif item == 'startDate':
                        col_a = self.xpath(self.relevant_fields_df[self.relevant_fields_df['Piece Name'] == self.field_dict[item]]['Classic XPath'].values[0])
                        try:
                            sdate = [a for a in flat_json_1.keys() if a.startswith(str(col_a))][0]
                            mapped_data.update({item : flat_json_1[sdate]})
        #                     print(sdate)
                        except:
                            pass
        #                 
                    elif item == 'endDate':
                        col_a = self.xpath(self.relevant_fields_df[self.relevant_fields_df['Piece Name'] == self.field_dict[item]]['Classic XPath'].values[0])
                        try:
                            edate = [a for a in flat_json_1.keys() if a.startswith(str(col_a))][0]
                            mapped_data.update({item : flat_json_1[edate]})
        #                     print(edate)
                        except:
                            pass

                    else:
        #                 print(i)
                        try:
                            col_a = self.xpath(self.relevant_fields_df[self.relevant_fields_df['Piece Name'] == self.field_dict[item]]['Classic XPath'].values[0])
        #                     print(col_a, '***')
        #                     print()
                            mapped_data.update({item : flat_json_1[col_a]})
                        except:
                            pass

            super_dict.update({n : mapped_data})
      
        self.super_dict = super_dict
        return self.super_dict
    
    # Function to clean text in criteria
    def clean_criteria(self, section):
        # Remove bullet points (e.g., '* ', '1. ', etc.), colons, and split into lines
        lines = re.split(r'\n+', section)
        cleaned_lines = [re.sub(r'^[\*\d\.\s]+|[:]', '', line).strip() for line in lines]
        # Filter out empty strings
        return [line for line in cleaned_lines if line]
    
    
    def inclusion_criteria(self):
        processed_data = {}
        
        # Initialize an empty list to collect error messages
        error_log = []
        
        for i, j in list(self.super_dict.items()):
        #     print(i, j.keys())
        #     print(j['eligibilityCriteria'])
            try:
                criteria_text = j['eligibilityCriteria']
        #         print(criteria_text)
                # Splitting the text into inclusion and exclusion sections
                sections = criteria_text.split("Exclusion Criteria:")
                inclusion_section = [y.split("Inclusion Criteria")[1].strip('\n') for y in [x for x in sections if x.startswith("Inclusion Criteria")]]
#                 print(inclusion_section)
                inclusion_criteria = self.clean_criteria("\n".join(inclusion_section))
#                 print(inclusion_criteria)
                processed_data.update({i: inclusion_criteria})
            except Exception as e:
                error_log.append(f"Error encountered with value i={i}: {e}")
                pass

        # Write all collected errors to a log file at the end of the loop
        if error_log:
            with open("error_log.txt", "w") as log_file:
                log_file.write("\n".join(error_log))
            print("Errors have been logged to 'error_log.txt'.")
        else:
            print("No errors encountered during the loop.")
            
            # Convert dictionary to DataFrame
        df = pd.DataFrame.from_dict(processed_data, orient="index").reset_index()
        df.columns = ["ID"] + [f"Sentence_{i}" for i in range(1, len(df.columns))]

        # df.columns = ["ID", "Sentence"]

        df['merged'] = df[df.columns[1:]].apply(lambda row: ' '.join([str(val) for val in row if val not in [None, '']]), axis=1)

        print(df)
        return df
    
def main():   
   try:
        ## Manually written dict based on the keywords found from searching keys from example schema, required as the field names are different. This can be customized.
        field_list = {'trialId':'nctId', 'title':'officialTitle', 'startDate':'startDateStruct', 'endDate':'completionDateStruct', 'phase':'Phase', 'principalInvestigator':['investigatorFullName',  'investigatorAffiliation'], 'locations':'locations\xa0⤷', 'eligibilityCriteria':'eligibilityCriteria'}
        
        
        data_structure = pd.read_csv(os.getcwd()+'/datastruct/Protocolsection.csv', header=0, skiprows=1)
        print(data_structure)
        
        # f.close()
        data_path = os.path.join(os.getcwd(), 'rawdata')
        with open(os.path.join(data_path, "all_studies.json")) as f:
            combined_studies = json.load(f)
        #     print(combined_studies)
        print('total number of studies', len(combined_studies))
    
        
        field_list = {'trialId':'nctId', 'title':'officialTitle', 'startDate':'startDateStruct', 'endDate':'completionDateStruct', 'phase':'Phase', 'principalInvestigator':['investigatorFullName',  'investigatorAffiliation'], 'locations':'locations\xa0⤷', 'eligibilityCriteria':'eligibilityCriteria'}
        example_schema = {
         "trialId": "NCT00560521",
         "title": "Effect of Continuous Positive Airway Pressure on Fluid Absorption Among Patients With Pleural Effusion Due to Tuberculosis",
         "startDate": "2005-03-01",
         "endDate": "2007-03-01",
         "phase": "Other",
         "principalInvestigator": {
         "name": "Juliana F Oliveira",
         "affiliation": "Universidade Federal do Rio de Janeiro"
         },
         "locations": [
         {
         "facility": "Federal University of Rio de Janeiro",
         "city": "Rio de Janeiro",
         "country": "Brazil"
         }
         ],
         "eligibilityCriteria": "Inclusion Criteria:\n\nConfirmed diagnosis of pleural tuberculosis.\nPatients 18 years of age and older.\n\nExclusion criteria:\n\nBe under previous treatment of respirat ory physiotherapy.\nIrregular use or abandonment of the anti-TB standard regimen.\nTo fail one or more physiotherapy section.\nTo fail one or more radiological evaluation."
        }
        
        parse = clindata_parser(data_structure, example_schema, combined_studies, field_dict=field_list)
        r_fields = parse.map_datastruct()
        super_dict = parse.map_schema()
        incl_data = parse.inclusion_criteria()
        incl_data.to_csv(os.path.join(os.getcwd(), 'inclusion_criteria_dict.csv'))
    except Exception as e:
        print(f"Error: {e}")


# Check if the script is being run directly
if __name__ == "__main__":
    main()



    

    

