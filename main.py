from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from blockchain import Blockchain

app = FastAPI()
blockchain = Blockchain()

# Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Data model for certificate submission
class Certificate(BaseModel):
    student: str
    course: str
    grade: str

# Route: UI page
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route: Add certificate
@app.post("/add_certificate")
async def add_certificate(cert: Certificate):
    index = blockchain.add_certificate(cert.student, cert.course, cert.grade)
    return {"message": f"Certificate will be added to Block {index}"}

# Route: Mine block
@app.get("/mine_block")
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    return {"message": "Block mined successfully!", "block": block}

# Route: Get chain
@app.get("/get_chain")
def get_chain():
    return {"chain": blockchain.chain, "length": len(blockchain.chain)}

# Route: Validate chain
@app.get("/is_valid")
def is_valid():
    return {"valid": blockchain.is_chain_valid(blockchain.chain)}
