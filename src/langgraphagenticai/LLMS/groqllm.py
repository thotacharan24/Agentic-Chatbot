import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    SUPPORTED_GROQ_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "openai/gpt-oss-120b",
    ]

    PRIMARY_MODEL = SUPPORTED_GROQ_MODELS[0]

    def __init__(self, user_contols_input):
        self.user_controls_input = user_contols_input

    def _get_api_key(self):
        return (
            self.user_controls_input.get("GROQ_API_KEY", "")
            or os.environ.get("GROQ_API_KEY", "")
        )

    def _normalize_requested_model(self):
        requested_model = self.user_controls_input.get("selected_groq_model", "")
        if requested_model in self.SUPPORTED_GROQ_MODELS:
            return requested_model
        return self.PRIMARY_MODEL

    def _get_model_chain(self, requested_model):
        chain = [requested_model]
        for fallback_model in self.SUPPORTED_GROQ_MODELS:
            if fallback_model not in chain:
                chain.append(fallback_model)
        return chain

    def _validate_model_name(self, model_name: str):
        if model_name not in self.SUPPORTED_GROQ_MODELS:
            raise ValueError(
                f"Unsupported Groq model '{model_name}'. Supported models: {', '.join(self.SUPPORTED_GROQ_MODELS)}"
            )

    def get_llm_model(self):
        try:
            groq_api_key = self._get_api_key()
            if not groq_api_key:
                raise ValueError(
                    "GROQ API key is required. Set it in the UI or via the GROQ_API_KEY environment variable."
                )

            requested_model = self._normalize_requested_model()
            model_chain = self._get_model_chain(requested_model)
            errors = []

            for model_name in model_chain:
                try:
                    self._validate_model_name(model_name)
                    return ChatGroq(api_key=groq_api_key, model=model_name)
                except Exception as e:
                    errors.append(f"{model_name}: {str(e)}")
                    if model_name != requested_model:
                        st.warning(
                            f"Falling back to supported model '{model_name}' after failure with '{requested_model}'."
                        )
                    continue

            raise ValueError(
                "Unable to initialize Groq model. Tried: " + ", ".join(errors)
            )
        except Exception as e:
            raise ValueError(f"Error occurred while creating Groq LLM: {e}")