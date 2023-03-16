
class Min:
    def __init__(self, minValue, error_message="Value must be greater than or equal to {0}"):
        self.minValue = minValue
        self.error_message = error_message.format(minValue)

    def __call__(self, value):
        return float(value) >= self.minValue
    
class Max:
    def __init__(self, maxValue, error_message="Value must be less than or equal to {0}"):
        self.maxValue = maxValue
        self.error_message = error_message.format(maxValue)

    def __call__(self, value):
        return float(value) <= self.maxValue

class Is_float:
    def __init__(self, error_message="Value must be a float number"):
        self.error_message = error_message

    def __call__(self, value):
        return value.replace(".", "").isnumeric()


class Is_number:
    def __init__(self, error_message="Value must be a number"):
        self.error_message = error_message

    def __call__(self, value):
        return value.isnumeric()