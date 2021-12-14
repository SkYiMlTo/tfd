a = [1, 2, 3, 2, 1, 5, 6, 5, 5, 5, 4, 4]

import collections
print([item for item, count in collections.Counter(a).items() if count > 1])