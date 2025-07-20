from app.database import engine
from app import models


print("creating tables...")
models.Base.metadata.create_all(bind=engine)
print("tables created")