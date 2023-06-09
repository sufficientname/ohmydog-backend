def make_choices(choices_dict):
    return [
        (choice['id'], choice['label']) for choice in choices_dict.values()
    ]

def choice(id, label):
    return {'id': id, 'label': label}