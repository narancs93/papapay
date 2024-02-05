def remove_prefix(string, prefix_to_remove):
    if string.startswith(prefix_to_remove):
        result_string = string[len(prefix_to_remove):]
    else:
        result_string = string
    return result_string
