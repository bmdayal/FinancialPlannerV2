# 🔌 API Documentation - Financial Planner AI

Complete REST API reference for the Financial Planner AI system.

## 📋 API Overview

The Financial Planner AI exposes a RESTful API that enables interaction with the Agentic AI system for financial planning. All endpoints return JSON responses and use standard HTTP status codes.

**Base URL**: `http://localhost:5000`  
**Content-Type**: `application/json`  
**Authentication**: Not required (API key handled server-side)

## 🏠 Core Endpoints

### GET `/`
**Description**: Serves the main application interface  
**Method**: `GET`  
**Authentication**: None

**Response**: HTML page with the financial planning interface

**Example**:
```bash
curl -X GET http://localhost:5000/
```

---

### GET `/api/plans`
**Description**: Retrieve available financial planning modules  
**Method**: `GET`  
**Authentication**: None

**Response**:
```json
{
  "plans": [
    "Retirement Planning",
    "Homeownership",
    "Education Savings", 
    "Emergency Fund",
    "Investment Portfolio",
    "Debt Management"
  ]
}
```

**Example**:
```bash
curl -X GET http://localhost:5000/api/plans
```

---

## 🤖 Planning Endpoints

### POST `/api/planning/start`
**Description**: Initialize a new financial planning session with Agentic AI  
**Method**: `POST`  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "age": 32,
  "annual_income": 85000,
  "savings": 45000,
  "selected_plans": [
    "Retirement Planning",
    "Homeownership"
  ]
}
```

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `age` | integer | ✅ | User's current age (18-100) |
| `annual_income` | number | ✅ | Annual gross income in USD |
| `savings` | number | ✅ | Current total savings amount |
| `selected_plans` | array | ✅ | Array of selected planning modules |

**Response** (Success - 200):
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "plan_summaries": {
    "Executive Summary": "Based on your profile...",
    "Retirement Planning": "Your retirement analysis shows...",
    "Homeownership": "For homeownership planning..."
  },
  "user_info": {
    "age": 32,
    "annual_income": 85000,
    "savings": 45000
  }
}
```

**Response** (Error - 400):
```json
{
  "error": "Invalid input data",
  "details": "Age must be between 18 and 100"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/planning/start \
  -H "Content-Type: application/json" \
  -d '{
    "age": 32,
    "annual_income": 85000,
    "savings": 45000,
    "selected_plans": ["Retirement Planning", "Homeownership"]
  }'
```

---

## 💬 Chat Endpoints

### POST `/api/chat/<session_id>`
**Description**: Send a message to the AI advisor for a specific planning session  
**Method**: `POST`  
**Content-Type**: `application/json`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | ✅ | UUID of the planning session |

**Request Body**:
```json
{
  "message": "How much should I save for retirement each month?"
}
```

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | ✅ | User's question or message |

**Response** (Success - 200):
```json
{
  "message": "Based on your retirement plan, I recommend saving $1,063 per month. This breaks down as follows: $850 to your 401(k) to get the full employer match, and $213 to a Roth IRA. This 15% savings rate will help you reach your retirement goal of $1.2M by age 65.",
  "status": "success"
}
```

**Response** (Error - 404):
```json
{
  "error": "Session not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/chat/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How much should I save for retirement?"
  }'
```

---

## 📄 Export Endpoints

### GET `/api/export/<session_id>`
**Description**: Export financial plan as JSON file  
**Method**: `GET`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | ✅ | UUID of the planning session |

**Response** (Success - 200):
```json
{
  "generated_at": "2024-11-15T20:30:00.000Z",
  "user_info": {
    "age": 32,
    "annual_income": 85000,
    "savings": 45000
  },
  "selected_plans": [
    "Retirement Planning",
    "Homeownership"
  ],
  "plan_summaries": {
    "Executive Summary": "...",
    "Retirement Planning": "...",
    "Homeownership": "..."
  }
}
```

**Response Headers**:
```
Content-Type: application/json
Content-Disposition: attachment; filename="financial_plan_20241115.json"
```

**Example**:
```bash
curl -X GET http://localhost:5000/api/export/550e8400-e29b-41d4-a716-446655440000
```

---

### GET `/api/export/<session_id>/pdf`
**Description**: Export financial plan as professionally formatted PDF  
**Method**: `GET`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | ✅ | UUID of the planning session |

**Response** (Success - 200): Binary PDF data

**Response Headers**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="financial_plan_20241115.pdf"
```

**Features**:
- Professional formatting with color-coded sections
- Client information table with financial data highlighting
- Executive summary with visual hierarchy  
- Individual plan sections with structured content
- Financial data presented in formatted tables
- Footer with disclaimers and professional styling

**Example**:
```bash
curl -X GET http://localhost:5000/api/export/550e8400-e29b-41d4-a716-446655440000/pdf \
  --output financial_plan.pdf
```

---

### GET `/api/export/<session_id>/docx`
**Description**: Export financial plan as editable Word document  
**Method**: `GET`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | ✅ | UUID of the planning session |

**Response** (Success - 200): Binary DOCX data

**Response Headers**:
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="financial_plan_20241115.docx"
```

**Features**:
- Rich text formatting with color-coded elements
- Editable content for customization
- Professional table styling for financial data
- Enhanced typography with proper spacing
- Bullet points and structured lists
- Financial data highlighting in blue
- Professional footer and disclaimers

**Example**:
```bash
curl -X GET http://localhost:5000/api/export/550e8400-e29b-41d4-a716-446655440000/docx \
  --output financial_plan.docx
```

---

## 📊 Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request data or parameters |
| 404 | Not Found | Session not found or endpoint doesn't exist |
| 500 | Internal Server Error | Server error or AI processing failure |

## 🔄 Session Management

### Session Lifecycle
1. **Creation**: Sessions are created via `POST /api/planning/start`
2. **Storage**: Session data stored in server memory with UUID identifier
3. **Access**: Sessions accessed via session_id in subsequent requests
4. **Timeout**: Sessions automatically cleaned up after period of inactivity
5. **Cleanup**: No persistent storage; sessions cleared on server restart

### Session Data Structure
```json
{
  "session_id": "uuid-string",
  "user_info": {
    "age": 32,
    "annual_income": 85000,
    "savings": 45000
  },
  "selected_plans": ["plan1", "plan2"],
  "plan_summaries": {
    "Plan Name": "Generated content..."
  },
  "conversation_history": [
    {"role": "user", "content": "Question"},
    {"role": "assistant", "content": "Answer"}
  ]
}
```

## 🚨 Error Handling

### Common Error Responses

**400 Bad Request - Invalid Input**:
```json
{
  "error": "Invalid input data",
  "details": "Age must be a positive integer"
}
```

**404 Not Found - Session Expired**:
```json
{
  "error": "Session not found"
}
```

**500 Internal Server Error - AI Processing**:
```json
{
  "error": "AI processing failed",
  "details": "OpenAI API error"
}
```

### Error Prevention
- Always validate input data before sending requests
- Handle session expiration gracefully in client applications
- Implement retry logic for temporary AI processing failures
- Check session existence before chat or export operations

## 🔧 Request Examples

### Complete Workflow Example

1. **Start Planning Session**:
```bash
SESSION_ID=$(curl -s -X POST http://localhost:5000/api/planning/start \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "annual_income": 75000,
    "savings": 30000,
    "selected_plans": ["Retirement Planning", "Emergency Fund"]
  }' | jq -r '.session_id')

echo "Session ID: $SESSION_ID"
```

2. **Ask Questions**:
```bash
curl -X POST http://localhost:5000/api/chat/$SESSION_ID \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How much emergency fund do I need?"
  }' | jq '.message'
```

3. **Export as PDF**:
```bash
curl -X GET http://localhost:5000/api/export/$SESSION_ID/pdf \
  --output my_financial_plan.pdf
```

### JavaScript/Fetch Examples

**Start Planning**:
```javascript
const planningData = {
  age: 28,
  annual_income: 65000,
  savings: 20000,
  selected_plans: ['Retirement Planning', 'Homeownership']
};

const response = await fetch('/api/planning/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(planningData)
});

const result = await response.json();
const sessionId = result.session_id;
```

**Send Chat Message**:
```javascript
const chatResponse = await fetch(`/api/chat/${sessionId}`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What investment allocation do you recommend?'
  })
});

const chatResult = await chatResponse.json();
console.log(chatResult.message);
```

**Download PDF**:
```javascript
const downloadLink = document.createElement('a');
downloadLink.href = `/api/export/${sessionId}/pdf`;
downloadLink.download = `financial_plan_${new Date().getTime()}.pdf`;
downloadLink.click();
```

## 🔐 Security Considerations

### Data Protection
- **No Authentication Required**: API designed for demo/development use
- **Memory-Only Storage**: No persistent user data storage
- **API Key Security**: OpenAI API key stored server-side only
- **Input Sanitization**: All inputs validated and sanitized
- **Session Isolation**: Each session is completely isolated

### Rate Limiting
- **OpenAI API**: Subject to OpenAI's rate limits
- **Server Resources**: Memory-based session storage has natural limits
- **Concurrent Sessions**: Multiple users supported simultaneously

### Production Recommendations
For production deployment, consider implementing:
- User authentication and authorization
- API rate limiting per user/IP
- Persistent session storage (Redis)
- Request logging and monitoring
- HTTPS/TLS encryption
- Input validation middleware
- Error response sanitization

---

This API provides a complete interface to the Agentic AI Financial Planning system, enabling integration with frontend applications, mobile apps, or other services.