import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, AlertCircle, XCircle, X } from 'lucide-react'
import clsx from 'clsx'

const Toast = ({ type, title, message, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose()
    }, 5000)

    return () => clearTimeout(timer)
  }, [onClose])

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'error':
        return <XCircle className="h-5 w-5 text-red-500" />
      case 'warning':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />
      default:
        return <CheckCircle className="h-5 w-5 text-blue-500" />
    }
  }

  const getBorderColor = () => {
    switch (type) {
      case 'success':
        return 'border-l-green-500'
      case 'error':
        return 'border-l-red-500'
      case 'warning':
        return 'border-l-yellow-500'
      default:
        return 'border-l-blue-500'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 300 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 300 }}
      className={clsx(
        'bg-white border border-gray-200 rounded-lg shadow-lg p-4 min-w-80 border-l-4',
        getBorderColor()
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          {getIcon()}
          <div>
            <h4 className="font-semibold text-gray-900">{title}</h4>
            <p className="text-sm text-gray-600 mt-1">{message}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 p-1"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </motion.div>
  )
}

export default Toast