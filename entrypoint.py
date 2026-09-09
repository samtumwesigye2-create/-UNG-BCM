from app import app
from recovery_kpis import router as recovery_kpis_router
app.include_router(recovery_kpis_router)
