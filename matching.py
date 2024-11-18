
def longest_common_substring(X, Y): # Longest Common (continuos) SUBSTRING
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for i in range(m + 1)]
    # O(n^2), not an optimal solution but acceptable for small strings
    for i in range(m + 1):
        for j in range(n + 1):
            if i and j and X[i - 1].lower() == Y[j - 1].lower():
                L[i][j] = L[i - 1][j - 1] + 1
    return max(max(row) for row in L)

def confidence_key_matching(X, Y):
    l = longest_common_substring(X, Y)
    return (l / len(X) + l / len(Y)) / 2 # proposed formula

def match(standard_keys, supplier_keys):
    # can be replace by a machine learning model or a llm
    map = dict()
    dest = dict()
    for standard_key in standard_keys:
        target = ""
        conf = 0
        for supplier_key in supplier_keys:
            c = confidence_key_matching(standard_key, supplier_key)
            if c > conf:
                target = supplier_key
                conf = c
        if conf > 0.5 or standard_key == "hotel_id": # hotel_id is a must so it should be matched
            map[standard_key] = target
            
            # handle duplicate keys
            if target not in dest:
                dest[target] = (standard_key, conf)
            else:
                if dest[target][1] < conf:
                    dest[target] = (standard_key, conf)
    
    delete = []
    for key in map:
        if dest[map[key]][0] != key:
            delete.append(key)
    for key in delete:
        del map[key]
        
    return map