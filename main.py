import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Configuración del cliente OpenAI
openai.api_key = "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"

app = FastAPI()

# Modelos de entrada
class HeaderRequest(BaseModel):
    extracted_text: str
    po: str
    shipto_postal_code: str
    billto_postal_code: str

class ItemsRequest(BaseModel):
    extracted_text: str

# Funciones auxiliares
def gpt_service_header(extracted_text, po, shipto_postal_code, billto_postal_code):
    messages = [
        {
            "role": "system",
            "content": (
                f"Del siguiente texto extraido a partir de una Orden de Compra: {extracted_text} "
                "Podrías regresar de manera estructurada los datos de PONumber, Vendor, Bill To, Ship To, "
                "estructurando el Name, Address, City, State, and PostalCode en un JSON en inglés."
            )
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

def gpt_service_items(extracted_text):
    messages = [
        {
            "role": "system",
            "content": (
                f"Del siguiente texto extraido a partir de una Orden de Compra: {extracted_text} "
                "Podrías regresar de manera estructurada los datos de los ítems en un JSON en inglés con la "
                "siguiente estructura: ItemNumber, PartNumber, Name or Description, DeliveryDate, Quantity, UM, UnitPrice, Amount."
            )
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

# Rutas de la API
@app.post("/doc2erp/po/extract/header/")
async def extract_header(data: HeaderRequest):
    try:
        result = gpt_service_header(
            data.extracted_text,
            data.po,
            data.shipto_postal_code,
            data.billto_postal_code
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/doc2erp/po/extract/items/")
async def extract_items(data: ItemsRequest):
    try:
        result = gpt_service_items(data.extracted_text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Punto de entrada
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
