import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import UniverseManager from './components/UniverseManager';
import CharacterManager from './components/CharacterManager';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-blue-600 text-white p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">PersonaForge</h1>
            <div className="space-x-4">
              <Link to="/" className="hover:text-blue-200">Universes</Link>
              <Link to="/characters" className="hover:text-blue-200">Characters</Link>
              <Link to="/chat" className="hover:text-blue-200">Chat</Link>
            </div>
          </div>
        </nav>

        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<UniverseManager />} />
            <Route path="/characters" element={<CharacterManager />} />
            <Route path="/chat" element={<ChatInterface />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 