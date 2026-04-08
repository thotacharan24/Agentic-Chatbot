from configparser import ConfigParser


class Config:
    def __init__(self,config_file="./src/langgraphagenticai/ui/uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)

    def get_llm_options(self):
        return [option.strip() for option in self.config["DEFAULT"].get("LLM_OPTIONS", "").split(",") if option.strip()]
    
    def get_usecase_options(self):
        return [option.strip() for option in self.config["DEFAULT"].get("USECASE_OPTIONS", "").split(",") if option.strip()]

    def get_groq_model_options(self):
        return [option.strip() for option in self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS", "").split(",") if option.strip()]

    def get_default_groq_model(self):
        return self.config["DEFAULT"].get("DEFAULT_GROQ_MODEL", self.get_groq_model_options()[0])
    
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
