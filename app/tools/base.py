class BaseTool:

    name: str
    description: str

    def execute(self, **kwargs):
        raise NotImplementedError
