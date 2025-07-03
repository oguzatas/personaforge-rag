import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UniverseManager = () => {
  const [universes, setUniverses] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [buildingIndex, setBuildingIndex] = useState({});
  const [newUniverse, setNewUniverse] = useState({
    universe_name: '',
    description: '',
    roles: [{ name: '', description: '' }]
  });

  useEffect(() => {
    fetchUniverses();
  }, []);

  const fetchUniverses = async () => {
    try {
      const response = await axios.get('/api/universes');
      setUniverses(response.data.universes);
    } catch (error) {
      console.error('Error fetching universes:', error);
    }
  };

  const buildUniverseIndex = async (universeName) => {
    setBuildingIndex(prev => ({ ...prev, [universeName]: true }));
    try {
      const response = await axios.post(`/api/universes/${universeName}/build-index`);
      alert(response.data.message);
    } catch (error) {
      alert('Error building index: ' + error.response?.data?.detail);
    } finally {
      setBuildingIndex(prev => ({ ...prev, [universeName]: false }));
    }
  };

  const handleCreateUniverse = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/universes', newUniverse);
      setShowCreateForm(false);
      setNewUniverse({
        universe_name: '',
        description: '',
        roles: [{ name: '', description: '' }]
      });
      fetchUniverses();
      alert('Universe created successfully!');
    } catch (error) {
      alert('Error creating universe: ' + error.response?.data?.detail);
    }
  };

  const addRole = () => {
    setNewUniverse({
      ...newUniverse,
      roles: [...newUniverse.roles, { name: '', description: '' }]
    });
  };

  const updateRole = (index, field, value) => {
    const updatedRoles = newUniverse.roles.map((role, i) => 
      i === index ? { ...role, [field]: value } : role
    );
    setNewUniverse({ ...newUniverse, roles: updatedRoles });
  };

  const removeRole = (index) => {
    const updatedRoles = newUniverse.roles.filter((_, i) => i !== index);
    setNewUniverse({ ...newUniverse, roles: updatedRoles });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Universe Management</h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Create Universe
        </button>
      </div>

      {/* Universe List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {universes.map((universe) => (
          <div key={universe} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-2">{universe}</h3>
            <p className="text-gray-600 mb-4">Click to view details</p>
            <div className="space-y-2">
              <button className="w-full text-blue-500 hover:text-blue-700 text-left">
                View Details →
              </button>
              <button
                onClick={() => buildUniverseIndex(universe)}
                disabled={buildingIndex[universe]}
                className="w-full bg-green-500 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded text-sm"
              >
                {buildingIndex[universe] ? 'Building Index...' : 'Build FAISS Index'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Create Universe Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Universe</h3>
              <form onSubmit={handleCreateUniverse}>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2">
                    Universe Name
                  </label>
                  <input
                    type="text"
                    value={newUniverse.universe_name}
                    onChange={(e) => setNewUniverse({...newUniverse, universe_name: e.target.value})}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>

                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2">
                    Description
                  </label>
                  <textarea
                    value={newUniverse.description}
                    onChange={(e) => setNewUniverse({...newUniverse, description: e.target.value})}
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    rows="3"
                    required
                  />
                </div>

                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2">
                    Roles
                  </label>
                  {newUniverse.roles.map((role, index) => (
                    <div key={index} className="mb-2 p-2 border rounded">
                      <input
                        type="text"
                        placeholder="Role name"
                        value={role.name}
                        onChange={(e) => updateRole(index, 'name', e.target.value)}
                        className="w-full mb-2 p-1 border rounded"
                        required
                      />
                      <input
                        type="text"
                        placeholder="Role description"
                        value={role.description}
                        onChange={(e) => updateRole(index, 'description', e.target.value)}
                        className="w-full mb-2 p-1 border rounded"
                        required
                      />
                      {newUniverse.roles.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeRole(index)}
                          className="text-red-500 text-sm"
                        >
                          Remove Role
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={addRole}
                    className="text-blue-500 text-sm"
                  >
                    + Add Role
                  </button>
                </div>

                <div className="flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Create
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

export default UniverseManager; 