import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ChatInterface = () => {
  const [universes, setUniverses] = useState([]);
  const [selectedUniverse, setSelectedUniverse] = useState('');
  const [characters, setCharacters] = useState([]);
  const [selectedCharacter, setSelectedCharacter] = useState('');
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchUniverses();
  }, []);

  useEffect(() => {
    if (selectedUniverse) {
      fetchCharacters();
      setSelectedCharacter('');
      setMessages([]);
    }
  }, [selectedUniverse]);

  useEffect(() => {
    if (selectedCharacter) {
      const character = characters.find(c => c.name === selectedCharacter);
      if (character) {
        setMessages([{
          type: 'system',
          content: `You are now chatting with ${character.name}, a ${character.role} from ${selectedUniverse}. Current mood: ${character.current_mood.primary_emotion} (${character.current_mood.intensity})`
        }]);
      }
    }
  }, [selectedCharacter, characters, selectedUniverse]);

  const fetchUniverses = async () => {
    try {
      const response = await axios.get('/api/universes');
      setUniverses(response.data.universes);
    } catch (error) {
      console.error('Error fetching universes:', error);
    }
  };

  const fetchCharacters = async () => {
    try {
      const response = await axios.get(`/api/universes/${selectedUniverse}/characters`);
      setCharacters(response.data.characters);
    } catch (error) {
      console.error('Error fetching characters:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!currentMessage.trim() || !selectedUniverse || !selectedCharacter) return;

    const userMessage = {
      type: 'user',
      content: currentMessage,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        query: currentMessage,
        universe: selectedUniverse,
        character_name: selectedCharacter
      });

      const aiMessage = {
        type: 'ai',
        content: response.data.response,
        character: response.data.character,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: 'Sorry, there was an error processing your message: ' + error.response?.data?.detail,
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    if (selectedCharacter) {
      const character = characters.find(c => c.name === selectedCharacter);
      setMessages([{
        type: 'system',
        content: `You are now chatting with ${character.name}, a ${character.role} from ${selectedUniverse}. Current mood: ${character.current_mood.primary_emotion} (${character.current_mood.intensity})`
      }]);
    } else {
      setMessages([]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md">
        {/* Header */}
        <div className="border-b p-4">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Chat Interface</h2>
          <div className="flex space-x-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">Universe</label>
              <select
                value={selectedUniverse}
                onChange={(e) => setSelectedUniverse(e.target.value)}
                className="w-full border rounded px-3 py-2"
              >
                <option value="">Select Universe</option>
                {universes.map((universe) => (
                  <option key={universe} value={universe}>{universe}</option>
                ))}
              </select>
            </div>
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">Character</label>
              <select
                value={selectedCharacter}
                onChange={(e) => setSelectedCharacter(e.target.value)}
                className="w-full border rounded px-3 py-2"
                disabled={!selectedUniverse}
              >
                <option value="">Select Character</option>
                {characters.map((character) => (
                  <option key={character.name} value={character.name}>
                    {character.name} ({character.role})
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={clearChat}
                className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                disabled={!selectedCharacter}
              >
                Clear Chat
              </button>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="h-96 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.type === 'user' 
                  ? 'bg-blue-500 text-white' 
                  : message.type === 'system'
                  ? 'bg-gray-200 text-gray-700 text-sm'
                  : message.type === 'error'
                  ? 'bg-red-100 text-red-700'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {message.type === 'ai' && (
                  <div className="text-xs text-gray-500 mb-1">{message.character}</div>
                )}
                <div className="whitespace-pre-wrap">{message.content}</div>
                {message.timestamp && (
                  <div className="text-xs opacity-75 mt-1">{message.timestamp}</div>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                  <span>Thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Message Input */}
        <div className="border-t p-4">
          <form onSubmit={sendMessage} className="flex space-x-2">
            <input
              type="text"
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              placeholder={selectedCharacter ? `Message ${selectedCharacter}...` : "Select a character to start chatting"}
              className="flex-1 border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={!selectedCharacter || isLoading}
            />
            <button
              type="submit"
              disabled={!selectedCharacter || isLoading || !currentMessage.trim()}
              className="bg-blue-500 hover:bg-blue-700 disabled:bg-gray-300 text-white font-bold py-2 px-4 rounded"
            >
              Send
            </button>
          </form>
        </div>
      </div>

      {/* Character Info Panel */}
      {selectedCharacter && (
        <div className="mt-4 bg-white rounded-lg shadow-md p-4">
          <h3 className="text-lg font-semibold mb-2">Character Info</h3>
          {(() => {
            const character = characters.find(c => c.name === selectedCharacter);
            return character ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p><strong>Name:</strong> {character.name}</p>
                  <p><strong>Role:</strong> {character.role}</p>
                  <p><strong>Location:</strong> {character.location}</p>
                </div>
                <div>
                  <p><strong>Mood:</strong> {character.current_mood.primary_emotion} ({character.current_mood.intensity})</p>
                  <p><strong>Emotions:</strong> {character.current_mood.plutchik_axis.join(', ')}</p>
                  <p><strong>Inventory:</strong> {character.inventory.join(', ')}</p>
                </div>
                <div className="md:col-span-2">
                  <p><strong>Backstory:</strong> {character.backstory}</p>
                </div>
              </div>
            ) : null;
          })()}
        </div>
      )}
    </div>
  );
};

export default ChatInterface; 