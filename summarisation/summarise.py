import re, torch
from model import ModelLoader

SUMMARY_RE = re.compile(r"summary:assistant\s*(.*)", re.I | re.S)

def _extract_summary(txt: str):
    m = SUMMARY_RE.search(txt)
    return m.group(1).strip() if m else txt.strip()

def prompt_handler(text, type="eea", dataset="civilsum"):
    if type=="eea":
        return [
            {
                "role": "system",
                "content": "You are a proficient legal assistant specializing in summarizing legal texts.",
            },
            {
                "role": "user",
                "content": f"""You are a proficient legal assistant. Your goal is to generate a clear, concise, and accurate summary that logically flows from the facts through to the ruling. Follow the steps below:

1. **Key Facts**: Start by summarizing the key facts, emphasizing their relevance to the issues at hand. Identify the most critical facts that shape the case.
2. **Issues**: Identify the legal issues involved. Clearly explain the relationship between these issues and the facts presented.
3. **Arguments**: Summarize the key arguments, highlighting how they connect to the facts and issues. Include both sides of the argument where relevant.
4. **Lower Court Rulings**: Explain the ruling of the lower court, linking it to the arguments and the relevant statutes or legal principles.
5. **Statutes**: Clarify the statutes that underpin the case, explaining how they are applied in this context.
6. **Precedents**: Discuss any relevant precedents, explaining how they support or influence the case at hand.
7. **Present Court’s Ruling**: Finally, explain the ruling by the present court, summarizing how it integrates the facts, issues, arguments, and precedents.

Your summary should present a unified narrative that integrates these categories in a logical and coherent way, ensuring that each element supports the others.
\n {text}""",
            },
        ]
    else: 
        if dataset == "civilsum":
            return [
            {
                "role": "system",
                "content": "You are a proficient legal assistant specializing in summarizing legal texts.",
            },
            {
                "role": "user",
                "content": f"You are a proficient legal assistant specializing in summarizing legal texts. Summarize the following judgement in 4-5 sentences or less. \n text: {text} \n summary:",
            }]
        
        return [
            {
                "role": "system",
                "content": "You are a proficient legal assistant specializing in summarizing legal texts.",
            },
            {
                "role": "user",
                "content": f"You are a proficient legal assistant specializing in summarizing legal texts. Summarize the following entire following text in 4-5 sentences or less as a single paragraph. \n text: {len(text)*0.5} \n summary:",
            },
        ]


def generate_summary(text, model, tokenizer, reference=None,
    model_name="phi-4",
    device="cuda", dataset="inabs", type="eea"):
    
    prompt_msgs = prompt_handler(text, type, dataset)
    prompt = tokenizer.apply_chat_template(prompt_msgs,
        tokenize=False,
        add_generation_prompt=True)
    
    with torch.inference_mode():
        tokens = tokenizer(prompt, return_tensors='pt').to(device)
        out = model.generate(**tokens,
        max_new_tokens=5000,
        temperature=0.6,
        top_p=0.9,
        do_sample=False)
        summary = _extract_summary(tokenizer.decode(out[0], skip_special_tokens=True))
    if reference is None:
        return summary
    return summary