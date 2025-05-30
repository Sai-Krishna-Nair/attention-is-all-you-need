# Importing necessary libraries
import torch
import torch.nn as nn
import torch.nn.functional as F


# Vocabularies for English and French
# These vocabularies are simplified and may not cover all words in the languages.
word_map_en = {
    "<pad": 0, "<sos": 1, "<eos": 2, "<unk": 3, "I": 4, "you": 5, "he": 6, "she": 7, "it": 8, "we": 9, "they": 10, "my": 11, "your": 12, "his": 13, "her": 14,
    "our": 15, "their": 16, "am": 17, "is": 18, "are": 19, "was": 20, "were": 21, "be": 22, "been": 23, "have": 24, "has": 25, "had": 26, "do": 27, "does": 28, "did": 29,
    "can": 30, "could": 31, "will": 32, "would": 33, "should": 34, "must": 35, "go": 36, "goes": 37, "went": 38, "eat": 39, "eats": 40, "ate": 41, "drink": 42, "drinks": 43, "drank": 44,
    "see": 45, "sees": 46, "saw": 47, "read": 48, "reads": 49, "like": 50, "likes": 51, "liked": 52, "love": 53, "loves": 54, "loved": 55, "hate": 56, "hates": 57, "hated": 58, "want": 59,
    "wants": 60, "wanted": 61, "need": 62, "needs": 63, "make": 64, "makes": 65, "made": 66, "take": 67, "takes": 68, "took": 69, "book": 70, "books": 71, "car": 72, "cars": 73, "house": 74,
    "houses": 75, "dog": 76, "dogs": 77, "cat": 78, "cats": 79, "man": 80, "men": 81, "woman": 82, "women": 83, "child": 84, "children": 85, "friend": 86, "friends": 87, "food": 88, "water": 89,
    "day": 90, "days": 91, "time": 92, "school": 93, "work": 94, "a": 95, "an": 96, "the": 97, "and": 98, "but": 99, "or": 100, "in": 101, "on": 102, "at": 103, "to": 104,
    "from": 105, "with": 106, "without": 107, "for": 108, "of": 109, "very": 110, "really": 111, "not": 112, "now": 113, "today": 114, "yesterday": 115, "tomorrow": 116, "here": 117, "there": 118, "good": 119,
    "bad": 120, "big": 121, "small": 122, "new": 123, "old": 124, "happy": 125, "sad": 126, ".": 127, "?": 128, "!": 129
}


word_map_fr = {
    "<pad": 0, "<sos": 1, "<eos": 2, "<unk": 3, "je": 4, "tu": 5, "il": 6, "elle": 7, "on": 8, "nous": 9, "vous": 10, "ils": 11, "elles": 12, "mon": 13, "ma": 14,
    "mes": 15, "ton": 16, "ta": 17, "tes": 18, "son": 19, "sa": 20, "ses": 21, "notre": 22, "nos": 23, "votre": 24, "vos": 25, "leur": 26, "leurs": 27, "suis": 28, "es": 29,
    "est": 30, "sommes": 31, "êtes": 32, "sont": 33, "étais": 34, "était": 35, "être": 36, "ai": 37, "as": 38, "a": 39, "avons": 40, "avez": 41, "ont": 42, "avais": 43, "avait": 44,
    "fais": 45, "fait": 46, "faisons": 47, "faites": 48, "font": 49, "vais": 50, "vas": 51, "va": 52, "allons": 53, "allez": 54, "vont": 55, "mange": 56, "manges": 57, "mangeons": 58, "mangez": 59,
    "mangent": 60, "bois": 61, "boit": 62, "buvons": 63, "buvez": 64, "boivent": 65, "vois": 66, "voit": 67, "voyons": 68, "voyez": 69, "voient": 70, "aime": 71, "aimes": 72, "aimons": 73, "aimez": 74,
    "aiment": 75, "veux": 76, "veut": 77, "voulons": 78, "voulez": 79, "veulent": 80, "livre": 81, "livres": 82, "voiture": 83, "voitures": 84, "maison": 85, "maisons": 86, "chien": 87, "chiens": 88, "chat": 89,
    "chats": 90, "homme": 91, "hommes": 92, "femme": 93, "femmes": 94, "enfant": 95, "enfants": 96, "ami": 97, "amie": 98, "amis": 99, "amies": 100, "nourriture": 101, "eau": 102, "jour": 103, "jours": 104,
    "temps": 105, "école": 106, "travail": 107, "un": 108, "une": 109, "le": 110, "la": 111, "les": 112, "et": 113, "mais": 114, "ou": 115, "dans": 116, "sur": 117, "à": 118, "de": 119,
    "avec": 120, "sans": 121, "pour": 122, "très": 123, "vraiment": 124, "ne": 125, "pas": 126, "maintenant": 127, "aujourd'hui": 128, "hier": 129, "demain": 130, "ici": 131, "là": 132, "bon": 133, "bonne": 134,
    "mauvais": 135, "mauvaise": 136, "grand": 137, "grande": 138, "petit": 139, "petite": 140, "nouveau": 141, "nouvelle": 142, "vieux": 143, "vieille": 144, "heureux": 145, "heureuse": 146, "triste": 147, ".": 148, "?": 149, "!": 150
}

  
# Tokenizer
def tokenize(sentence,word_map):
    return torch.tensor([word_map[word] for word in sentence.split()])

 
#Positional Encoding
class PositionalEncoding(nn.Module):
    def __init__(self,d_model,max_len = 5000):
        super(PositionalEncoding,self).__init__()
        self.PE = torch.zeros(max_len,d_model)
        i = torch.arange(0,d_model,2).float()
        token_pos = torch.arange(0,max_len,dtype = torch.float).unsqueeze(1)
        d = torch.pow(1000,2*i/d_model)
        self.PE[:,0::2] = torch.sin(token_pos/d)
        self.PE[:,1::2] = torch.cos(token_pos/d)
        self.PE = self.PE.unsqueeze(0)


    def forward(self,x):
        return x+self.PE[:,:x.size(1)]
        

 
#Multi-Head Attention
class MultiHeadAttention(nn.Module):
    def __init__(self,d_model,num_heads):
        super(MultiHeadAttention,self).__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model//num_heads
        self.query = nn.Linear(d_model,d_model)
        self.key = nn.Linear(d_model,d_model)
        self.value = nn.Linear(d_model,d_model)
        self.fc = nn.Linear(d_model,d_model)

    
    def forward(self,q_input,k_input,v_input,mask=None):
        batch_size,max_len,_ = q_input.size()
        Q = self.query(q_input)
        K = self.key(q_input)
        V= self.value(q_input)
        
        q = Q.reshape(batch_size,max_len,self.num_heads,self.d_k).transpose(1,2)
        k = K.reshape(batch_size,max_len,self.num_heads,self.d_k).transpose(1,2)
        v = V.reshape(batch_size,max_len,self.num_heads,self.d_k).transpose(1,2)


        attn_scores = torch.matmul(q,k.transpose(-2,-1))/torch.sqrt(torch.tensor(self.d_k,dtype=torch.float))
        if mask is not None:
            attn_scores = attn_scores.masked_fill(mask==0,float('-inf'))

            
        attn_weights = F.softmax(attn_scores,dim=-1)
        attn_output = torch.matmul(attn_weights,v).transpose(1,2).contiguous().view(batch_size,max_len,self.d_model)
        output = self.fc(attn_output)
        
        return output

#Feed-Forward Network
class PositionwiseFeedForward(nn.Module): 
    def __init__(self,d_model,hidden,drop_prob=0.1):
        super(PositionwiseFeedForward,self).__init__()
        self.linear1 = nn.Linear(d_model,hidden)
        self.linear2 = nn.Linear(hidden,d_model)
        self.relu = nn.ReLU()
        self.dropout =  nn.Dropout(p = drop_prob)
    def forward(self,x):
        x = self.relu(self.linear1(x))
        x = self.dropout(x)
        x = self.linear2(x)
        return x


#Encoder Layer
class EncoderLayer(nn.Module):
    def __init__(self,d_model,ffn_hidden,num_heads,drop_prob):
        super(EncoderLayer,self).__init__()
        self.mha = MultiHeadAttention(d_model = d_model, num_heads = num_heads)
        self.drop1 = nn.Dropout(p=drop_prob)
        self.norm1 = nn.LayerNorm(d_model,eps = 1e-6)
        self.feedforward = PositionwiseFeedForward(d_model = d_model,hidden= ffn_hidden,drop_prob=drop_prob)
        self.drop2 = nn.Dropout(p=drop_prob)
        self.norm2 = nn.LayerNorm(d_model,1e-6)
    def forward(self,x,mask=None):
        attn_output = self.mha(x,x,x,mask=None)
        attn_output = self.drop1(attn_output)
        x = self.norm1(attn_output + x)
        ffn_output = self.feedforward(x)
        ffn_output = self.drop2(ffn_output)
        enc_out = self.norm2(ffn_output + x)
        return enc_out

# Encoder
class Encoder(nn.Module):
    def __init__(self,d_model,ffn_hidden,num_heads,drop_prob,num_layers):
        super().__init__()
        self.layers = nn.Sequential(*[EncoderLayer(d_model,ffn_hidden,num_heads,drop_prob) for _ in range(num_layers)])
    def forward(self,x):
        x = self.layers(x)
        return x




#Decoder Layer
class DecoderLayer(nn.Module):
    def __init__(self,d_model,ffn_hidden,num_heads,drop_prob):
        super(DecoderLayer,self).__init__()
        self.masked_mha = MultiHeadAttention(d_model = d_model, num_heads = num_heads)
        self.drop1 = nn.Dropout(p = drop_prob)
        self.norm1 = nn.LayerNorm(d_model,eps = 1e-6)
        
        self.encoder_decoder_mha = MultiHeadAttention(d_model = d_model, num_heads = num_heads)
        self.drop2 = nn.Dropout(p = drop_prob)
        self.norm2 = nn.LayerNorm(d_model,eps = 1e-6)
        
        self.feedforward = PositionwiseFeedForward(d_model = d_model,hidden = ffn_hidden,drop_prob=drop_prob)
        self.drop3 = nn.Dropout(p = drop_prob)
        self.norm3 = nn.LayerNorm(d_model,eps = 1e-6)

    
    def forward(self,x,enc_out_k,enc_out_v,decoder_mask):
        masked_o = self.masked_mha(x,x,x,mask=decoder_mask)
        masked_o = self.drop1(masked_o)
        x = self.norm1(x + masked_o)
        
        cross_attn_o = self.encoder_decoder_mha(x,enc_out_k,enc_out_v,mask = None)
        cross_attn_o= self.drop2(cross_attn_o)
        x = self.norm2(x + cross_attn_o)
        
        ffn_output = self.feedforward(x)
        ffn_output = self.drop3(ffn_output)
        dec_out = self.norm3(x + ffn_output)
        
        return dec_out   

# Sequential Decoder 
class SequentialDecoder(nn.Sequential):
    def forward(self, *inputs):
        x, enc_out_k, enc_out_v, mask = inputs
        for module in self._modules.values():
            y = module(x, enc_out_k, enc_out_v, mask) #30 x 200 x 512
        return y

# Decoder
class Decoder(nn.Module):
    def __init__(self, d_model, ffn_hidden, num_heads, drop_prob, num_layers):
        super().__init__()
        self.layers = SequentialDecoder(*[DecoderLayer(d_model, ffn_hidden, num_heads, drop_prob)
                                     for _ in range(num_layers)])

    def forward(self, x, enc_out_k, enc_out_v, mask):
        x = self.layers(x, enc_out_k, enc_out_v, mask)
        return x

 
#Transformer Model
class Transformer(nn.Module):
    def __init__(self,vocab_size,d_model,num_heads,ffn_hidden,num_encoder_layers,num_decoder_layers,drop_prob=0.2,max_len=5000):
        super(Transformer,self).__init__()
        self.embedding = nn.Embedding(vocab_size,d_model)
        self.pos_encoder = PositionalEncoding(d_model,max_len)
        self.encoder = Encoder(d_model,ffn_hidden,num_heads,drop_prob,num_encoder_layers)
        self.decoder = Decoder(d_model,ffn_hidden,num_heads,drop_prob,num_decoder_layers)
        self.fc = nn.Linear(d_model,vocab_size)
    def forward(self,src,trgt,trgt_mask=None):
        src = self.pos_encoder(self.embedding(src))
        trgt = self.pos_encoder(self.embedding(trgt))
        encoder_o =  self.encoder(src)
        decoder_o = self.decoder(trgt,encoder_o,encoder_o,trgt_mask)
        output = self.fc(decoder_o)
        return output     

 
#Prediction  
def translate(input_sentence, word_map_en, word_map_fr, transformer):
    # Tokenize input sentence
    input_tensor = tokenize(input_sentence, word_map_en).unsqueeze(0)  # Shape (1, seq_len)
    
    # Generate a mask for the target sentence
    tgt_mask = torch.tril(torch.ones((input_tensor.size(1), input_tensor.size(1)))).unsqueeze(0).unsqueeze(0)  # Lower triangular mask

    # Initialize a tensor for the target sentence
    target_tensor = torch.zeros((1, input_tensor.size(1)), dtype=torch.long)

    # Predict the output sentence (translation)
    output = transformer(input_tensor, target_tensor, tgt_mask)

    # Apply Softmax to get probabilities
    softmax_output = F.softmax(output, dim=-1)

    # Get predicted token indices 
    predicted_tokens = torch.argmax(softmax_output, dim=-1)

    # Convert predicted tokens back to words
    reverse_word_map_fr = {v: k for k, v in word_map_fr.items()}
    translated_sentence = [reverse_word_map_fr[token.item()] for token in predicted_tokens[0] if token != 0]

    return " ".join(translated_sentence)

 
#Initialize Model
vocab_size_en = len(word_map_en)
vocab_size_te = len(word_map_fr)
d_model = 128
num_heads = 8
num_encoder_layers = 2
num_decoder_layers = 2
ffn_hidden = 32
drop_prob=0.2 
max_len=500

transformer = Transformer(vocab_size_te, d_model, num_heads, ffn_hidden, num_encoder_layers, num_decoder_layers, drop_prob, max_len)

 
#Take Input Sentence and Generate Translation
input_sentence = "I am happy ."  # input sentence
predicted_sentence = translate(input_sentence, word_map_en, word_map_fr, transformer)
print("Input Sentence:", input_sentence)
print("Predicted Translation:", predicted_sentence)

  



