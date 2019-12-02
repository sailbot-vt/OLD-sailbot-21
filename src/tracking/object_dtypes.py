import numpy as np

from src.tracking.classification_types import ObjectType

buoy_array_dtype = [('range', float), ('bearing', float)]
object_array_dtype = [('range', float), ('bearing', float), ('type', ObjectType)]
