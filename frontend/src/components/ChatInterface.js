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
  const [debugMode, setDebugMode] = useState(false);
  const [debugInfo, setDebugInfo] = useState(null);

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
    setDebugInfo(null);

    try {
      console.log('Sending request with debug mode:', debugMode);
      const requestData = {
        query: currentMessage,
        universe: selectedUniverse,
        character_name: selectedCharacter,
        debug: debugMode
      };
      console.log('Request data:', requestData);
      
      const response = await axios.post('/api/chat', requestData);
      console.log('Response received:', response.data);

      const aiMessage = {
        type: 'ai',
        content: response.data.response,
        character: response.data.character,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // Store debug info if available
      if (debugMode && response.data.debug_info) {
        console.log('Setting debug info:', response.data.debug_info);
        setDebugInfo(response.data.debug_info);
      } else if (debugMode) {
        console.log('Debug mode enabled but no debug_info in response');
        console.log('Full response:', response.data);
      }
    } catch (error) {
      console.error('Error in sendMessage:', error);
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
    setDebugInfo(null);
  };

  const toggleDebugMode = () => {
    setDebugMode(!debugMode);
    setDebugInfo(null);
  };

  return (
    <div className="max-w-6xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Chat Interface</h2>
          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={debugMode}
                onChange={toggleDebugMode}
                className="mr-2"
              />
              <span className="text-sm font-medium">Debug Mode</span>
            </label>
            <button
              onClick={clearChat}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Clear Chat
            </button>
          </div>
        </div>

        {/* Universe and Character Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Universe
            </label>
            <select
              value={selectedUniverse}
              onChange={(e) => setSelectedUniverse(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="">Choose a universe...</option>
              {universes.map((universe) => (
                <option key={universe} value={universe}>
                  {universe}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Character
            </label>
            <select
              value={selectedCharacter}
              onChange={(e) => setSelectedCharacter(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
              disabled={!selectedUniverse}
            >
              <option value="">Choose a character...</option>
              {characters.map((character) => (
                <option key={character.name} value={character.name}>
                  {character.name} ({character.role})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Messages */}
          <div className="lg:col-span-2">
            <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto mb-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`mb-4 p-3 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-blue-100 ml-8'
                      : message.type === 'ai'
                      ? 'bg-green-100 mr-8'
                      : message.type === 'system'
                      ? 'bg-yellow-100 text-center'
                      : 'bg-red-100'
                  }`}
                >
                  <div className="font-medium text-sm text-gray-600 mb-1">
                    {message.type === 'user' ? 'You' : 
                     message.type === 'ai' ? message.character : 
                     message.type === 'system' ? 'System' : 'Error'}
                    {message.timestamp && (
                      <span className="ml-2 text-xs">{message.timestamp}</span>
                    )}
                  </div>
                  <div className="text-gray-800">{message.content}</div>
                </div>
              ))}
              {isLoading && (
                <div className="text-center text-gray-500">
                  <div className="animate-spin inline-block w-4 h-4 border-2 border-gray-500 border-t-transparent rounded-full mr-2"></div>
                  Thinking...
                </div>
              )}
            </div>

            {/* Message Input */}
            <form onSubmit={sendMessage} className="flex gap-2">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 p-2 border border-gray-300 rounded-md"
                disabled={!selectedCharacter || isLoading}
              />
              <button
                type="submit"
                disabled={!selectedCharacter || isLoading || !currentMessage.trim()}
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300"
              >
                Send
              </button>
            </form>
          </div>

          {/* Debug Panel */}
          {debugMode && (
            <div className="lg:col-span-1">
              <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto">
                <h3 className="text-lg font-semibold mb-4 text-gray-800">Debug Info</h3>
                {debugInfo ? (
                  <div className="space-y-4">
                    {/* Character Info */}
                    <div>
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Character Info</h4>
                      <div className="bg-white p-3 rounded border text-xs">
                        <p><strong>Name:</strong> {debugInfo.character_info.name}</p>
                        <p><strong>Role:</strong> {debugInfo.character_info.role}</p>
                        <p><strong>Mood:</strong> {debugInfo.character_info.mood}</p>
                        <p><strong>Location:</strong> {debugInfo.character_info.location}</p>
                      </div>
                    </div>

                    {/* Retrieved Context */}
                    <div>
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Retrieved Context ({debugInfo.retrieved_context.length} chunks)</h4>
                      <div className="bg-white p-3 rounded border text-xs max-h-32 overflow-y-auto">
                        {debugInfo.retrieved_context.map((chunk, index) => (
                          <div key={index} className="mb-2 p-2 bg-gray-50 rounded">
                            <strong>Chunk {index + 1}:</strong> {chunk}
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Full Prompt */}
                    <div>
                      <h4 className="font-medium text-sm text-gray-700 mb-2">Full Prompt</h4>
                      <div className="bg-white p-3 rounded border text-xs max-h-32 overflow-y-auto">
                        <pre className="whitespace-pre-wrap">{debugInfo.full_prompt}</pre>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-gray-500 text-sm">
                    Send a message to see debug information
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 