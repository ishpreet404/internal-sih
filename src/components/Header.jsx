import React from 'react'
import { Train } from 'lucide-react'
import clsx from 'clsx'

const Header = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'upload', label: 'Upload', icon: '📤' },
    { id: 'chat', label: 'AI Chat', icon: '💬' },
    { id: 'results', label: 'Results', icon: '📊' }
  ]

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-40">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <Train className="h-8 w-8 text-primary-600" />
            <h1 className="text-xl font-bold text-gray-900">
              Railway Document Intelligence
            </h1>
          </div>
          
          <nav className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={clsx(
                  'flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-200',
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                )}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header