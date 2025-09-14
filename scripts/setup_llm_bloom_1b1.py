from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_llm(model_name="bigscience/bloom-1b1"):
    print(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return qa_pipeline