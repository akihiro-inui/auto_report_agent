# Deployment
```bash
az deployment group create --resource-group ${RESOURCE_GROUP_NAME} --template-file deployment/main.bicep
```


# How to run MCP Server locally
```bash
uvicorn backend.src.services.mcp_service:app --host 127.0.0.1 --port 8000
```

# How to test MCP Client locally
```bash
python backend/src/services/llm_service.py
```
