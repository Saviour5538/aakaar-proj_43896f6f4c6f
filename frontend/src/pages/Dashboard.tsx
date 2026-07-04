import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listDocuments as fetchDocuments, listConversations as fetchConversations } from '../api/client';
import { Document, Conversation } from '../types';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [docsResponse, convResponse] = await Promise.all([
          fetchDocuments(),
          fetchConversations(),
        ]);
        setDocuments(docsResponse);
        setConversations(convResponse);
      } catch (err) {
        setError('Failed to load data. Please try again.');
        toast.error('Error fetching dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>
      {loading ? (
        <div className="text-center text-gray-600">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-600">{error}</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold text-gray-700">Documents</h2>
              <p className="text-2xl font-bold text-gray-900">{documents.length}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-4">
              <h2 className="text-lg font-semibold text-gray-700">Conversations</h2>
              <p className="text-2xl font-bold text-gray-900">{conversations.length}</p>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Documents</h2>
            {documents.length > 0 ? (
              <ul className="bg-white shadow rounded-lg divide-y divide-gray-200">
                {documents.slice(0, 5).map((doc) => (
                  <li key={doc.id} className="p-4">
                    <p className="text-gray-700 font-medium">{doc.name}</p>
                    <p className="text-gray-500 text-sm">{new Date(doc.created_at).toLocaleString()}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600">No documents available.</p>
            )}
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Conversations</h2>
            {conversations.length > 0 ? (
              <ul className="bg-white shadow rounded-lg divide-y divide-gray-200">
                {conversations.slice(0, 5).map((conv) => (
                  <li key={conv.id} className="p-4">
                    <p className="text-gray-700 font-medium">Conversation #{conv.id}</p>
                    <p className="text-gray-500 text-sm">{new Date(conv.created_at).toLocaleString()}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600">No conversations available.</p>
            )}
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleUploadClick}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-700"
            >
              Upload Document
            </button>
            <button
              onClick={handleChatClick}
              className="bg-green-600 text-white px-4 py-2 rounded-lg shadow hover:bg-green-700"
            >
              Start Chat
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;