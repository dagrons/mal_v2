from .basicConfig import basicConfig
from .developmentConfig import developmentConfig
from .productionConfig import productionConfig
from .testConfig import testConfig

config = {
    'development': developmentConfig,
    'production': productionConfig,
    'test': testConfig
}