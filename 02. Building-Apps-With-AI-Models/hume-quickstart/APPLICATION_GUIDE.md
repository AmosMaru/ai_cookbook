# Hume Empathic Voice Interface (EVI) Application Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Key Technologies](#key-technologies)
5. [Setup and Installation](#setup-and-installation)
6. [Environment Configuration](#environment-configuration)
7. [Application Flow](#application-flow)
8. [Component Breakdown](#component-breakdown)
9. [Features](#features)
10. [API Integration](#api-integration)
11. [Styling and UI](#styling-and-ui)
12. [Development Workflow](#development-workflow)
13. [Deployment](#deployment)
14. [Troubleshooting](#troubleshooting)

## Overview

This application is a **Next.js-based implementation** of Hume AI's **Empathic Voice Interface (EVI)**, which enables real-time voice conversations with an AI that can detect and respond to emotional cues in speech. The application provides a chat interface where users can have voice conversations with an emotionally-aware AI assistant.

### What makes this special?
- **Emotion Detection**: Analyzes emotional expressions in real-time during voice conversations
- **Empathic Responses**: AI responds with emotional awareness and context
- **Real-time Communication**: WebSocket-based voice streaming for instant interactions
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS

## Architecture

The application follows a **client-server architecture** with the following layers:

```
Frontend (Next.js) → Hume Voice React SDK → Hume API → AI Model
     ↓                     ↓                  ↓           ↓
  UI Components      WebSocket Connection   Auth & API   EVI Engine
```

### Key Architectural Decisions:
- **Next.js Pages Router**: Server-side rendering for authentication
- **Component-based React**: Modular UI components for maintainability
- **Real-time WebSocket**: Low-latency voice communication
- **Server-side Authentication**: Secure token generation on the server

## Project Structure

```
hume-quickstart/
├── components/              # React UI components
│   ├── Chat.tsx            # Main chat container
│   ├── Controls.tsx        # Voice controls (mute, disconnect)
│   ├── Expressions.tsx     # Emotion visualization
│   ├── Messages.tsx        # Message display component
│   ├── MicFFT.tsx         # Microphone visualization
│   ├── Nav.tsx            # Navigation component
│   ├── StartCall.tsx      # Call initiation component
│   ├── logos/             # Logo components
│   └── ui/                # Reusable UI components
├── pages/                  # Next.js pages
│   ├── _app.tsx           # App wrapper
│   ├── _document.tsx      # HTML document structure
│   ├── index.tsx          # Main page with auth
│   └── 500.tsx            # Error page
├── styles/                 # Global styles
├── utils/                  # Utility functions
├── public/                 # Static assets
├── .env                   # Environment variables
└── package.json           # Dependencies and scripts
```

## Key Technologies

### Frontend Stack:
- **Next.js 14.2.3**: React framework with SSR/SSG
- **React 18**: Component-based UI library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions

### Hume AI Integration:
- **@humeai/voice-react**: React SDK for voice interactions
- **hume**: Core Hume AI SDK for authentication

### UI Components:
- **Radix UI**: Accessible component primitives
- **Lucide React**: Icon library
- **class-variance-authority**: Component variant management

### Development Tools:
- **ESLint**: Code linting
- **PostCSS**: CSS processing
- **pnpm**: Fast package manager

## Setup and Installation

### Prerequisites:
- Node.js 18+ installed
- pnpm package manager
- Hume AI account with API access

### Step-by-Step Installation:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hume-quickstart
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your Hume AI credentials.

4. **Run the development server:**
   ```bash
   pnpm run dev
   ```

5. **Open the application:**
   Navigate to `http://localhost:3000`

## Environment Configuration

### Required Environment Variables:

```bash
# .env file
HUME_API_KEY=your_api_key_here
HUME_SECRET_KEY=your_secret_key_here
```

### How to get Hume AI credentials:
1. Visit [Hume AI Platform](https://platform.hume.ai)
2. Log in or create an account
3. Navigate to [API Keys page](https://platform.hume.ai/settings/keys)
4. Generate new API Key and Secret Key
5. Copy credentials to your `.env` file

### Security Notes:
- **Never commit `.env` to version control**
- Environment variables are only accessible on the server
- Access tokens are generated server-side for security

## Application Flow

### Complete Process Flow Diagram

```
1. User navigates to application
   ↓
2. Next.js Server-Side Rendering (pages/index.tsx)
   ↓
3. getServerSideProps() executes
   ↓
4. Server fetches Hume access token
   ↓
5. Page renders with Chat component
   ↓
6. VoiceProvider initializes
   ↓
7. StartCall button displayed (not connected state)
   ↓
8. User clicks "Start Call"
   ↓
9. WebSocket connection established
   ↓
10. Connection status changes to "connected"
    ↓
11. StartCall component hides, Controls component shows
    ↓
12. Microphone access requested
    ↓
13. Real-time voice streaming begins
    ↓
14. Messages displayed with emotion analysis
    ↓
15. User can mute/unmute or end call
```

### Detailed Step-by-Step Process Flow

#### **PHASE 1: Application Initialization**

**Step 1: User Request** 
- User navigates to `http://localhost:3000`
- Browser sends GET request to Next.js server

**Step 2: Server-Side Rendering (`pages/index.tsx`)**
```typescript
export const getServerSideProps = async () => {
  // This runs on the server BEFORE the page is sent to browser
  
  // 1. Check environment variables exist
  if (!process.env.HUME_API_KEY) {
    throw new Error("The HUME_API_KEY environment variable is not set.");
  }
  if (!process.env.HUME_SECRET_KEY) {
    throw new Error("The HUME_SECRET_KEY environment variable is not set.");
  }
  
  // 2. Generate access token using Hume SDK
  try {
    const accessToken = await fetchAccessToken({
      apiKey: String(process.env.HUME_API_KEY),
      secretKey: String(process.env.HUME_SECRET_KEY),
    });

    // 3. Return token as props to client
    return {
      props: {
        accessToken,  // This will be passed to the Page component
      },
    };
  } catch (error) {
    console.error("Failed to fetch access token:", error);
    throw error;  // This will show 500 error page
  }
};
```

**Step 3: Page Component Rendering**
```typescript
export default function Page({ accessToken }: PageProps) {
  return (
    <div className={"grow flex flex-col"}>
      <Chat accessToken={accessToken} />  {/* Pass token to Chat */}
    </div>
  );
}
```

#### **PHASE 2: Client-Side Initialization**

**Step 4: Chat Component Initialization (`components/Chat.tsx`)**
```typescript
export default function ClientComponent({ accessToken }: { accessToken: string }) {
  const timeout = useRef<number | null>(null);
  const ref = useRef<ComponentRef<typeof Messages> | null>(null);

  return (
    <div className={"relative grow flex flex-col mx-auto w-full overflow-hidden h-[0px]"}>
      {/* Initialize VoiceProvider with access token */}
      <VoiceProvider
        onMessage={() => {
          // Auto-scroll setup for new messages
          if (timeout.current) {
            window.clearTimeout(timeout.current);
          }
          timeout.current = window.setTimeout(() => {
            if (ref.current) {
              const scrollHeight = ref.current.scrollHeight;
              ref.current.scrollTo({
                top: scrollHeight,
                behavior: "smooth",
              });
            }
          }, 200);
        }}
      >
        <Messages ref={ref} />     {/* Message display area */}
        <Controls />              {/* Mute/Disconnect controls */}
        <StartCall accessToken={accessToken} />  {/* Connection button */}
      </VoiceProvider>
    </div>
  );
}
```

**Step 5: VoiceProvider Context Setup**
- `VoiceProvider` creates React context for voice state
- Initializes `useVoice` hook with default state:
  ```typescript
  {
    status: { value: "disconnected" },
    messages: [],
    isMuted: false,
    micFft: [],
    connect: function,
    disconnect: function,
    mute: function,
    unmute: function
  }
  ```

#### **PHASE 3: Pre-Connection State**

**Step 6: StartCall Component Display (`components/StartCall.tsx`)**
```typescript
export default function StartCall({ accessToken }: { accessToken: string }) {
  const { status, connect } = useVoice();

  const EVI_CONNECT_OPTIONS: ConnectOptions = {
    auth: { type: "accessToken", value: accessToken },
    configId: "c727d956-e06c-459a-9640-0bc0efa2c159"  // Pre-configured EVI
  };

  return (
    <AnimatePresence>
      {status.value !== "connected" ? (  // Show only when NOT connected
        <motion.div className={"fixed inset-0 p-4 flex items-center justify-center bg-background"}>
          <Button
            onClick={() => {
              connect(EVI_CONNECT_OPTIONS)  // Trigger connection
                .then(() => {})
                .catch(() => {})
                .finally(() => {});
            }}
          >
            <Phone className={"size-4 opacity-50"} />
            <span>Start Call</span>
          </Button>
        </motion.div>
      ) : null}  {/* Hide when connected */}
    </AnimatePresence>
  );
}
```

**Step 7: Controls Component (Hidden State)**
```typescript
export default function Controls() {
  const { disconnect, status, isMuted, unmute, mute, micFft } = useVoice();

  return (
    <div className={"fixed bottom-0 left-0 w-full p-4 flex items-center justify-center"}>
      <AnimatePresence>
        {status.value === "connected" ? (  // Only show when connected
          <motion.div>
            {/* Control buttons will appear here after connection */}
          </motion.div>
        ) : null}  {/* Hidden when disconnected */}
      </AnimatePresence>
    </div>
  );
}
```

#### **PHASE 4: Connection Process**

**Step 8: User Clicks "Start Call"**
- Click event triggers `connect(EVI_CONNECT_OPTIONS)`
- Status changes from "disconnected" → "connecting"

**Step 9: WebSocket Connection Establishment**
```typescript
// Inside Hume SDK (@humeai/voice-react)
connect({
  auth: { type: "accessToken", value: accessToken },
  configId: "c727d956-e06c-459a-9640-0bc0efa2c159"
})
```

**Step 10: Connection State Changes**
- SDK establishes WebSocket connection to `wss://api.hume.ai/v0/evi/chat`
- Authentication happens using the access token
- Status updates: "connecting" → "connected"

**Step 11: UI State Transition**
- `StartCall` component: `status.value !== "connected"` becomes `false`
- StartCall button disappears with exit animation
- `Controls` component: `status.value === "connected"` becomes `true`
- Controls appear with enter animation

#### **PHASE 5: Active Call State**

**Step 12: Microphone Access Request**
```typescript
// Browser requests microphone permission
navigator.mediaDevices.getUserMedia({ audio: true })
```

**Step 13: Controls Component Active State (`components/Controls.tsx`)**
```typescript
<motion.div className={"p-4 bg-card border border-border rounded-lg shadow-sm flex items-center gap-4"}>
  {/* Mute/Unmute Toggle */}
  <Toggle
    pressed={!isMuted}
    onPressedChange={() => {
      if (isMuted) {
        unmute();  // Enable microphone
      } else {
        mute();    // Disable microphone
      }
    }}
  >
    {isMuted ? <MicOff /> : <Mic />}
  </Toggle>

  {/* Microphone Visualization */}
  <div className={"relative grid h-8 w-48 shrink grow-0"}>
    <MicFFT fft={micFft} />  {/* Real-time audio visualization */}
  </div>

  {/* End Call Button */}
  <Button onClick={async () => await disconnect()} variant={"destructive"}>
    <Phone />
    <span>End Call</span>
  </Button>
</motion.div>
```

**Step 14: Real-Time Voice Streaming**
- Audio captured from microphone
- Audio data sent via WebSocket to Hume API
- Hume processes audio for:
  - Speech-to-text conversion
  - Emotion analysis
  - AI response generation
  - Text-to-speech synthesis
- Audio response streamed back
- Browser plays audio response

#### **PHASE 6: Message Handling**

**Step 15: Message Processing (`components/Messages.tsx`)**
```typescript
const Messages = forwardRef<ComponentRef<typeof motion.div>>(() => {
  const { messages } = useVoice();  // Real-time message updates

  return (
    <motion.div className={"grow rounded-md overflow-auto p-4"}>
      <motion.div className={"max-w-2xl mx-auto w-full flex flex-col gap-4 pb-24"}>
        <AnimatePresence mode={"popLayout"}>
          {messages.map((msg, index) => {
            if (msg.type === "user_message" || msg.type === "assistant_message") {
              return (
                <motion.div
                  key={msg.type + index}
                  className={cn(
                    "w-[80%]",
                    "bg-card border border-border rounded",
                    msg.type === "user_message" ? "ml-auto" : "",  // User messages on right
                  )}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 0 }}
                >
                  <div className={"text-xs opacity-50 pt-3 px-3"}>
                    {msg.type === "user_message" ? "You" : "Assistant"}
                  </div>
                  <div className={"pb-3 px-3"}>{msg.message.content}</div>
                  
                  {/* Emotion visualization for assistant messages */}
                  {msg.type === "assistant_message" && msg.models.prosody?.scores && (
                    <Expressions values={msg.models.prosody.scores} />
                  )}
                </motion.div>
              );
            }
          })}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
});
```

**Step 16: Emotion Visualization (`components/Expressions.tsx`)**
```typescript
export default function Expressions({ values }: { values: EmotionScores | undefined }) {
  if (!values) return;

  // Get top 3 emotions with highest scores
  const top3 = R.pipe(
    values || {},
    R.entries(),
    R.sortBy(R.pathOr([1], 0)),
    R.reverse(),
    R.take(3),
  );

  return (
    <div className={"text-xs p-3 w-full border-t border-border flex flex-col md:flex-row gap-3"}>
      {top3.map(([emotion, score]) => {
        const color = expressionColors[emotion];  // Get color from utils
        return (
          <div key={emotion} className={"flex items-center gap-2"}>
            <div
              className={"w-3 h-3 rounded-full"}
              style={{ backgroundColor: color }}
            />
            <span className={"capitalize"}>{emotion}</span>
            <span className={"opacity-50"}>
              {typeof score === "number" ? (score * 100).toFixed(0) : score}%
            </span>
          </div>
        );
      })}
    </div>
  );
}
```

#### **PHASE 7: Session Management**

**Step 17: Microphone FFT Visualization (`components/MicFFT.tsx`)**
```typescript
export default function MicFFT({ fft }: { fft: number[] }) {
  return (
    <svg className={"w-full h-full"} viewBox="0 0 100 20">
      {fft.map((value, index) => (
        <rect
          key={index}
          x={index * 2}           // Bar spacing
          y={20 - value * 20}     // Height based on audio level
          width={1.5}             // Bar width
          height={value * 20}     // Dynamic height
          className={"fill-current opacity-75"}
        />
      ))}
    </svg>
  );
}
```

**Step 18: Auto-Scroll Behavior**
```typescript
// In Chat.tsx - triggered by onMessage
onMessage={() => {
  if (timeout.current) {
    window.clearTimeout(timeout.current);
  }
  
  timeout.current = window.setTimeout(() => {
    if (ref.current) {
      const scrollHeight = ref.current.scrollHeight;
      ref.current.scrollTo({
        top: scrollHeight,     // Scroll to bottom
        behavior: "smooth",    // Smooth scrolling
      });
    }
  }, 200);  // Delay to ensure message is rendered
}}
```

#### **PHASE 8: Call Termination**

**Step 19: User Clicks "End Call"**
- `disconnect()` function called
- WebSocket connection closed
- Status changes: "connected" → "disconnected"

**Step 20: UI State Reset**
- Controls component hides with exit animation
- StartCall component shows with enter animation
- Messages remain visible (conversation history)
- Microphone access released

### Error Handling Flow

**Authentication Errors:**
```typescript
// In getServerSideProps
try {
  const accessToken = await fetchAccessToken(/*...*/);
  return { props: { accessToken } };
} catch (error) {
  console.error("Failed to fetch access token:", error);
  throw error;  // → Renders pages/500.tsx
}
```

**Connection Errors:**
```typescript
// In StartCall component
connect(EVI_CONNECT_OPTIONS)
  .then(() => {
    // Success - UI automatically updates via status change
  })
  .catch((error) => {
    // Error handling - status remains "disconnected"
    console.error("Connection failed:", error);
  })
  .finally(() => {
    // Cleanup if needed
  });
```

**Microphone Errors:**
- Browser denies microphone access
- User can still see messages but cannot speak
- Mute button indicates no microphone access

This complete flow shows how the application moves through each state, from initial load to active conversation, with clear component interactions and state management throughout the entire process.

## Component Breakdown

### Core Components:

#### `Chat.tsx` - Main Container
- **Purpose**: Central orchestrator for the voice chat experience
- **Key Features**: 
  - VoiceProvider context setup
  - Auto-scroll message behavior
  - Component composition
- **Props**: `accessToken: string`

#### `StartCall.tsx` - Connection Initiator
- **Purpose**: Handles connection to Hume's EVI service
- **Key Features**:
  - One-click connection
  - Configuration ID support
  - Connection status management
- **Configuration**: 
  ```typescript
  configId: "c727d956-e06c-459a-9640-0bc0efa2c159"
  ```

#### `Messages.tsx` - Conversation Display
- **Purpose**: Renders conversation history with animations
- **Key Features**:
  - Message type differentiation (user vs assistant)
  - Emotion expression visualization
  - Smooth enter/exit animations
  - Auto-scrolling behavior

#### `Controls.tsx` - Voice Controls
- **Purpose**: Manages voice interaction controls
- **Key Features**:
  - Mute/unmute toggle
  - Microphone activity visualization
  - Call termination
  - Real-time audio feedback

#### `Expressions.tsx` - Emotion Visualization
- **Purpose**: Displays detected emotional expressions
- **Key Features**:
  - Top 3 emotion scores
  - Color-coded emotion indicators
  - Real-time emotion updates
  - Visual emotion intensity

#### `MicFFT.tsx` - Audio Visualization
- **Purpose**: Visual representation of microphone input
- **Key Features**:
  - Real-time audio waveform
  - SVG-based visualization
  - Responsive design

### UI Components (`components/ui/`):

#### `button.tsx` - Custom Button
- Built on Radix UI primitives
- Multiple variants (default, destructive, etc.)
- Consistent styling with CVA (Class Variance Authority)

#### `toggle.tsx` - Toggle Switch
- Accessible toggle implementation
- Used for mute/unmute functionality
- Styled with Tailwind CSS

## Features

### 1. **Voice Conversation**
- Real-time voice input and output
- Natural conversation flow
- Automatic speech recognition
- Text-to-speech synthesis

### 2. **Emotion Detection**
- Real-time emotion analysis
- Visual emotion indicators
- Top 3 emotions displayed
- Color-coded emotion representation

### 3. **Interactive Controls**
- Start/end call functionality
- Mute/unmute microphone
- Visual microphone activity feedback
- Responsive touch controls

### 4. **Modern UI/UX**
- Clean, minimalist design
- Smooth animations with Framer Motion
- Responsive layout for all devices
- Accessible components

### 5. **Real-time Feedback**
- Live microphone visualization
- Connection status indicators
- Message delivery confirmation
- Error handling and recovery

## API Integration

### Authentication Flow:
```typescript
// Server-side token generation
const accessToken = await fetchAccessToken({
  apiKey: process.env.HUME_API_KEY,
  secretKey: process.env.HUME_SECRET_KEY,
});

// Client-side connection
connect({
  auth: { type: "accessToken", value: accessToken },
  configId: "optional-config-id"
});
```

### Voice Provider Integration:
```typescript
import { VoiceProvider, useVoice } from "@humeai/voice-react";

// Provider setup
<VoiceProvider onMessage={handleMessage}>
  {/* Components */}
</VoiceProvider>

// Hook usage
const { status, connect, disconnect, messages, micFft } = useVoice();
```

### Message Handling:
- **User Messages**: Captured from microphone input
- **Assistant Messages**: Received from Hume AI
- **Emotion Data**: Included with each message
- **Real-time Updates**: WebSocket-based message streaming

## Styling and UI

### Design System:
- **Color Scheme**: Modern dark/light theme support
- **Typography**: Geist font family for clean readability
- **Spacing**: Consistent spacing scale with Tailwind
- **Components**: Shadcn/ui component library

### Key Design Patterns:
```css
/* Card-based layout */
.bg-card .border .border-border .rounded

/* Responsive spacing */
.p-4 .gap-4 .mx-auto .w-full

/* Animation classes */
.transition-all .duration-200 .ease-in-out
```

### Responsive Design:
- Mobile-first approach
- Flexible grid layouts
- Touch-friendly controls
- Adaptive typography

## Development Workflow

### Available Scripts:
```json
{
  "dev": "next dev",        // Development server
  "build": "next build",    // Production build
  "start": "next start",    // Production server
  "lint": "next lint"       // Code linting
}
```

### Development Commands:
```bash
# Start development server
pnpm run dev

# Build for production
pnpm run build

# Start production server
pnpm run start

# Run linting
pnpm run lint
```

### Hot Reloading:
- Automatic code recompilation
- Live browser refresh
- State preservation during development
- Error overlay for debugging

## Deployment

### Vercel Deployment (Recommended):
1. **One-click deployment:**
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fhumeai%2Fhume-evi-next-js-starter&env=HUME_API_KEY,HUME_CLIENT_SECRET)

2. **Manual deployment:**
   ```bash
   # Connect to Vercel
   npx vercel

   # Set environment variables in Vercel dashboard
   # Deploy
   npx vercel --prod
   ```

### Environment Variables in Production:
- Set `HUME_API_KEY` in deployment platform
- Set `HUME_SECRET_KEY` in deployment platform
- Ensure variables are marked as secure/encrypted

### Alternative Deployment Options:
- **Netlify**: Static site deployment
- **Railway**: Full-stack deployment
- **DigitalOcean**: App platform deployment
- **Self-hosted**: Docker containerization

## Troubleshooting

### Common Issues:

#### **1. Authentication Errors**
```
Error: The HUME_API_KEY environment variable is not set.
```
**Solution**: Verify `.env` file exists with correct API credentials

#### **2. Connection Failures**
```
Failed to fetch access token
```
**Solution**: 
- Check API key validity
- Verify internet connection
- Check Hume AI service status

#### **3. Microphone Access**
```
Microphone access denied
```
**Solution**: 
- Enable microphone permissions in browser
- Use HTTPS in production
- Check browser compatibility

#### **4. Build Errors**
```
Module not found: Can't resolve '@/components/...'
```
**Solution**: 
- Check `tsconfig.json` path aliases
- Verify component imports
- Run `pnpm install` to ensure dependencies

### Debug Steps:
1. **Check browser console** for JavaScript errors
2. **Verify environment variables** are loaded correctly
3. **Test API connectivity** with curl or Postman
4. **Check microphone permissions** in browser settings
5. **Review network tab** for failed requests

### Performance Optimization:
- **Lazy loading**: Components loaded on demand
- **Code splitting**: Automatic route-based splitting
- **Image optimization**: Next.js built-in optimization
- **Bundle analysis**: Use `npm run build` to analyze

## Advanced Configuration

### Custom EVI Configuration:
1. Create configuration in Hume AI Platform
2. Get configuration ID
3. Update `StartCall.tsx`:
   ```typescript
   configId: "your-custom-config-id"
   ```

### Styling Customization:
- Modify `tailwind.config.ts` for theme changes
- Update `styles/globals.css` for global styles
- Customize component variants in `ui/` folder

### Adding New Features:
1. **Voice Commands**: Extend message handling
2. **Custom Emotions**: Add new emotion types
3. **Chat History**: Implement persistent storage
4. **Multiple Users**: Add user management

This application provides a solid foundation for building empathic AI voice interfaces with modern web technologies. The modular architecture makes it easy to extend and customize for specific use cases.
