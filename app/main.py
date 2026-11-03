from fastapi import FastAPI

from app.routes import orders, products

app = FastAPI(
    title="E-Commerce API prd new version",
    version="1.0.0"
)


app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {
        "application": "E-Commerce API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

def calculate_discount(price, discount):
    if price < 0:
        raise ValueError("Invalid price")

    if not 0 <= discount <= 100:
        raise ValueError("Invalid discount")

    return price - (price * discount / 100)
