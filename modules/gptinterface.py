import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from mingpt.model import GPT
from mingpt.utils import set_seed
from mingpt.bpe import BPETokenizer


class GPTInterface():
    def __init__(self):
        # establish connection

        set_seed(3407)

        self.use_mingpt = True # use minGPT or huggingface/transformers model?
        self.model_type = "gpt2-xl"
        self.device = "cuda"

        if self.use_mingpt:
            self.model = GPT.from_pretrained(self.model_type)
        else:
            self.model = GPT2LMHeadModel.from_pretrained(self.model_type)
            self.model.config.pad_token_id = self.model.config.eos_token_id # suppress a warning

        # ship model to self.device and set to eval mode
        self.model.to(self.device)
        self.model.eval()

        pass

    def get_answer(question):
        # get answer

        answer = question
        return answer

    def generate(self, prompt="", num_samples=10, steps=20, do_sample=True):
            
        # tokenize the input prompt into integer input sequence
        if self.use_mingpt:
            tokenizer = BPETokenizer()
            if prompt == "":
                # to create unconditional samples...
                # manually create a tensor with only the special <|endoftext|> token
                # similar to what openai"s code does here https://github.com/openai/gpt-2/blob/master/src/generate_unconditional_samples.py
                x = torch.tensor([[tokenizer.encoder.encoder["<|endoftext|>"]]], dtype=torch.long)
            else:
                x = tokenizer(prompt).to(self.device)
        else:
            tokenizer = GPT2Tokenizer.from_pretrained(self.model_type)
            if prompt == "": 
                # to create unconditional samples...
                # huggingface/transformers tokenizer special cases these strings
                prompt = "<|endoftext|>"
            encoded_input = tokenizer(prompt, return_tensors="pt").to(self.device)
            x = encoded_input["input_ids"]
        
        # we"ll process all desired num_samples in a batch, so expand out the batch dim
        x = x.expand(num_samples, -1)

        # forward the model `steps` times to get samples, in a batch
        y = self.model.generate(x, max_new_tokens=steps, do_sample=do_sample, top_k=40)
        
        for i in range(num_samples):
            out = tokenizer.decode(y[i].cpu().squeeze())
            print(out)

if __name__ == "__main__":
    print(1)
    gpti = GPTInterface()
    print(2)
    gpti.generate("My balls")
    print(3)

