
from dataclasses import dataclass
from typing import List
from . import features


@dataclass
class ProductMetadata(object):
    """
    Metadata for a Stripe product.
    """
    stripe_id: str
    name: str
    features: List[str]
    description: str = ''
    is_default: bool = False


Professional = ProductMetadata(
    stripe_id='prod_LZfElI2ZiqTqzK',
    name='Professional',
    description='For small businesses and teams',
    is_default=False,
    features=[
        features.UNLIMITED_PRODUCTS,
        
    ],
)
Basic = ProductMetadata(
    stripe_id='prod_LZewfE80o3qSXd',
    name='Basic',
    description='For small businesses and teams',
    is_default=False,
    features=[
        features.LIMITED_PRODUCTS,
    ],
)