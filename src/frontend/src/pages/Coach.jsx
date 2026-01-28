import React, { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, Send, Calendar, Target, TrendingUp, Activity, Loader2, X, ChevronDown, ChevronUp, Wifi, WifiOff } from 'lucide-react'
import axios from 'axios'
import { io } from 'socket.io-client'
import { formatPace, formatTime } from '../utils/formatters'

const API_URL = 'http://localhost:5001/api'
const SOCKET_URL = 'http://localhost:5001'

function Coach() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingContent, setStreamingContent] = useState('')
  const [context, setContext] = useState(null)
  const [showContext, setShowContext] = useState(false)
  const [showPlanModal, setShowPlanModal] = useState(false)
  const [planForm, setPlanForm] = useState({
    goal_race: '5K',
    goal_time: '',
    weeks: 8
  })
  const [generatedPlan, setGeneratedPlan] = useState(null)
  const [isPlanLoading, setIsPlanLoading] = useState(false)
  const [socketConnected, setSocketConnected] = useState(false)
  const messagesEndRef = useRef(null)
  const socketRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingContent])

  // Initialize WebSocket connection
  useEffect(() => {
    socketRef.current = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    })

    const socket = socketRef.current

    socket.on('connect', () => {
      console.log('WebSocket connected:', socket.id)
      setSocketConnected(true)
    })

    socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      setSocketConnected(false)
    })

    socket.on('connected', (data) => {
      console.log('Server confirmed connection:', data)
    })

    socket.on('coach_stream_start', () => {
      setIsStreaming(true)
      setStreamingContent('')
    })

    socket.on('coach_token', (data) => {
      setStreamingContent(prev => prev + data.token)
    })

    socket.on('coach_stream_end', (data) => {
      // Add the complete message to messages
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.full_response
      }])

      // Update context if provided
      if (data.context_summary) {
        setContext(data.context_summary)
      }

      setIsStreaming(false)
      setStreamingContent('')
      setIsLoading(false)
    })

    socket.on('coach_error', (data) => {
      console.error('Coach error:', data.error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${data.error}`
      }])
      setIsStreaming(false)
      setStreamingContent('')
      setIsLoading(false)
    })

    return () => {
      socket.disconnect()
    }
  }, [])

  useEffect(() => {
    // Load context and conversation from localStorage
    const savedMessages = localStorage.getItem('coach_messages')
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages))
      } catch (e) {
        console.error('Error loading saved messages:', e)
      }
    }

    // Fetch context
    axios.get(`${API_URL}/coach/context`)
      .then(res => {
        setContext(res.data)
        // Add welcome message if no previous messages
        if (!savedMessages || JSON.parse(savedMessages).length === 0) {
          setMessages([{
            role: 'assistant',
            content: `Hey there! I'm your AI running coach. I can see you've logged ${res.data.total_runs} runs totaling ${res.data.total_miles} miles. Your current weekly average is ${res.data.weekly_avg_miles} miles.\n\nHow can I help you today? I can:\n- Answer questions about your training\n- Suggest workouts based on your fitness\n- Create a personalized training plan for an upcoming race\n- Provide advice on pacing, recovery, and more`
          }])
        }
      })
      .catch(err => console.error('Error loading context:', err))
  }, [])

  useEffect(() => {
    // Save messages to localStorage
    if (messages.length > 0) {
      localStorage.setItem('coach_messages', JSON.stringify(messages))
    }
  }, [messages])

  const sendMessage = useCallback(() => {
    if (!inputMessage.trim() || isLoading || isStreaming) return

    const userMessage = inputMessage.trim()
    setInputMessage('')

    // Add user message immediately
    const newMessages = [...messages, { role: 'user', content: userMessage }]
    setMessages(newMessages)
    setIsLoading(true)

    // Convert messages to history format (exclude the just-added user message)
    const history = messages.map(m => ({ role: m.role, content: m.content }))

    // Use WebSocket if connected, otherwise fall back to REST
    if (socketConnected && socketRef.current) {
      socketRef.current.emit('coach_message', {
        message: userMessage,
        history: history
      })
    } else {
      // Fallback to REST API
      axios.post(`${API_URL}/coach/chat`, {
        message: userMessage,
        history: history
      })
        .then(response => {
          setMessages([...newMessages, {
            role: 'assistant',
            content: response.data.response
          }])
          if (response.data.context_summary) {
            setContext(response.data.context_summary)
          }
        })
        .catch(err => {
          console.error('Error sending message:', err)
          setMessages([...newMessages, {
            role: 'assistant',
            content: 'Sorry, I encountered an error. Please check that the API server is running and AWS Bedrock is properly configured.'
          }])
        })
        .finally(() => {
          setIsLoading(false)
        })
    }
  }, [inputMessage, isLoading, isStreaming, messages, socketConnected])

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const generatePlan = async () => {
    if (!planForm.goal_time) return

    setIsPlanLoading(true)
    try {
      const response = await axios.post(`${API_URL}/coach/training-plan`, planForm)
      setGeneratedPlan(response.data)
    } catch (err) {
      console.error('Error generating plan:', err)
      setGeneratedPlan({ error: 'Failed to generate training plan. Please try again.' })
    } finally {
      setIsPlanLoading(false)
    }
  }

  const clearConversation = () => {
    setMessages([])
    localStorage.removeItem('coach_messages')
    // Re-add welcome message
    if (context) {
      setMessages([{
        role: 'assistant',
        content: `Conversation cleared! I'm ready to help with your training. What would you like to discuss?`
      }])
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
      className="coach-page"
    >
      {/* Header */}
      <div className="coach-header">
        <div className="coach-title">
          <Bot size={32} color="var(--accent-primary)" />
          <div>
            <h1 className="page-title">AI Running Coach</h1>
            <p className="page-subtitle">
              Personalized training advice powered by Claude
              <span className={`connection-status ${socketConnected ? 'connected' : 'disconnected'}`}>
                {socketConnected ? <Wifi size={14} /> : <WifiOff size={14} />}
                {socketConnected ? 'Live' : 'Offline'}
              </span>
            </p>
          </div>
        </div>

        <div className="coach-actions">
          <button
            className="btn btn-secondary"
            onClick={() => setShowContext(!showContext)}
          >
            {showContext ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
            Your Stats
          </button>
          <button
            className="btn btn-primary"
            onClick={() => setShowPlanModal(true)}
          >
            <Calendar size={18} />
            Generate Training Plan
          </button>
        </div>
      </div>

      {/* Context Panel */}
      <AnimatePresence>
        {showContext && context && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="context-panel"
          >
            <div className="context-grid">
              <div className="context-item">
                <Activity size={20} color="var(--accent-primary)" />
                <div>
                  <span className="context-value">{context.total_runs}</span>
                  <span className="context-label">Total Runs</span>
                </div>
              </div>
              <div className="context-item">
                <Target size={20} color="var(--accent-secondary)" />
                <div>
                  <span className="context-value">{context.total_miles}</span>
                  <span className="context-label">Total Miles</span>
                </div>
              </div>
              <div className="context-item">
                <TrendingUp size={20} color="var(--accent-tertiary)" />
                <div>
                  <span className="context-value">{context.weekly_avg_miles}</span>
                  <span className="context-label">Weekly Avg (mi)</span>
                </div>
              </div>
              <div className="context-item">
                <Activity size={20} color="var(--success)" />
                <div>
                  <span className="context-value">{context.last_30_days?.runs || 0}</span>
                  <span className="context-label">Runs (30d)</span>
                </div>
              </div>
            </div>

            {context.predictions && Object.keys(context.predictions).length > 0 && (
              <div className="predictions-row">
                <span className="predictions-label">Race Predictions:</span>
                {Object.entries(context.predictions).map(([distance, pred]) => (
                  <span key={distance} className="prediction-chip">
                    {distance}: {pred.time}
                  </span>
                ))}
              </div>
            )}

            <div className="trend-info">
              <TrendingUp size={16} />
              <span>{context.trend_description}</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Container */}
      <div className="chat-container">
        <div className="messages-list">
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
              className={`message ${msg.role}`}
            >
              {msg.role === 'assistant' && (
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
              )}
              <div className="message-content">
                {msg.content.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </motion.div>
          ))}

          {/* Streaming message */}
          {isStreaming && streamingContent && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="message assistant streaming"
            >
              <div className="message-avatar">
                <Bot size={20} />
              </div>
              <div className="message-content">
                {streamingContent.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
                <span className="cursor-blink">|</span>
              </div>
            </motion.div>
          )}

          {/* Loading indicator (before streaming starts) */}
          {isLoading && !isStreaming && !streamingContent && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="message assistant"
            >
              <div className="message-avatar">
                <Bot size={20} />
              </div>
              <div className="message-content loading">
                <Loader2 size={20} className="spin" />
                <span>Thinking...</span>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <button
            className="clear-btn"
            onClick={clearConversation}
            title="Clear conversation"
          >
            <X size={18} />
          </button>
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask your coach anything..."
            rows={1}
            disabled={isLoading || isStreaming}
          />
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading || isStreaming}
          >
            <Send size={20} />
          </button>
        </div>
      </div>

      {/* Training Plan Modal */}
      <AnimatePresence>
        {showPlanModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal-overlay"
            onClick={() => !isPlanLoading && setShowPlanModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="modal-content plan-modal"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="modal-header">
                <h2>Generate Training Plan</h2>
                <button
                  className="modal-close"
                  onClick={() => !isPlanLoading && setShowPlanModal(false)}
                >
                  <X size={24} />
                </button>
              </div>

              {!generatedPlan ? (
                <div className="plan-form">
                  <div className="form-group">
                    <label>Goal Race</label>
                    <select
                      value={planForm.goal_race}
                      onChange={(e) => setPlanForm({ ...planForm, goal_race: e.target.value })}
                    >
                      <option value="5K">5K</option>
                      <option value="10K">10K</option>
                      <option value="Half Marathon">Half Marathon</option>
                      <option value="Marathon">Marathon</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Goal Time</label>
                    <input
                      type="text"
                      placeholder="e.g., 22:00 or 1:45:00"
                      value={planForm.goal_time}
                      onChange={(e) => setPlanForm({ ...planForm, goal_time: e.target.value })}
                    />
                    {context?.predictions?.[planForm.goal_race] && (
                      <span className="form-hint">
                        Current prediction: {context.predictions[planForm.goal_race].time}
                      </span>
                    )}
                  </div>

                  <div className="form-group">
                    <label>Weeks Until Race</label>
                    <input
                      type="number"
                      min="4"
                      max="24"
                      value={planForm.weeks}
                      onChange={(e) => setPlanForm({ ...planForm, weeks: parseInt(e.target.value) || 8 })}
                    />
                  </div>

                  <button
                    className="btn btn-primary btn-full"
                    onClick={generatePlan}
                    disabled={!planForm.goal_time || isPlanLoading}
                  >
                    {isPlanLoading ? (
                      <>
                        <Loader2 size={18} className="spin" />
                        Generating Plan...
                      </>
                    ) : (
                      <>
                        <Calendar size={18} />
                        Generate Plan
                      </>
                    )}
                  </button>
                </div>
              ) : (
                <div className="plan-result">
                  {generatedPlan.error ? (
                    <div className="plan-error">
                      <p>{generatedPlan.error}</p>
                      <button
                        className="btn btn-secondary"
                        onClick={() => setGeneratedPlan(null)}
                      >
                        Try Again
                      </button>
                    </div>
                  ) : (
                    <>
                      <div className="plan-header-info">
                        <h3>{generatedPlan.goal_race} Training Plan</h3>
                        <p>Goal: {generatedPlan.goal_time} | {generatedPlan.weeks} weeks</p>
                        {generatedPlan.current_prediction && (
                          <p className="current-pred">Current prediction: {generatedPlan.current_prediction}</p>
                        )}
                      </div>

                      {generatedPlan.plan && (
                        <>
                          <div className="plan-summary">
                            <p>{generatedPlan.plan.summary}</p>
                            {generatedPlan.plan.key_workouts && (
                              <div className="key-workouts">
                                <strong>Key Workouts:</strong>
                                <ul>
                                  {generatedPlan.plan.key_workouts.map((w, i) => (
                                    <li key={i}>{w}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>

                          <div className="plan-weeks">
                            {generatedPlan.plan.weeks?.map((week, idx) => (
                              <div key={idx} className="plan-week">
                                <div className="week-header">
                                  <span className="week-number">Week {week.week}</span>
                                  <span className="week-focus">{week.focus}</span>
                                  <span className="week-miles">{week.total_miles} mi</span>
                                </div>
                                <div className="week-days">
                                  {week.days?.map((day, dayIdx) => (
                                    <div key={dayIdx} className="day-workout">
                                      <span className="day-name">{day.day}</span>
                                      <span className="workout">{day.workout}</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            ))}
                          </div>

                          {generatedPlan.plan.race_day_tips && (
                            <div className="race-tips">
                              <strong>Race Day Tips:</strong>
                              <p>{generatedPlan.plan.race_day_tips}</p>
                            </div>
                          )}

                          {generatedPlan.plan.notes && (
                            <div className="plan-notes">
                              <strong>Notes:</strong>
                              <p>{generatedPlan.plan.notes}</p>
                            </div>
                          )}
                        </>
                      )}

                      <div className="plan-actions">
                        <button
                          className="btn btn-secondary"
                          onClick={() => setGeneratedPlan(null)}
                        >
                          Generate Another
                        </button>
                        <button
                          className="btn btn-primary"
                          onClick={() => setShowPlanModal(false)}
                        >
                          Done
                        </button>
                      </div>
                    </>
                  )}
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export default Coach
