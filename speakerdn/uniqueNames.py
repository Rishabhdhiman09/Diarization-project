import re
def unique_names(text):
    name_list = re.findall("Speaker\w+", text)
    return list(set(name_list))