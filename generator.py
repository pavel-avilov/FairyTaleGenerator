from happytransformer import HappyGeneration, GENSettings

model = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-125M", load_path="FairyTaleModel")

min_l = 150
genArgs = GENSettings(
    max_length=min_l + 100,
    min_length=min_l,
    no_repeat_ngram_size=2,
    temperature=0.7,
    top_p=0.8,
    do_sample=True,
    early_stopping=True
)


def generate_fairy_tale(data_string):
    text = model.generate_text(
        text=data_string,
        args=genArgs
    ).text
    for i in reversed(range(len(text))):
        if text[i] in '!.?':
            text = text[: i + 1]
            break
    text = '. '.join(list(map(lambda x: x.strip().capitalize(), text.split('.'))))
    return data_string + text
