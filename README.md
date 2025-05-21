# Attention is all you need (Transformer from Scratch)

This is a **from-scratch implementation** of the original Transformer model introduced in the paper *Attention is All You Need* (Vaswani et al., 2017)*. It includes the core components like **tokenization**,**positional encoding**,**multi-head self-attention**,**encoder and decoder blocks** etc. All written **purely using pytorch**

#### This implementation is designed for a machine translation task from English to French, as in the original paper.



##  What's Inside

* Tokenizer and basic vocabulary builder
* Positional encodings (sinusoidal, just like the paper)
* Multi-head self-attention from scratch
* Optional masking logic
* Feedforward network
---

##  Try It Out

```bash
python main.py
```

Expect weird outputs — it’s just a forward pass on untrained weights ,there is no training loop. As a result, the outputs are mostly nonsensical :) .

---
## Reference

 The paper - [Attention is All You Need](https://arxiv.org/pdf/1706.03762).

---

