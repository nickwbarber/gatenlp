def is_strict_match( x, y ):
    return x == y

def is_lenient_match( x, y ):
    """x and y must be sets"""
    intersection = x & y
    symmetric_difference = x ^ y
    return len( intersection )  > len( symmetric_difference )

def iter_true_positives(key_set,
                        response_set,
                        is_match):
    """"key_set and response_set must be a list of sets.
    is_match must be a comparative operation.
    """
    return (
        (x,y)
        for x in frozenset(response_set)
        for y in frozenset(key_set)
        if is_match(x,y)
    )

def iter_false_positives(key_set,
                         response_set,
                         is_match):
    """key_set and response_set must be a list of sets.
    is_match must be a comparative operation.
    """
    return (
        (x,y)
        for x in frozenset(response_set)
        for y in frozenset(key_set)
        if not is_match(x,y)
    )

def iter_false_negatives(key_set,
                         response_set,
                         is_match):
    """key_set and response_set must be a list of sets.
    is_match must be a comparative operation.
    """
    return (
        (x,y)
        for x in frozenset(key_set)
        for y in frozenset(response_set)
        if not is_match(x,y)
    )

def calc_precision(num_true_positives,
                   num_false_positives):
    try:
        return (
            ( num_true_positives ) /
            ( num_true_positives + num_false_positives )
        )
    except ZeroDivisionError:
        # Since dividing by zero only happens when both annot-
        # ators select nothing, evaluate this as perfect agree-
        # ment.
        return 1

def calc_recall(num_true_positives,
                num_false_negatives):
    try:
        return (
            ( num_true_positives ) /
            ( num_true_positives + num_false_negatives )
        )
    except ZeroDivisionError:
        # Since dividing by zero only happens when both annot-
        # ators select nothing, evaluate this as perfect agree-
        # ment.
        return 1

def calc_harmonic_mean( x, y ):
    return 2 * ( ( x * y ) / ( x + y ) )

def calc_f_measure(num_true_positives,
                   num_false_positives,
                   num_false_negatives):

    precision = calc_precision(
        num_true_positives,
        num_false_positives
    )
    recall = calc_recall(
        num_true_positives,
        num_false_negatives
    )

    try:
        return calc_harmonic_mean( precision, recall )
    except ZeroDivisionError:
        # Since division by zero will only happen when
        # no true-positives are selected, evaluate as
        # no agreement.
        return 0

def main():

    key_set = (
        frozenset( ( x + 0 for x in range(10) ) ),
    )
    response_set = (
        frozenset( ( x + 0 for x in range(10) ) ),
        frozenset( ( x + 0 for x in range(10) ) ),
        frozenset( ( x + 0 for x in range(10) ) ),
        frozenset( ( x + 0 for x in range(10) ) ),
        frozenset( ( x + 50 for x in range(10) ) ),
        frozenset( ( x + 70 for x in range(10) ) ),
        frozenset( ( x + 90 for x in range(10) ) ),
        frozenset( ( x + 10 for x in range(10) ) ),
    )

    num_true_positives = sum(
        1 for _ in iter_true_positives( key_set, response_set, is_lenient_match )
    )
    num_false_positives = sum(
        1 for _ in iter_false_positives( key_set, response_set, is_lenient_match )
    )
    num_false_negatives = sum(
        1 for _ in iter_false_negatives(key_set, response_set, is_lenient_match)
    )

    print(calc_f_measure(num_true_positives, num_false_positives, num_false_negatives))

if __name__ == "__main__":
    main()
