import pandas as pd
from collections import Counter
from rake_nltk import Rake


class Geo_Name_Dictionary:
    def __init__(self, dictionary_file):
        self.dictionary_file = pd.read_excel(dictionary_file)
        self.dictionary = pd.DataFrame()


    def build_dictionary(self):
        def keyword(text):
            get_key = Rake()  # Uses stopwords for english from NLTK, and all puntuation characters.
            # r = Rake(<language>) # To use it in a specific language supported by nltk.
            # If you want to provide your own set of stop words and punctuations to
            # r = Rake(<list of stopwords>, <string of puntuations to ignore>)
            get_key.extract_keywords_from_text(text)
            return get_key.get_ranked_phrases()

        def build_keyword(row):
            merge_line = [x for x in row.tolist() if str(x) != 'nan']
            text = ", ".join(merge_line)
            output = keyword(text)
            return output

        def clean_keyword(keys, keys_duplicate):
            output = []
            for key in keys:
                for k in key:
                    if k in keys_duplicate:
                        key.remove(k)
                output.append(key)

            return output

        df = self.dictionary_file.copy()
        name_list = [name_col for name_col in df.columns.tolist() if "NAME" in name_col]
        df_name = df[name_list].copy()
        keys = df_name.apply(build_keyword, axis = 1).tolist()
        keys_list = [x for y in keys for x in y]
        keys_duplicate = [x for x,y in Counter(keys_list).items() if y > 1]
        df["KEYWORDS"] = clean_keyword(keys, keys_duplicate)
        # output check file
        df.to_excel("dictionary/file_for_check.xlsx", index=False)

        df_output = df[['ID', 'NAME', 'GGN', 'COUNTRY', 'CONTINENT', 'FOUNDATION_YEAR', 'KEYWORDS']]

        self.dictionary = df_output.copy()
        df_output.to_excel("dictionary/dictionary.xlsx", index=False)

        return df_output


