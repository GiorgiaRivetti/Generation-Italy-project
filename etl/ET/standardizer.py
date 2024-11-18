import re
import numpy as np


class Standardizer:

    @staticmethod
    def standardize_str_with_dict(input_str: str, keywords: dict) -> str:
        """
        Check if the input_str is in one of the keywords key and return the respective value, if not returns "Other"

        :param input_str: string you want to standardize
        :param keywords: the reference dict
        :return: keyword value or "Other"
        """
        title_lower = input_str.lower()
        for key in keywords:
            if re.search(key, title_lower):
                return keywords[key]
        return "Other"

    @staticmethod
    def get_keywords(text: str, keywords: list):
        """
        Extracts the keywords from a text

        :param text: input text
        :param keywords: the reference list
        :return: a string with only the extracted keywords separated by a comma
        """
        # Searches for keywords in the description
        found_keywords = [keyword for keyword in keywords if
                          re.search(rf'\b{keyword}\b', text, re.IGNORECASE)]

        if not found_keywords:
            return np.nan

        return ', '.join(found_keywords)

    @staticmethod
    def standardize_str_with_list(input_str: str, keywords: list):
        """
        Check if the input_str is in the list and return the list value, if not returns nan

        :param input_str: string you want to standardize
        :param keywords: the reference list
        :return: keyword value or nan
        """
        for keyword in keywords:
            if re.search(str(keyword), input_str):
                return keyword
        return np.nan

    @staticmethod
    def standardize_company_names(companies: list):
        # Create a copy of the list to work on. It will be used to create a list with clean and unique company names
        companies_copy = companies.copy()

        def clean_name(name):
            name = name.lower()
            # Remove unnecessary "."
            name = re.sub(r'\b(\w)\.(\w)\b', r'\1\2', name)
            # Remove srl and spa in any form
            name = re.sub(r'\s*(?:s\.?r\.?l\.?|s\.?p\.?a\.?)\.*\s*', '', name, flags=re.IGNORECASE)
            # Remove "italia" (but not "italy")
            name = re.sub(r'\bitalia\b', '', name, flags=re.IGNORECASE)
            # Remove anything after "-", "|" or "filiale"
            if len(name.split()) > 1:
                name = re.split(r'[-|]|filiale', name, flags=re.IGNORECASE)[0]
            # Remove unnecessary white spaces
            name = name.strip()

            return name

        # Clean company names
        companies_copy = [clean_name(name) for name in companies_copy]
        # Make a set to remove duplicates
        unique_companies = sorted(set(companies_copy))
        # Create list to use as reference
        reference_list = []

        # Cycle to get the companies with the same initial word one time only
        for i in range(len(unique_companies)):
            if len(reference_list) == 0:
                reference_list.append(unique_companies[i])
            else:
                last_added = reference_list[-1]
                current_first_word = unique_companies[i].split()[0]
                last_first_word = last_added.split()[0]
                if current_first_word != last_first_word:
                    reference_list.append(unique_companies[i])

        final_list = []

        for company in companies:
            company_lower = company.lower()
            cleaned_company = clean_name(company_lower)

            # Check if the first word is in one of the words in the reference_list and substitute it
            for ref_name in reference_list:
                if cleaned_company.startswith(ref_name.split()[0]):
                    cleaned_company = ref_name
                    break

            # Capitalize the first letter
            final_company = cleaned_company.capitalize()
            final_list.append(final_company)

        return final_list

