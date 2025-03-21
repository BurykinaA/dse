import torch 
from transformers import AutoModel, AutoTokenizer, AutoConfig

MODEL_CLASS = {
    "bertlarge": 'bert-large-uncased',
    "bertbase": 'bert-base-uncased',
    "robertabase": 'roberta-base',
    "robertalarge": 'roberta-large',
    'distilbertbase': 'distilbert-base-uncased',
}

def get_optimizer(model, args):
    if 'roberta' in args.bert:
        optimizer = torch.optim.Adam([
            {'params':model.roberta.parameters()}, 
            {'params':model.contrast_head.parameters(), 'lr': args.lr*args.lr_scale}], lr=args.lr)
    elif 'distilbert' in args.bert:
        optimizer = torch.optim.Adam([
            {'params':model.distilbert.parameters()}, 
            {'params':model.contrast_head.parameters(), 'lr': args.lr*args.lr_scale}], lr=args.lr)
    elif 'bert' in args.bert:
        optimizer = torch.optim.Adam([
            {'params':model.bert.parameters()}, 
            {'params':model.contrast_head.parameters(), 'lr': args.lr*args.lr_scale}], lr=args.lr)
    else:
        optimizer = torch.optim.Adam([
            {'params':model.model.parameters()}, 
            {'params':model.contrast_head.parameters(), 'lr': args.lr*args.lr_scale}], lr=args.lr)

    return optimizer 
    
def get_bert_config_tokenizer(model_name):
    if model_name in MODEL_CLASS:
        config = AutoConfig.from_pretrained(MODEL_CLASS[model_name])
        tokenizer = AutoTokenizer.from_pretrained(MODEL_CLASS[model_name])
    else:
        config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    return config, tokenizer
