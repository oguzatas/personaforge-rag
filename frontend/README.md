# PersonaForge Frontend

React-based frontend for the PersonaForge RAG system, providing an intuitive interface for managing characters, universes, and interactive conversations.

## Features

- **Character Management**: Create, edit, and manage characters with rich schemas
- **Universe Management**: Organize characters into different universes
- **Interactive Chat**: Real-time conversations with AI-powered characters
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Real-time Updates**: Live updates for character data and conversations

## Quick Start

### Installation

npm version v23.6.1

```bash
npm install
```

### Development Server

```bash
npm start
```

The application will start on `http://localhost:3000`

### Production Build

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/              # Static assets
│   └── index.html      # Main HTML template
├── src/                # React source code
│   ├── components/     # React components
│   │   ├── CharacterManager.js  # Character management interface
│   │   ├── ChatInterface.js     # Chat interface
│   │   └── UniverseManager.js   # Universe management
│   ├── App.js          # Main application component
│   ├── App.css         # Application styles
│   └── index.js        # Application entry point
├── package.json        # Node.js dependencies
├── tailwind.config.js  # Tailwind CSS configuration
└── postcss.config.js   # PostCSS configuration
```

## Components

### CharacterManager
- Character creation and editing
- Character listing and search
- Character statistics and analytics

### ChatInterface
- Real-time chat with characters
- Conversation history
- Character selection

### UniverseManager
- Universe creation and management
- Universe listing and navigation

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- **Character Endpoints**: CRUD operations for characters
- **Universe Endpoints**: Universe management
- **Chat Endpoints**: Interactive conversations
- **Analytics Endpoints**: Character statistics

## Development

### Available Scripts

- `npm start` - Start development server
- `npm test` - Run tests
- `npm run build` - Build for production
- `npm run eject` - Eject from Create React App

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Styling

The application uses:
- **Tailwind CSS** for utility-first styling
- **PostCSS** for CSS processing
- **Custom CSS** for component-specific styles

## Dependencies

- **React**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing

See `package.json` for complete list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 