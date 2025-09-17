# 🎨 UI Features Documentation

## Model Selection & Configuration

The AI Task Planner now includes a comprehensive model selection and configuration interface that allows users to easily switch between different LLM providers and models directly from the web interface.

### 🚀 Key Features

#### 1. **Model Settings Modal**
- **Access**: Click the "⚙️ Model Settings" button in the header
- **Provider Selection**: Choose between OpenAI (cloud) and Ollama (local)
- **Model Selection**: Pick from available models for each provider
- **API Key Management**: Secure input and validation for OpenAI API keys
- **Real-time Status**: View current configuration and connection status

#### 2. **Supported Providers**

##### **OpenAI (Cloud-based)**
- **GPT-4**: Most capable model for complex tasks
- **GPT-4 Turbo**: Faster version of GPT-4
- **GPT-3.5 Turbo**: Fast and efficient for most tasks
- **GPT-3.5 Turbo 16K**: Extended context version

##### **Ollama (Local)**
- **Llama2**: Meta's open-source model
- **CodeLlama**: Code-specialized Llama model
- **Mistral**: Efficient open-source model
- **Llama2 7B/13B**: Different sizes of Llama2

#### 3. **API Key Management**
- **Secure Input**: Password-masked API key field
- **Real-time Validation**: Test API keys before saving
- **Status Feedback**: Clear success/error messages
- **Auto-save**: Keys are saved when switching providers

### 🔧 How to Use

#### **Step 1: Open Model Settings**
1. Navigate to http://localhost:8000
2. Click the "⚙️ Model Settings" button in the top-right header
3. The modal will open with current configuration

#### **Step 2: Choose Provider**
1. Select either "OpenAI" or "Ollama" radio button
2. The model dropdown will update automatically
3. For OpenAI, the API key field will appear

#### **Step 3: Configure Settings**
1. **For OpenAI**:
   - Enter your API key (starts with "sk-")
   - Click "Validate" to test the key
   - Select your preferred model
   
2. **For Ollama**:
   - Ensure Ollama is running locally
   - Select your preferred model
   - No API key required

#### **Step 4: Test & Save**
1. Click "Test Connection" to verify everything works
2. Click "Save & Apply" to apply the settings
3. The header will update to show the new configuration

### 🛠️ API Endpoints

The UI features are backed by several new API endpoints:

#### **GET /api/llm/models**
Returns available models for each provider.

```json
{
  "openai": [
    {"id": "gpt-4", "name": "GPT-4", "description": "Most capable model"},
    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient"}
  ],
  "ollama": [
    {"id": "llama2:latest", "name": "Llama2", "description": "Meta's Llama2 model"},
    {"id": "mistral:latest", "name": "Mistral", "description": "Efficient open-source model"}
  ]
}
```

#### **POST /api/llm/switch**
Switch LLM provider and model.

```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "api_key": "sk-your-api-key-here"
}
```

#### **POST /api/llm/validate-key**
Validate OpenAI API key.

```json
{
  "api_key": "sk-your-api-key-here"
}
```

#### **GET /api/llm/info**
Get current LLM configuration.

```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "api_key_configured": true,
  "status": "configured"
}
```

#### **POST /api/llm/test**
Test current LLM connection.

### 🎯 Use Cases

#### **For OpenAI Users**
1. **Quick Setup**: Enter API key and start using immediately
2. **Model Comparison**: Test different GPT models for your tasks
3. **Cost Optimization**: Switch between GPT-4 and GPT-3.5 based on complexity

#### **For Ollama Users**
1. **Privacy-First**: Keep all processing local
2. **Offline Capability**: Work without internet connection
3. **Model Experimentation**: Try different local models easily

#### **For Developers**
1. **API Integration**: Use the REST endpoints in your own applications
2. **Automation**: Switch models programmatically based on task requirements
3. **Testing**: Validate configurations before deployment

### 🔒 Security Features

- **API Key Protection**: Keys are masked in the UI
- **Validation**: Keys are tested before saving
- **Session Management**: Keys persist only for the current session
- **Error Handling**: Clear feedback for invalid configurations

### 🚨 Troubleshooting

#### **Common Issues**

1. **"API key is invalid"**
   - Check that your OpenAI API key is correct
   - Ensure you have credits in your OpenAI account
   - Try regenerating the API key

2. **"Ollama model not found"**
   - Ensure Ollama is running: `ollama serve`
   - Pull the model: `ollama pull model-name`
   - Check model availability: `ollama list`

3. **"Connection test failed"**
   - Verify your internet connection (for OpenAI)
   - Check Ollama is running (for local models)
   - Try switching to a different model

#### **Debug Steps**

1. **Check Status**: Look at the "Current Status" section in the modal
2. **Test Connection**: Use the "Test Connection" button
3. **Check Logs**: Look at the browser console for errors
4. **API Testing**: Use the test script: `python test_ui_features.py`

### 📱 Mobile Support

The model settings modal is fully responsive and works on:
- Desktop browsers
- Tablet devices
- Mobile phones
- Touch interfaces

### 🔄 Future Enhancements

Planned features for future releases:
- **Model Performance Metrics**: Show speed and accuracy comparisons
- **Custom Model Support**: Add support for custom Ollama models
- **Batch Testing**: Test multiple models simultaneously
- **Configuration Profiles**: Save and load different configurations
- **Usage Analytics**: Track model usage and costs

---

## 🎉 Getting Started

1. **Start the application**: `./activate_and_run.sh`
2. **Open the web interface**: http://localhost:8000
3. **Click "⚙️ Model Settings"** in the header
4. **Configure your preferred model** and start planning!

For more information, see the [main README](../README.md) or [API documentation](API_REFERENCE.md).
