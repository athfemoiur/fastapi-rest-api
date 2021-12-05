def serialize_dict(instance):
    return {i: str(instance[i]) if i == '_id' else instance[i] for i in instance}


def serialize_list(entity):
    return [serialize_dict(a) for a in entity]
