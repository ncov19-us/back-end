import uvicorn
from api.app import create_app
from api.config import DevelopmentConfig, ProductionConfig

app = create_app(config_object=DevelopmentConfig)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=DevelopmentConfig.SERVER_PORT,
        log_level="info",
        reload=True,
    )
