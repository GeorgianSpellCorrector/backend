import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List


class InferenceWrapper:
    model: AutoModelForSeq2SeqLM
    tokenizer: AutoTokenizer
    MODEL_PATH: str = 'ZurabDz/geo-spell-check-v8'
    DEVICE: str = 'cuda' if torch.cuda.is_available() else 'cpu' 
    USE_HALF: bool = True if DEVICE == 'cuda' else False

    TOP_K: float = 30
    TOP_P: float = 0.95
    MAX_LENGTH: int = 64

    def start(self):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_PATH)
        if self.USE_HALF:
            self.model = self.model.half(self.DEVICE).eval()

        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_PATH)

    async def inference(self, input: List[str]):
        input_ids = self.tokenizer(input, return_tensors='pt', 
                                   padding=True)['input_ids']
        
        if self.USE_HALF:
            input_ids = input_ids.half().to(self.DEVICE)


        outputs = self.model.generate(
            input_ids,
            max_length=self.MAX_LENGTH,
            do_sample=True,
            top_k=self.TOP_K,
            top_p=self.TOP_P,
            pad_token_id=self.model.config.pad_token_id
        )

        output_text = self.tokenizer.batch_decode(outputs,
                                                   skip_special_tokens=True)
        
        return output_text
    

inference_wrapper = InferenceWrapper()