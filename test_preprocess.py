from preprocess import ArabertPreprocessor

if __name__ == "__main__":
    model_name = "aubmindlab/bert-base-arabertv2"
    arabert_prep = ArabertPreprocessor(model_name=model_name)
    text = "ولن نبالغ إذا قلنا: إن 'هاتف' أو 'كمبيوتر المكتب' في زمننا هذا ضروري"
    processed = arabert_prep.preprocess(text)
    print("Processed text:", processed)
