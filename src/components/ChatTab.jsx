import React, { useState } from 'react'
import { Send, Bot, User, Lightbulb } from 'lucide-react'
import { motion } from 'framer-motion'
import clsx from 'clsx'
import { apiService } from '../services/api'

const ChatTab = ({ processedData, isEnabled }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: isEnabled 
        ? "Hello! I've analyzed your documents. Ask me anything about the railway documents you've processed."
        : "Hello! Upload and process documents first, then I can help you analyze them, answer questions, and provide insights about railway-related content."
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  const quickQuestions = [
    "What type of railway document is this?",
    "Extract all dates and schedules mentioned",
    "Find safety and compliance information",
    "Summarize the main points"
  ]

  const handleSendMessage = async (message) => {
    if (!message.trim() || !isEnabled) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsTyping(true)

    try {
      // Call the real API
      const response = await apiService.chatWithDocuments(message, processedData)
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.response
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your question. Please try again.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleQuickQuestion = (question) => {
    handleSendMessage(question)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage(inputValue)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">AI Document Assistant</h2>
        <p className="text-lg text-gray-600">
          Ask questions about your processed documents
        </p>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden">
        {/* Chat Messages */}
        <div className="h-96 overflow-y-auto p-6 bg-gray-50">
          <div className="space-y-4">
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={clsx(
                  'flex',
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                <div className={clsx(
                  'flex max-w-xs lg:max-w-md xl:max-w-lg',
                  message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
                )}>
                  <div className={clsx(
                    'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
                    message.type === 'user' 
                      ? 'bg-primary-600 text-white ml-2' 
                      : 'bg-gray-600 text-white mr-2'
                  )}>
                    {message.type === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                  </div>
                  <div className={clsx(
                    'px-4 py-2 rounded-lg',
                    message.type === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-white border border-gray-200 text-gray-900'
                  )}>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              </motion.div>
            ))}
            
            {isTyping && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-start"
              >
                <div className="flex">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 text-white flex items-center justify-center mr-2">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Chat Input */}
        <div className="p-6 bg-white border-t border-gray-200">
          <div className="flex space-x-2 mb-4">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={!isEnabled}
              placeholder={isEnabled ? "Ask me about the processed documents..." : "Process documents first to enable chat"}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all duration-200"
            />
            <button
              onClick={() => handleSendMessage(inputValue)}
              disabled={!isEnabled || !inputValue.trim() || isTyping}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all duration-200"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>

          {/* Quick Questions */}
          {isEnabled && (
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Lightbulb className="h-4 w-4" />
                <span>Quick questions:</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {quickQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickQuestion(question)}
                    disabled={isTyping}
                    className="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-primary-100 hover:text-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatTab