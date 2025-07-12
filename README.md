# OFDA Backend Challenge

Este projeto é uma solução para o desafio técnico da Belvo, focado na extração de dados financeiros através de uma API.

A proposta é construir um serviço robusto, resiliente e de fácil manutenção, capaz de:
- Criar dinamicamente clientes e consentimentos.
- Lidar com instabilidade da API externa (erros 504).
- Armazenar dados temporários em cache.
- Normalizar as informações obtidas e entregar uma resposta clara e padronizada.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI**
- **Pydantic**
- **Requests**
- **Tenacity** – para retry automático com backoff exponencial.
- **Cachetools** – para armazenamento em memória com TTL.

---

## 📂 Estrutura do Projeto

```
app/
├── api/                      # Rotas e controllers (FastAPI)
│   └── api.py
├── services/                 # Regras de negócio
│   └── extract_service.py
├── clients/                  # Comunicação com a API externa (/dynamic-client, /consent)
│   ├── dynamic_client.py
│   └── consents.py
├── extractors/               # Coleta dados de contas, saldo e transações
│   └── extractor.py
├── normalizers/              # Converte dados crus em objetos Pydantic
│   └── normalizer.py
├── schemas/                  # Modelos Pydantic usados como entrada e saída
│   └── request.py
├── core/                     # Utilitários compartilhados
│   ├── cache.py
│   └── retry_utils.py
```

---

## ⚙️ Como Rodar

1. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

2. **Execute a aplicação:**

```bash
uvicorn app.api.api:app --reload --port 8001
```

3. **Faça uma requisição para o endpoint de extração:**

```http
POST /extract-financial-data
Content-Type: application/json
```

```json
{
  "name": "Meu App",
  "organization_name": "Minha Organização",
  "organization_id": "123",
  "user_document_number": "00011122233"
}
```

---

## 🧠 Estratégias Adotadas

### ✅ Cache com TTL

- Tokens do `dynamic_client` e `consent` são armazenados usando `cachetools.TTLCache`.
- Isso evita requisições desnecessárias e melhora a performance.

### ✅ Retry automático com backoff exponencial

- Toda chamada instável à API externa usa a biblioteca `tenacity`.
- Em caso de falha (ex: 504), a requisição é automaticamente reexecutada com espera crescente entre tentativas.

### ✅ Normalização de dados

- Os dados extraídos são convertidos em objetos Pydantic, com os campos essenciais, formatados e padronizados.
- A resposta final tem campos de controle como `summary`, número total de transações, contas, tempo de execução, etc.

### ✅ Código modular e de fácil manutenção

- Cada componente tem responsabilidade única.
- As camadas de extração, cache, normalização, serviço e comunicação externa estão bem separadas.

---

## 🧪 Exemplo de Resposta

```json
{
  "user_document": "00011122233",
  "extraction_date": "2025-07-12T13:02:06.320Z",
  "accounts": [
    {
      "account_id": "abc123",
      "account_type": "checking",
      "balance": {
        "ammount": 1000.0,
        "currency": "BRL"
      },
      "transactions": [
        {
          "transaction_id": "tx1",
          "transaction_type": "deposit",
          "transaction_status": "completed",
          "ammount": 1000.0,
          "currency": "BRL",
          "direction": "in",
          "description": "Transferência",
          "date": "2025-07-11T13:00:00.000Z"
        }
      ]
    }
  ],
  "summary": {
    "total_accounts": 1,
    "total_transactions": 1,
    "processing_time_ms": 273,
    "errors": []
  }
}
```

---

## 🤖 Apoio de IA

Durante o desenvolvimento deste projeto, utilizei inteligência artificial (ChatGPT) como **assistente técnico e revisora de decisões**. A IA ajudou a:

- Validar ideias de estrutura e separação de responsabilidades
- Sugerir boas práticas com bibliotecas como `tenacity` e `cachetools`
- Identificar melhorias de legibilidade e organização
- Apoiar na criação deste README

> Todo o código foi implementado por mim, com decisões conscientes e adaptação às necessidades do desafio.  
> A IA foi usada como parceira de raciocínio, não como substituta de execução. 😉

---

## 📌 Considerações Finais

- O projeto foi desenvolvido com foco em clareza, manutenibilidade e resiliência.
- O uso do Pydantic foi essencial tanto na entrada quanto na saída para garantir consistência.
- O retry e o cache tornam o sistema robusto frente a falhas externas e idempotente sempre que possível.
