from fastapi import FastAPI


app = FastAPI()


# get
@app.get("/")
def read_root():
    return {"message": "HelloWorld"}


# post
@app.post("/plans")
async def plans(plans: Plan):
    return {"plans": plans}

@app.post("/spots")
async def spots(spots: Spot):
    return {"spots": spots}

@app.post("/memos")
async def memos(memos: Memo):
    return {"memos": memos}
