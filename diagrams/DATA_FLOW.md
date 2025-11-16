# 📊 Data Flow Diagrams - Financial Planner AI

Detailed data flow and interaction diagrams for the Agentic AI Financial Planning System.

## 🔄 User Interaction Flow

```mermaid
flowchart TB
    A[User Opens Application] --> B[Load Homepage]
    B --> C[Display Financial Goals Form]
    C --> D{User Selects Goals}
    D --> E[Fill Personal Information]
    E --> F[Submit Planning Request]
    
    F --> G[Show Loading Animation]
    G --> H[AI Processes Request]
    H --> I[Display Generated Plans]
    
    I --> J{User Actions}
    J -->|Ask Question| K[Chat with AI Advisor]
    J -->|Download Plan| L[Export to PDF/DOCX]
    J -->|Modify Goals| M[Return to Form]
    
    K --> N[AI Responds with Context]
    N --> O[Update Chat History]
    O --> J
    
    L --> P[Generate Document]
    P --> Q[Download File]
    Q --> J
    
    M --> C
    
    style A fill:#e3f2fd
    style H fill:#fff3e0
    style N fill:#e8f5e8
    style P fill:#fce4ec
```

## 🤖 Agentic AI Processing Pipeline

```mermaid
sequenceDiagram
    participant User as User Browser
    participant API as Flask API
    participant Router as Agent Router
    participant Ret as Retirement Agent
    participant Home as Homeownership Agent
    participant Edu as Education Agent
    participant AI as OpenAI GPT-4
    participant Doc as Document Engine
    
    User->>API: POST /api/planning/start
    Note over User,API: User data + selected goals
    
    API->>Router: Initialize Multi-Agent Session
    Router->>Router: Determine Required Agents
    
    par Parallel Agent Processing
        Router->>Ret: Process Retirement Planning
        Ret->>AI: Specialized Retirement Prompts
        AI-->>Ret: Retirement Recommendations
        
        Router->>Home: Process Homeownership Planning  
        Home->>AI: Specialized Housing Prompts
        AI-->>Home: Housing Recommendations
        
        Router->>Edu: Process Education Planning
        Edu->>AI: Specialized Education Prompts
        AI-->>Edu: Education Recommendations
    end
    
    Router->>Router: Coordinate All Agent Results
    Router->>AI: Generate Executive Summary
    AI-->>Router: Integrated Financial Plan
    
    Router-->>API: Complete Financial Strategy
    API-->>User: JSON Response with Plans
    
    Note over User: User can now chat or export
    
    User->>API: POST /api/chat/{session}
    API->>Router: Retrieve Session Context
    Router->>AI: Context-Aware Chat Request
    AI-->>Router: Personalized Response
    Router-->>API: Chat Answer
    API-->>User: JSON Chat Response
    
    User->>API: GET /api/export/{session}/pdf
    API->>Doc: Generate PDF Document
    Doc->>Doc: Apply Professional Formatting
    Doc-->>API: PDF Binary Data
    API-->>User: PDF Download
```

## 📋 Data Structure Flow

```mermaid
graph TB
    subgraph "Input Data Structure"
        A[User Profile] --> A1[Age: number]
        A --> A2[Annual Income: currency]
        A --> A3[Current Savings: currency]
        A --> A4[Selected Goals: array]
    end
    
    subgraph "Processing Layer"
        B[Session Management] --> B1[Generate UUID]
        B1 --> B2[Store User Data]
        B2 --> B3[Initialize Agent Context]
        
        C[Agent Routing] --> C1[Parse Selected Goals]
        C1 --> C2[Instantiate Required Agents]
        C2 --> C3[Prepare Specialized Prompts]
    end
    
    subgraph "AI Processing"
        D[LangChain Framework] --> D1[Context Management]
        D1 --> D2[Prompt Engineering]
        D2 --> D3[OpenAI API Calls]
        D3 --> D4[Response Processing]
    end
    
    subgraph "Output Data Structure"
        E[Financial Plan] --> E1[Executive Summary: text]
        E --> E2[Individual Plans: object]
        E --> E3[Session ID: string]
        E --> E4[Chat History: array]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#fce4ec
```

## 🔗 API Request/Response Flow

### Planning Request Flow

```mermaid
graph LR
    A[POST /api/planning/start] --> B{Validate Input}
    B -->|Valid| C[Create Session]
    B -->|Invalid| D[Return Error 400]
    
    C --> E[Route to Agents]
    E --> F[Process with AI]
    F --> G[Generate Plans]
    G --> H[Store in Session]
    H --> I[Return JSON Response]
    
    D --> Z[Error Response]
    I --> J[Success Response]
    
    subgraph "Response Structure"
        J --> J1[session_id]
        J --> J2[plan_summaries]
        J --> J3[status: success]
    end
    
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style F fill:#e3f2fd
    style Z fill:#ffebee
```

### Chat Request Flow

```mermaid
graph LR
    A[POST /api/chat/{session}] --> B{Session Exists?}
    B -->|No| C[Return Error 404]
    B -->|Yes| D[Retrieve Context]
    
    D --> E[Build Chat Prompt]
    E --> F[Include Conversation History]
    F --> G[Include Plan Context]
    G --> H[Send to OpenAI]
    H --> I[Process Response]
    I --> J[Update Chat History]
    J --> K[Return JSON Response]
    
    C --> Z[Session Not Found]
    K --> L[Chat Success]
    
    subgraph "Chat Context"
        F --> F1[Previous Messages]
        G --> G1[User Profile]
        G --> G2[Generated Plans]
    end
    
    style B fill:#fff3e0
    style H fill:#e3f2fd
    style I fill:#e8f5e8
    style Z fill:#ffebee
```

## 📄 Document Export Flow

### PDF Generation Pipeline

```mermaid
graph TB
    A[Export Request] --> B[Retrieve Session Data]
    B --> C[Extract Plan Content]
    C --> D[Clean Text Content]
    D --> E[Structure Content Sections]
    
    E --> F[ReportLab Processing]
    F --> G[Apply Professional Styling]
    G --> H[Create Document Elements]
    
    subgraph "Document Elements"
        H --> H1[Title & Header]
        H --> H2[Client Information Table]
        H --> H3[Executive Summary]
        H --> H4[Individual Plan Sections]
        H --> H5[Financial Data Tables]
        H --> H6[Footer & Disclaimers]
    end
    
    H1 --> I[Assemble PDF]
    H2 --> I
    H3 --> I
    H4 --> I
    H5 --> I
    H6 --> I
    
    I --> J[Generate Binary Data]
    J --> K[Set Response Headers]
    K --> L[Return PDF Download]
    
    style F fill:#e3f2fd
    style G fill:#fff3e0
    style I fill:#e8f5e8
    style L fill:#fce4ec
```

### DOCX Generation Pipeline

```mermaid
graph TB
    A[Export Request] --> B[Retrieve Session Data]
    B --> C[Process Content Structure]
    C --> D[Apply Rich Text Formatting]
    
    D --> E[python-docx Processing]
    E --> F[Create Document Structure]
    F --> G[Apply Styling]
    
    subgraph "DOCX Elements"
        G --> G1[Title with Color Coding]
        G --> G2[Client Info Table with Styling]
        G --> G3[Formatted Text Sections]
        G --> G4[Bullet Points & Lists]
        G --> G5[Financial Data Highlighting]
        G --> G6[Professional Footer]
    end
    
    G1 --> H[Assemble DOCX]
    G2 --> H
    G3 --> H
    G4 --> H
    G5 --> H
    G6 --> H
    
    H --> I[Generate Binary Data]
    I --> J[Set Response Headers]
    J --> K[Return DOCX Download]
    
    style E fill:#e3f2fd
    style F fill:#fff3e0
    style H fill:#e8f5e8
    style K fill:#fce4ec
```

## 🧠 AI Agent Coordination Flow

### Multi-Agent Processing

```mermaid
graph TB
    A[User Request with Multiple Goals] --> B[Agent Router Analysis]
    
    B --> C{Determine Required Agents}
    C -->|Retirement Selected| D[Retirement Agent]
    C -->|Homeownership Selected| E[Homeownership Agent]
    C -->|Education Selected| F[Education Agent]
    C -->|Emergency Fund Selected| G[Emergency Agent]
    C -->|Investment Selected| H[Investment Agent]
    C -->|Debt Management Selected| I[Debt Agent]
    
    subgraph "Parallel Processing"
        D --> D1[Retirement Analysis]
        E --> E1[Housing Analysis]
        F --> F1[Education Analysis]
        G --> G1[Emergency Planning]
        H --> H1[Investment Strategy]
        I --> I1[Debt Elimination]
    end
    
    D1 --> J[Agent Coordination Layer]
    E1 --> J
    F1 --> J
    G1 --> J
    H1 --> J
    I1 --> J
    
    J --> K[Identify Synergies & Conflicts]
    K --> L[Optimize Resource Allocation]
    L --> M[Create Integrated Timeline]
    M --> N[Generate Executive Summary]
    
    N --> O[Return Coordinated Plan]
    
    style B fill:#e3f2fd
    style J fill:#fff3e0
    style K fill:#e8f5e8
    style N fill:#fce4ec
```

### Agent Context Management

```mermaid
sequenceDiagram
    participant Router as Agent Router
    participant Context as Context Manager
    participant Agent1 as Agent 1
    participant Agent2 as Agent 2
    participant AI as OpenAI API
    
    Router->>Context: Initialize Session Context
    Context->>Context: Store User Profile
    Context->>Context: Store Selected Goals
    
    Router->>Agent1: Assign Task with Context
    Agent1->>Context: Retrieve User Data
    Context-->>Agent1: User Profile + History
    
    Agent1->>AI: Send Contextualized Prompt
    AI-->>Agent1: Specialized Response
    Agent1->>Context: Store Agent Results
    
    Router->>Agent2: Assign Task with Context
    Agent2->>Context: Retrieve User Data + Agent1 Results
    Context-->>Agent2: Enhanced Context
    
    Agent2->>AI: Send Enhanced Prompt
    AI-->>Agent2: Coordinated Response
    Agent2->>Context: Store Final Results
    
    Router->>Context: Retrieve All Results
    Context-->>Router: Complete Plan Data
    Router->>Router: Generate Executive Summary
```

## 💾 Session Management Flow

### Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> SessionCreated: User Starts Planning
    SessionCreated --> ActivePlanning: Processing Request
    ActivePlanning --> PlanGenerated: AI Completes Plans
    
    PlanGenerated --> ChatActive: User Asks Questions
    PlanGenerated --> ExportGenerated: User Downloads
    PlanGenerated --> SessionTimeout: No Activity
    
    ChatActive --> PlanGenerated: Continue Planning
    ChatActive --> SessionTimeout: Inactivity
    
    ExportGenerated --> PlanGenerated: Continue Session
    ExportGenerated --> SessionEnd: User Leaves
    
    SessionTimeout --> SessionCleanup: Auto Cleanup
    SessionEnd --> SessionCleanup: Manual End
    SessionCleanup --> [*]: Memory Released
    
    note right of SessionCreated
        Store:
        - User Profile
        - Selected Goals
        - Session UUID
    end note
    
    note right of PlanGenerated
        Store:
        - Generated Plans
        - Chat History
        - Export Ready
    end note
```

### Memory Management

```mermaid
graph TB
    A[Session Start] --> B[Allocate Memory]
    B --> C[Store User Data]
    C --> D[Process AI Requests]
    D --> E[Accumulate Results]
    
    E --> F{Session Active?}
    F -->|Yes| G[Continue Processing]
    F -->|No| H[Cleanup Timer Start]
    
    G --> D
    H --> I[Release Memory]
    I --> J[Remove Session Data]
    J --> K[Session End]
    
    subgraph "Memory Contents"
        L[User Profile Data]
        M[Generated Plans]
        N[Conversation History]
        O[Temporary Variables]
    end
    
    C --> L
    E --> M
    E --> N
    D --> O
    
    I --> P[Clear All Data]
    P -.-> L
    P -.-> M
    P -.-> N
    P -.-> O
    
    style A fill:#e3f2fd
    style F fill:#fff3e0
    style I fill:#ffebee
    style K fill:#e8f5e8
```

## 🔒 Security Data Flow

### Data Protection Pipeline

```mermaid
graph TB
    A[User Input] --> B[Input Validation]
    B --> C[Sanitize Data]
    C --> D[Memory-Only Storage]
    
    D --> E[AI Processing]
    E --> F[Response Filtering]
    F --> G[Output Sanitization]
    
    G --> H[Client Response]
    
    subgraph "Security Layers"
        B --> B1[XSS Prevention]
        B --> B2[Injection Prevention]
        C --> C1[Data Cleaning]
        F --> F1[Sensitive Data Removal]
        G --> G1[Safe Output Formatting]
    end
    
    subgraph "External API Security"
        I[API Key Management] --> J[Server-Side Only]
        J --> K[Encrypted Storage]
        K --> L[Rate Limiting]
    end
    
    E --> I
    
    style B fill:#ffebee
    style C fill:#fff3e0
    style D fill:#e3f2fd
    style G fill:#e8f5e8
```

---

These diagrams illustrate the comprehensive data flow and interaction patterns within the Financial Planner AI system, showcasing the sophisticated Agentic AI architecture powered by LangChain and OpenAI.