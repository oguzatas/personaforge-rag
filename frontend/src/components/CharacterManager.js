import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CharacterManager = () => {
  const [universes, setUniverses] = useState([]);
  const [selectedUniverse, setSelectedUniverse] = useState('');
  const [characters, setCharacters] = useState([]);
  const [universeRoles, setUniverseRoles] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newCharacter, setNewCharacter] = useState({
    name: '',
    role: '',
    universe: '',
    inventory: [''],
    current_mood: {
      primary_emotion: 'joy',
      intensity: 'moderate',
      plutchik_axis: ['joy']
    },
    backstory: '',
    location: ''
  });

  const plutchikEmotions = [
    'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation'
  ];

  const intensityLevels = ['low', 'moderate', 'high', 'extreme'];

  useEffect(() => {
    fetchUniverses();
  }, []);

  useEffect(() => {
    if (selectedUniverse) {
      fetchCharacters();
      fetchUniverseDetails();
    }
  }, [selectedUniverse]);

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

  const fetchUniverseDetails = async () => {
    try {
      const response = await axios.get(`/api/universes/${selectedUniverse}`);
      setUniverseRoles(response.data.roles);
    } catch (error) {
      console.error('Error fetching universe details:', error);
    }
  };

  const handleCreateCharacter = async (e) => {
    e.preventDefault();
    try {
      const characterData = {
        ...newCharacter,
        universe: selectedUniverse,
        inventory: newCharacter.inventory.filter(item => item.trim() !== '')
      };
      await axios.post(`/api/universes/${selectedUniverse}/characters`, characterData);
      setShowCreateForm(false);
      resetForm();
      fetchCharacters();
      alert('Character created successfully!');
    } catch (error) {
      alert('Error creating character: ' + error.response?.data?.detail);
    }
  };

  const resetForm = () => {
    setNewCharacter({
      name: '',
      role: '',
      universe: '',
      inventory: [''],
      current_mood: {
        primary_emotion: 'joy',
        intensity: 'moderate',
        plutchik_axis: ['joy']
      },
      backstory: '',
      location: ''
    });
  };

  const addInventoryItem = () => {
    setNewCharacter({
      ...newCharacter,
      inventory: [...newCharacter.inventory, '']
    });
  };

  const updateInventoryItem = (index, value) => {
    const updatedInventory = newCharacter.inventory.map((item, i) => 
      i === index ? value : item
    );
    setNewCharacter({ ...newCharacter, inventory: updatedInventory });
  };

  const removeInventoryItem = (index) => {
    const updatedInventory = newCharacter.inventory.filter((_, i) => i !== index);
    setNewCharacter({ ...newCharacter, inventory: updatedInventory });
  };

  const updateMood = (field, value) => {
    setNewCharacter({
      ...newCharacter,
      current_mood: {
        ...newCharacter.current_mood,
        [field]: value
      }
    });
  };

  const addEmotionToAxis = (emotion) => {
    if (!newCharacter.current_mood.plutchik_axis.includes(emotion)) {
      updateMood('plutchik_axis', [...newCharacter.current_mood.plutchik_axis, emotion]);
    }
  };

  const removeEmotionFromAxis = (emotion) => {
    updateMood('plutchik_axis', newCharacter.current_mood.plutchik_axis.filter(e => e !== emotion));
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Character Management</h2>
        <div className="flex space-x-4">
          <select
            value={selectedUniverse}
            onChange={(e) => setSelectedUniverse(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="">Select Universe</option>
            {universes.map((universe) => (
              <option key={universe} value={universe}>{universe}</option>
            ))}
          </select>
          {selectedUniverse && (
            <button
              onClick={() => setShowCreateForm(true)}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            >
              Create Character
            </button>
          )}
        </div>
      </div>

      {/* Character List */}
      {selectedUniverse && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {characters.map((character, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-2">{character.name}</h3>
              <p className="text-gray-600 mb-2">Role: {character.role}</p>
              <p className="text-gray-600 mb-2">Location: {character.location}</p>
              <p className="text-gray-600 mb-2">
                Mood: {character.current_mood.primary_emotion} ({character.current_mood.intensity})
              </p>
              <p className="text-gray-600 text-sm">{character.backstory.substring(0, 100)}...</p>
            </div>
          ))}
        </div>
      )}

      {/* Create Character Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-10 mx-auto p-5 border w-4/5 max-w-4xl shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Character</h3>
              <form onSubmit={handleCreateCharacter} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                {/* Basic Info */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Name</label>
                    <input
                      type="text"
                      value={newCharacter.name}
                      onChange={(e) => setNewCharacter({...newCharacter, name: e.target.value})}
                      className="w-full p-2 border rounded"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Role</label>
                    <select
                      value={newCharacter.role}
                      onChange={(e) => setNewCharacter({...newCharacter, role: e.target.value})}
                      className="w-full p-2 border rounded"
                      required
                    >
                      <option value="">Select Role</option>
                      {universeRoles.map((role) => (
                        <option key={role.name} value={role.name}>{role.name}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Location</label>
                    <input
                      type="text"
                      value={newCharacter.location}
                      onChange={(e) => setNewCharacter({...newCharacter, location: e.target.value})}
                      className="w-full p-2 border rounded"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Backstory</label>
                    <textarea
                      value={newCharacter.backstory}
                      onChange={(e) => setNewCharacter({...newCharacter, backstory: e.target.value})}
                      className="w-full p-2 border rounded"
                      rows="4"
                      required
                    />
                  </div>
                </div>

                {/* Mood & Inventory */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Primary Emotion</label>
                    <select
                      value={newCharacter.current_mood.primary_emotion}
                      onChange={(e) => updateMood('primary_emotion', e.target.value)}
                      className="w-full p-2 border rounded"
                    >
                      {plutchikEmotions.map((emotion) => (
                        <option key={emotion} value={emotion}>{emotion}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Intensity</label>
                    <select
                      value={newCharacter.current_mood.intensity}
                      onChange={(e) => updateMood('intensity', e.target.value)}
                      className="w-full p-2 border rounded"
                    >
                      {intensityLevels.map((level) => (
                        <option key={level} value={level}>{level}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Plutchik Axis</label>
                    <div className="mb-2">
                      {newCharacter.current_mood.plutchik_axis.map((emotion) => (
                        <span
                          key={emotion}
                          className="inline-block bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded mr-2 mb-2"
                        >
                          {emotion}
                          <button
                            type="button"
                            onClick={() => removeEmotionFromAxis(emotion)}
                            className="ml-1 text-red-500"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                    </div>
                    <select
                      onChange={(e) => addEmotionToAxis(e.target.value)}
                      className="w-full p-2 border rounded"
                      value=""
                    >
                      <option value="">Add emotion to axis</option>
                      {plutchikEmotions.map((emotion) => (
                        <option key={emotion} value={emotion}>{emotion}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2">Inventory</label>
                    {newCharacter.inventory.map((item, index) => (
                      <div key={index} className="flex mb-2">
                        <input
                          type="text"
                          value={item}
                          onChange={(e) => updateInventoryItem(index, e.target.value)}
                          className="flex-1 p-2 border rounded"
                          placeholder="Item name"
                        />
                        {newCharacter.inventory.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removeInventoryItem(index)}
                            className="ml-2 text-red-500"
                          >
                            Remove
                          </button>
                        )}
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={addInventoryItem}
                      className="text-blue-500 text-sm"
                    >
                      + Add Item
                    </button>
                  </div>
                </div>

                <div className="col-span-1 md:col-span-2 flex justify-end space-x-2 mt-4">
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Create Character
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CharacterManager; 