# Utility functions for geneators

def colorhex(color):
    result = '%02X%02X%02X' % tuple(color[:3])
    if len(result) != 6:
        raise Exception('Invalid color range')
    return result

