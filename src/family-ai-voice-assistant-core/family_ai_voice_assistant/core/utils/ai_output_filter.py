class AiOutputFilter:

    @staticmethod
    def filter_output(text: str) -> str:
        return AiOutputFilter.markdown_symbol_filter(text)

    @staticmethod
    def markdown_symbol_filter(text: str) -> str:
        return text.replace("*", "").replace("#", "")
