import re

original_names = ('test00123', 'SSNI827')

# pattern = r"[a-ZA-Z]+"

for original_name in original_names:
    match_result = re.search('^[a-zA-Z]+', original_name)
    if match_result:
        label = match_result.group()
        # print(label)

    match_result = re.search('\d{3}$', original_name)
    if match_result:
        number = match_result.group().replace('00', '')
        # print(number)

    transformed_name = label.__str__() + '-' + number.__str__()

    print('Original Name    : [' + original_name + ']')
    print('Transformed Name : [' + transformed_name + ']')
