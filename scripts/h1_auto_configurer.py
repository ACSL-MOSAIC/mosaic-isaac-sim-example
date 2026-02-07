from mosaic_core import auto_configurer


class H1AutoConfigurer(auto_configurer.AutoConfigurer):
    def __init__(self, h1_demo):
        super().__init__()
        self.h1_demo = h1_demo

    def before_configure(self):
        for configurable_connectors in self.configurable_connectors:
            # if configurable_connectors is an instance of H1ConnectorConfigurer, set the h1_demo
            if hasattr(configurable_connectors, 'set_h1_demo'):
                configurable_connectors.set_h1_demo(self.h1_demo)

