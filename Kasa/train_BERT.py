from transformers import BertConfig
from transformers import BertTokenizerFast

#tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased") # use pretrained mBERT checkpoint tokenizer
tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased", do_lower_case=True) # for asante, lowercase pretrained tokenizer

#tokenizer.save_vocabulary("abena-base-akuapem-twi-cased") # when using pretrained tokenizer, be sure to save it locally
tokenizer.save_vocabulary("abena-base-asante-twi-uncased") # saving pretrained tokenizer locally in case of asante

#tokenizer = BertTokenizerFast.from_pretrained("abena-base-v2-akuapem-twi-cased", max_len=512) # how to use language-specific tokenizer trained with train_tokenizer.py

from transformers import BertForMaskedLM

#model = BertForMaskedLM.from_pretrained("bert-base-multilingual-cased") # start with mBERT checkpoint weights
model = BertForMaskedLM.from_pretrained("abena-base-akuapem-twi-cased") # for asante, start with akuapem weights

print("Number of parameters in mBERT model:")
print(model.num_parameters())

from transformers import LineByLineTextDataset

dataset = LineByLineTextDataset(
        tokenizer=tokenizer,
        # jw300.en-tw.tw # akuapem       
        file_path="../../data/asante_twi_bible.txt", # asante
        block_size=128)

from transformers import DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True, mlm_probability=0.15
)

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
#    output_dir="abena-base-akuapem-twi-cased",
    output_dir="abena-base-asante-twi-uncased", # asante
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_gpu_train_batch_size=16,
    save_steps=10_000,
    save_total_limit=1,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    prediction_loss_only=True,
)

trainer.train()

#trainer.save_model("abena-base-akuapem-twi-cased")
trainer.save_model("abena-base-asante-twi-uncased") # asante

from transformers import pipeline

fill_mask = pipeline(
    "fill-mask",
    model="abena-base-asante-twi-uncased",
    tokenizer=tokenizer
)

print(fill_mask("Eyi de ɔhaw kɛse baa [MASK] hɔ."))
