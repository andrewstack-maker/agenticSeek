import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentView, setCurrentView] = useState('blocks');
    const [responseData, setResponseData] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;
        setMessages((prev) => [...prev, { type: 'user', content: query }]);
        setIsLoading(true);
        setError(null);

        try {
            const res = await axios.post('http://localhost:8000/query', {
                query,
                lang: 'en',
                tts_enabled: false,
                stt_enabled: false,
            });
            const data = res.data;
            setResponseData(data);
            setMessages((prev) => [
                ...prev,
                { type: 'agent', content: data.answer, agentName: data.agent_name },
            ]);
            setCurrentView('blocks');
        } catch (err) {
            setError('Failed to process query.');
            setMessages((prev) => [
                ...prev,
                { type: 'error', content: 'Error: Unable to get a response.' },
            ]);
        } finally {
            setIsLoading(false);
            setQuery('');
        }
    };

    const handleGetScreenshot = async () => {
        try {
            const res = await axios.get('http://localhost:8000/screenshots/updated_screen.png');
            setResponseData((prev) => ({ ...prev, screenshot: res.data.screenshot }));
            setCurrentView('screenshot');
        } catch (err) {
            setError('Failed to fetch screenshot.');
        }
    };

    return (
        <div className="app">
            <header className="header">
                <h1>AgenticSeek</h1>
            </header>
            <main className="main">
                <div className="chat-container">
                    <div className="left-panel">
                        <h2>Chat</h2>
                        <div className="messages">
                            {messages.length === 0 ? (
                                <p className="placeholder">No messages yet. Type below to start!</p>
                            ) : (
                                messages.map((msg, index) => (
                                    <div
                                        key={index}
                                        className={`message ${
                                            msg.type === 'user'
                                                ? 'user-message'
                                                : msg.type === 'agent'
                                                ? 'agent-message'
                                                : 'error-message'
                                        }`}
                                    >
                                        {msg.type === 'agent' && (
                                            <span className="agent-name">{msg.agentName}</span>
                                        )}
                                        <p>{msg.content}</p>
                                    </div>
                                ))
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                        {isLoading && <div className="loading-animation">Loading...</div>}
                        <form onSubmit={handleSubmit} className="input-form">
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="Type your query..."
                                disabled={isLoading}
                            />
                            <button type="submit" disabled={isLoading}>
                                Send
                            </button>
                        </form>
                    </div>
                    <div className="right-panel">
                        <h2>Details</h2>
                        <div className="view-selector">
                            <button
                                className={currentView === 'blocks' ? 'active' : ''}
                                onClick={() => setCurrentView('blocks')}
                            >
                                Editor View
                            </button>
                            <button
                                className={currentView === 'screenshot' ? 'active' : ''}
                                onClick={responseData?.screenshot ? () => setCurrentView('screenshot') : handleGetScreenshot}
                            >
                                Browser View
                            </button>
                        </div>
                        <div className="content">
                            {error && <p className="error">{error}</p>}
                            {currentView === 'blocks' ? (
                                <div className="blocks">
                                    {responseData && responseData.blocks && Object.values(responseData.blocks).length > 0 ? (
                                        Object.values(responseData.blocks).map((block, index) => (
                                            <div key={index} className="block">
                                                <p className="block-tool">Tool: {block.tool_type}</p>
                                                <pre>{block.block}</pre>
                                                <p className="block-feedback">Feedback: {block.feedback}</p>
                                                <p className="block-success">
                                                    Success: {block.success ? 'Yes' : 'No'}
                                                </p>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="block">
                                            <p className="block-tool">Tool: No tool in use</p>
                                            <pre>No file opened</pre>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div className="screenshot">
                                  <img src="http://localhost:8000/screenshots/updated_screen.png" alt="Screenshot" />
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
