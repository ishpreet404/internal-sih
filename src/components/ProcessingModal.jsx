import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Loader } from 'lucide-react'

const ProcessingModal = ({ isOpen, status, progress }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="bg-white rounded-xl p-8 max-w-md w-full mx-4 text-center"
          >
            <div className="flex flex-col items-center space-y-4">
              <Loader className="h-12 w-12 text-primary-600 animate-spin" />
              <h3 className="text-xl font-semibold text-gray-900">
                Processing Documents...
              </h3>
              <p className="text-gray-600">{status}</p>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div
                  className="bg-primary-600 h-2 rounded-full"
                  initial={{ width: '0%' }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
              
              <p className="text-sm text-gray-500">{progress}% complete</p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default ProcessingModal