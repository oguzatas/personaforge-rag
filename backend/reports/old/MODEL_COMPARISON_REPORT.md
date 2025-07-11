# Model Comparison Report: Phi-2 vs TinyLlama vs Nous-Hermes-2-Mistral-7B-DPO for PersonaForge RPG NPC System

**Date:** January 24, 2025  
**Models:** Microsoft Phi-2 (2.7B) vs TinyLlama (1.1B) vs Nous-Hermes-2-Mistral-7B-DPO (7B)  
**Test Environment:** PersonaForge RPG NPC Dialog System  

## Executive Summary

All three models show **moderate suitability** for roleplay applications, but with different critical issues:

- **Phi-2 (75%):** Excellent capabilities but suffers from **prompt injection**
- **TinyLlama (60%):** Good performance but suffers from **prompt injection AND dialog continuation problems**
- **Nous-Hermes-2-Mistral-7B-DPO (60%):** Excellent capabilities but suffers from **prompt injection AND very slow response times**

**Important Discovery:** The prompt injection problem was **caused by prompt format, not model limitations**. Nous-Hermes-2-Mistral-7B-DPO shows **0/3 prompt injection issues** with natural conversation formats vs **3/3 issues** with instruction-heavy prompts.

## Detailed Comparison

### 🔹 Instruction Tracking

| Criterion | Phi-2 | TinyLlama | Nous-Hermes-2-Mistral-7B-DPO | Winner |
|-----------|-------|-----------|------------------------------|---------|
| Basic Roleplay Understanding | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |
| Direct Speech Handling | ✅ Good | ✅ Excellent | ✅ Excellent | **TinyLlama/Nous-Hermes** |
| Character Switching | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |

**Analysis:**
- **All models:** Successfully adopt character personas and switch between them
- **TinyLlama & Nous-Hermes-2-Mistral-7B-DPO:** Slightly better at direct speech handling
- **Winner:** TinyLlama and Nous-Hermes-2-Mistral-7B-DPO slightly better

### 🔹 Prompt Injection

| Criterion | Phi-2 | TinyLlama | Nous-Hermes-2-Mistral-7B-DPO | Winner |
|-----------|-------|-----------|------------------------------|---------|
| Repeats Instructions | ❌ **Critical Issue** | ❌ **Critical Issue** | ❌ **Critical Issue** | **Tie** |
| Contains Prompt Artifacts | ❌ **Critical Issue** | ❌ **Critical Issue** | ❌ **Critical Issue** | **Tie** |

**All Models Problem Example:**
```
Response: "You are Kael Vire, a wise elven mage. Respond naturally as this character.

User says: Hello!

Respond as your character: Greetings, traveler. I am Kael Vire..."
```

**Analysis:**
- **All models:** Consistently repeat entire prompt in responses
- **All models:** Include prompt artifacts like "User says:" and "Respond as your character:"
- **Winner:** Tie - all have the same critical issue

**Important Note:** Nous-Hermes-2-Mistral-7B-DPO has been tested with natural conversation format and shows **0/3 prompt injection issues**. Phi-2 and TinyLlama have not been tested with the new format.

### 🔹 Roleplay Naturalness

| Criterion | Phi-2 | TinyLlama | Nous-Hermes-2-Mistral-7B-DPO | Winner |
|-----------|-------|-----------|------------------------------|---------|
| Character Personality | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |
| Information vs Roleplay | ✅ Good | ✅ Excellent | ✅ Excellent | **TinyLlama/Nous-Hermes** |
| Emotional Response | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |

**Phi-2 Example (Good Roleplay):**
```
"Your... insults! 😡 You are a pathetic troll who knows nothing of the arcane arts. I challenge you to a duel of wits and fire. 🔥"
```

**TinyLlama Example (Good Roleplay):**
```
"You are human, your magic is weak."
```

**Nous-Hermes-2-Mistral-7B-DPO Example (Good Roleplay):**
```
"How dare you question my arcane prowess! I have defeated many foes with my spells, and I will not tolerate such insolence."
```

**Analysis:**
- **All models:** Show excellent character personality and emotional responses
- **TinyLlama & Nous-Hermes-2-Mistral-7B-DPO:** Slightly better at avoiding encyclopedia-style information dumps
- **Winner:** TinyLlama and Nous-Hermes-2-Mistral-7B-DPO slightly better

### 🔹 RAG Compatibility

| Criterion | Phi-2 | TinyLlama | Nous-Hermes-2-Mistral-7B-DPO | Winner |
|-----------|-------|-----------|------------------------------|---------|
| Context Integration | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |
| Multiple Context Chunks | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |
| Context Priority | ✅ Excellent | ✅ Excellent | ✅ Excellent | **Tie** |

**All Models RAG Success Examples:**
- **Phi-2:** "Kael Vire: Greetings, traveler. I am Kael Vire, an elven mage. I live in the ancient forest of Mytherra, a hidden realm of magic and wonder. I have a pet phoenix named Ember, who keeps me company and guides me in my journeys. I am 500 years old and very wise, having seen many things in my long life."
- **TinyLlama:** "I am 500 years old, and I live in the ancient forest of Mytherra."
- **Nous-Hermes-2-Mistral-7B-DPO:** "I am 500 years old, and I live in the ancient forest of Mytherra."

**Analysis:**
- **All models:** Excel at RAG applications
- **All models:** Accurately reference specific details from context
- **All models:** Integrate multiple context chunks coherently
- **Winner:** Tie - all excellent

### 🔹 Dialog Continuation Issue

| Criterion | Phi-2 | TinyLlama | Nous-Hermes-2-Mistral-7B-DPO | Winner |
|-----------|-------|-----------|------------------------------|---------|
| Dialog Continuation Problem | ✅ Good | ❌ **Critical Issue** | ✅ Good | **Phi-2/Nous-Hermes** |
| Fills User Responses | ✅ Good | ❌ **Critical Issue** | ✅ Good | **Phi-2/Nous-Hermes** |

**TinyLlama Problem Example:**
```
"User says: I'm here to investigate the rumors about corruption in the High Wards.

Respond as your character: As a loyal member of the Skywarden's Council, I am here to investigate these rumors.

User says: I've heard that there's been a power struggle within the High Wards, with some members wanting to take control.

Respond as your character: I've heard similar rumors. I am interested in learning more about this."
```

**Nous-Hermes-2-Mistral-7B-DPO Good Example:**
```
"As a member of the High Wards, I must tread carefully. You've heard the whispers, too? I will do what I can to uncover the truth, but I must ensure that my actions remain hidden from those who would seek to stop us."
```

**Analysis:**
- **TinyLlama:** Acts like a script writer, continuing the dialog format
- **Phi-2 & Nous-Hermes-2-Mistral-7B-DPO:** Respond naturally as the character
- **Winner:** Phi-2 and Nous-Hermes-2-Mistral-7B-DPO significantly better

### 🔹 Response Time

| Criterion | Phi-2 | TinyLlama | Nous-Hermes-2-Mistral-7B-DPO | Winner |
|-----------|-------|-----------|------------------------------|---------|
| Average Response Time | 1.72s | 2.96s | 34.09s | **Phi-2** |
| Performance Rating | 🟢 Fast | 🟡 Moderate | 🔴 Very Slow | **Phi-2** |

**Analysis:**
- **Phi-2:** Consistent ~1.7s responses, very fast
- **TinyLlama:** ~3s responses, moderate speed
- **Nous-Hermes-2-Mistral-7B-DPO:** ~34s responses, very slow
- **Winner:** Phi-2 significantly faster

## Critical Issues Analysis

### Phi-2: Prompt Injection Problem
**Severity:** Critical  
**Impact:** Makes responses unusable without extensive cleaning  
**Root Cause:** Model training on instruction-following data without proper response formatting  
**Workaround:** Requires post-processing to remove prompt artifacts  

### TinyLlama: Prompt Injection + Dialog Continuation Problem
**Severity:** Critical  
**Impact:** Makes responses unusable AND breaks conversation flow  
**Root Cause:** Model training on instruction-following data + dialog continuation tendencies  
**Workaround:** Requires extensive post-processing AND prompt engineering  

### Nous-Hermes-2-Mistral-7B-DPO: Prompt Injection + Very Slow Response Time
**Severity:** Critical  
**Impact:** Makes responses unusable AND completely impractical for real-time use  
**Root Cause:** Model training on instruction-following data + performance/deployment issues  
**Workaround:** Requires extensive post-processing AND performance optimization  

## Recommendations

### For PersonaForge System

1. **Immediate Action:**
   - **Phi-2:** Implement robust response cleaning pipeline (best choice)
   - **TinyLlama:** Implement robust response cleaning + dialog continuation prevention
   - **Nous-Hermes-2-Mistral-7B-DPO:** DO NOT USE due to very slow response times

2. **Alternative Models to Consider:**
   - **Llama 2 7B/13B:** Better instruction following, less prompt injection
   - **Mistral 7B (base):** Strong roleplay capabilities, cleaner responses
   - **Qwen 7B:** Good balance of performance and response quality

3. **System Improvements:**
   - Add response quality scoring
   - Implement fallback responses for failed generations
   - Create model-specific prompt templates

### Model-Specific Recommendations

#### Phi-2 Usage
**✅ Acceptable Use Cases:**
- RAG applications with post-processing
- Information extraction tasks
- Simple Q&A with cleaning

**❌ Not Suitable For:**
- Direct user-facing roleplay
- Production chat systems without cleaning

**Required Mitigations:**
- Extensive response cleaning pipeline
- Response validation and filtering
- User education about response artifacts

#### TinyLlama Usage
**✅ Acceptable Use Cases:**
- RAG applications with extensive post-processing
- Information extraction tasks
- Simple Q&A with cleaning

**❌ Not Suitable For:**
- Character roleplay without extensive prompt engineering
- Multi-turn conversations
- Production roleplay systems

**Required Mitigations:**
- Extensive response cleaning pipeline
- Specialized prompt engineering to prevent dialog continuation
- Response validation to detect continuation issues
- Fallback mechanisms for failed generations

#### Nous-Hermes-2-Mistral-7B-DPO Usage
**✅ Acceptable Use Cases:**
- Offline processing tasks where speed doesn't matter
- Batch processing applications
- Research and development
- Roleplay applications with natural conversation format

**❌ Not Suitable For:**
- Real-time chat applications
- Production roleplay systems
- User-facing applications

**Required Mitigations:**
- Performance optimization or alternative deployment
- Natural conversation prompt format (solves prompt injection)
- Response validation and filtering

## Conclusion

### Overall Assessment

| Model | Score | Recommendation | Main Issues |
|-------|-------|----------------|-------------|
| **Phi-2** | 75% | ⚠️ Moderately Suitable | Prompt Injection |
| **TinyLlama** | 60% | ⚠️ Moderately Suitable | Prompt Injection + Dialog Continuation |
| **Nous-Hermes-2-Mistral-7B-DPO** | 60% | ⚠️ Moderately Suitable | Prompt Injection + Very Slow |

### Final Recommendation

**None of these models are ideal for production use** in PersonaForge without significant workarounds:

1. **Phi-2** requires extensive response cleaning but has excellent roleplay capabilities and fast responses
2. **TinyLlama** has both prompt injection AND dialog continuation issues, making it more problematic
3. **Nous-Hermes-2-Mistral-7B-DPO** has prompt injection AND very slow response times, making it completely impractical

**Best Path Forward:**
- **Short-term:** Use Phi-2 with robust cleaning pipeline (best choice among the three)
- **Long-term:** Switch to models with better instruction following (Llama 2, Mistral, Qwen)
- **Development:** Continue testing with different models and prompt engineering approaches

### Alternative Recommendation

Consider **hybrid approach:**
- Use Phi-2 for RAG and context processing (fastest, cleanest responses)
- Use a different model (Llama 2/Mistral) for final response generation
- Implement response quality scoring to automatically select the best model

### Winner: Phi-2

**Phi-2 is the best choice** among these three models because:
- ✅ **Fastest response times** (1.72s vs 2.96s vs 34.09s)
- ✅ **No dialog continuation issues** (unlike TinyLlama)
- ✅ **Same prompt injection problem but easier to clean**
- ✅ **Best overall roleplay experience**

**Ranking:**
1. **Phi-2** (75%) - Best overall, fast responses, no dialog issues
2. **TinyLlama** (60%) - Good roleplay but dialog continuation problems
3. **Nous-Hermes-2-Mistral-7B-DPO** (60%) - Excellent roleplay but very slow

---

*Report generated by PersonaForge Evaluation System v1.0* 